#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import random
import json
from datetime import datetime, timedelta
import requests
from library.geoinfo import GeoInfo
from library.iohelper import merge_two_dicts, parse_client_referer_url_string, parse_client_request_query_string, \
    parse_browser_agent, normalize_country
from opensearchpy import OpenSearch
from pprint import pprint
# import logging

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)

# the endpoint of GraphQL API
url = 'https://api.cloudflare.com/client/v4/graphql/'

# Customize these variables via Docker env (pass with --env-file or -e)
# Must include trailing slash. If left blank, csv will be created in the current directory.
file_dir = ''
api_token = os.getenv("CLOUDFLARE_API_KEY")
CLOUDFLARE_ACCOUNT = os.getenv("CLOUDFLARE_ACCOUNT")  # accountTag
CLOUDFLARE_ZONE = os.getenv("CLOUDFLARE_ZONE")        # zoneTag

# Set most recent day as yesterday by default.
offset_days = 1
# How many days worth of data do we want? By default, 7.
historical_days = 1

OPENSEARCH_USERNAME = os.getenv("OPENSEARCH_USERNAME", "admin")
OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD", "admin")
OPENSEARCH_HOSTNAME = os.getenv("OPENSEARCH_HOSTNAME", "opensearch-node")
OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT", "9200"))
OPENSEARCH_INDEX_PREFIX = os.getenv("OPENSEARCH_INDEX", "cloudflare-requests-")
OPENSEARCH_HOST = f"https://{OPENSEARCH_HOSTNAME}:9200"

# Cloudflare plan configuration
# Set to "true" or "1" if you have Bot Management or Enterprise plan
INCLUDE_PREMIUM_FIELDS = True if os.getenv("INCLUDE_PREMIUM_FIELDS", "false").lower() in ("true", "1", "yes") else False

es = OpenSearch(
    hosts=[{"host": OPENSEARCH_HOSTNAME,
            "port": OPENSEARCH_PORT, "scheme": "https"}],
    http_auth=(OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD),
    # turn on SSL
    use_ssl=True,
    # no verify SSL certificates
    verify_certs=False,
    # don't show warnings about ssl certs verification
    ssl_show_warn=False,
    http_compress=True,  # enables gzip compression for request bodies
)

geoip_instance = GeoInfo()


def create_index_data(index_name: str, index_data: str | dict, index_id: str | int | None,
                      doc_type: object = 'doc') -> object:
    return es.index(index=index_name, body=index_data, id=index_id)


def get_past_date(num_days):
    today = datetime.utcnow().date()
    return today - timedelta(days=num_days)


def get_cf_graphql(limit, start_date, end_date, include_premium_fields=False):

    assert (start_date <= end_date)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }
    # Make sure this is the correct URL for your Cloudflare API
    url = 'https://api.cloudflare.com/client/v4/graphql'

    # Base fields available on all plans
    base_fields = """
        clientCountryName: clientCountryName
        clientIP: clientIP
        clientRequestHTTPHost: clientRequestHTTPHost
        clientRequestHTTPMethodName: clientRequestHTTPMethodName
        clientRequestPath: clientRequestPath
        datetime: datetime
        edgeResponseStatus: edgeResponseStatus
        originResponseStatus: originResponseStatus
        sampleInterval: sampleInterval
        userAgent: userAgent
    """

    # Premium fields for Bot Management/Enterprise plans
    premium_fields = """
        originIP: originIP
        clientRequestQuery: clientRequestQuery
        clientRequestReferer: clientRequestReferer
        clientRefererHost: clientRefererHost
        clientAsn: clientAsn
        clientASNDescription: clientASNDescription
        edgeResponseContentTypeName: edgeResponseContentTypeName
        botManagementDecision: botManagementDecision
        botScoreSrcName: botScoreSrcName
        securityAction: securityAction
        securitySource: securitySource
        wafAttackScore: wafAttackScore
        wafAttackScoreClass: wafAttackScoreClass
        wafXssAttackScore: wafXssAttackScore
        xRequestedWith: xRequestedWith
    """

    # Combine fields based on plan
    dimensions_fields = base_fields
    if include_premium_fields:
        dimensions_fields += premium_fields

    payload = f'''{{
    "query": "query ZapTimeseriesBydatetimeGroupedByclientRequestPath( $zoneTag: string $filter: ZoneHttpRequestsAdaptiveGroupsFilter_InputObject ) {{ viewer {{ zones(filter: {{ zoneTag: $zoneTag }}) {{ series: httpRequestsAdaptiveGroups(limit: 10000, filter: $filter) {{ count avg {{ sampleInterval __typename }} sum {{ edgeResponseBytes visits __typename }} dimensions {{ {dimensions_fields} }} __typename }} __typename }} __typename }} }}",
     "variables": {{
    "accountTag": "{CLOUDFLARE_ACCOUNT}",
    "zoneTag": "{CLOUDFLARE_ZONE}",
    "filter": {{
      "AND": [
        {{
          "datetime_geq": "{start_date}",
          "datetime_leq": "{end_date}"
        }},
        {{
          "userAgent_neq": ""
         }},
        {{
          "userAgent_neq": "test"
        }},
        {{
          "clientRequestPath_notlike": "%/.well-known/%"
        }},
        {{
         "clientRequestPath_neq": "//.well-known/"
        }},
        {{
          "clientRequestPath_notlike": "/favicon.ico"
        }},
        {{
          "clientRequestPath_notlike": "%.ico%"
        }},
        {{
          "clientRequestPath_notlike": "%.gif%"
        }},
        {{
          "clientRequestPath_notlike": "%wlwmanifest%"
        }},
        {{
          "clientRequestPath_notlike": "%.git%"
        }},
        {{
          "clientRequestPath_notlike": "%/durbin%"
        }},
        {{
          "clientRequestPath_notlike": "%/Blueprint.aspx%"
        }},
        {{
          "clientRequestPath_notlike": "%.jsp%"
        }},
        {{
          "clientRequestPath_notlike": "%/.aws%"
        }},
        {{
          "clientRequestPath_notlike": "%/.env%"
        }},
        {{
          "clientRequestPath_notlike": "%/index.php%"
        }}
      ]
    }}
  }}
  }}'''
    payload = payload.replace('\n', '')
    payload = " ".join(payload.split())
    # print( payload )
    r = requests.post(url, data=payload.replace(
        '\n', ''), headers=headers, verify=False)
    return r


def sent_to_es(raw_data, batch_name: str = None, index_prefix_name: str = None):
    # raw data is a json string conver to dict'
    response = json.loads(raw_data)
    data = response.get("data")
    errors = response.get('errors')

    if errors:
        pprint(errors)

    # Check if we got any errors or missing data
    if data is None or "viewer" not in data or 'zones' not in data['viewer']:
        print('Failed to retrieve data: GraphQL API responded with error:')
        if errors:
            print('Errors:', errors)
        return

    # pprint(data)
    # loop through the raw_data['viewer']['scope']['activity'] and print it

    for item in data['viewer']['zones'][0]['series']:
        item_data = item['dimensions']

        # Ensure required fields have empty values if not present
        required_fields = [
            'clientCountryName',
            'clientIP',
            'clientRequestHTTPHost',
            'clientRequestHTTPMethodName',
            'clientRequestPath',
            'datetime',
            'edgeResponseStatus',
            'originResponseStatus',
            'sampleInterval',
            'userAgent'
        ]
        for field in required_fields:
            if field not in item_data or item_data[field] is None:
                item_data[field] = ''

        created_date = item_data['datetime']
        created_at = datetime.fromisoformat(created_date).strftime("%Y.%m.%d")

        # client request query dicts
        client_request_utm_dict = parse_client_request_query_string(
            item_data.get('clientRequestQuery', ''))
        item_data = merge_two_dicts(item_data, client_request_utm_dict)

        # user agent dicts
        parsed_user_agent = parse_browser_agent(item_data['userAgent'])
        item_data = merge_two_dicts(item_data, parsed_user_agent)

        # referer dicts
        parsed_referer = parse_client_referer_url_string(
            item_data.get('clientRequestReferer', ''))
        item_data = merge_two_dicts(item_data, parsed_referer)

        # normalize the country name
        item_data['clientRequest_CountryCode'] = item_data['clientCountryName']
        item_data['clientRequest_CountryName'] = normalize_country(
            item_data['clientCountryName'])

        # get client ip geo info
        geo_result = geoip_instance.get_ip_info(item_data['clientIP'])
        geo_dicts = {
            'clientRequest_geoip_city': geo_result['city'],
            'clientRequest_geoip_country': geo_result['country'],
            'clientRequest_geoip_country_iso_code': geo_result['country_iso_code'],
            'clientRequest_geoip_continent': geo_result['continent'],
            'clientRequest_geoip_province': geo_result['province'],
            'clientRequest_geoip_postal_code': geo_result['postal_code'],
            'clientRequest_geoip_latitude': geo_result['latitude'],
            'clientRequest_geoip_longitude': geo_result['longitude'],
            'clientRequest_geoip_geocoding': geo_result['geocoding'],
            'clientRequest_geoip_is_anonymous': geo_result['is_anonymous'],
            'clientRequest_geoip_is_anonymous_vpn': geo_result['is_anonymous_vpn'],
            'clientRequest_geoip_is_public_proxy': geo_result['is_public_proxy'],
            'clientRequest_geoip_is_residential_proxy': geo_result['is_residential_proxy'],
            'clientRequest_geoip_is_tor_exit_node': geo_result['is_tor_exit_node'],
            'clientRequest_geoip_is_hosting_provider': geo_result['is_hosting_provider'],
            'clientRequest_geoip_asn': geo_result['asn'],
            'clientRequest_geoip_asn_org': geo_result['asn_org'],
        }
        item_data = merge_two_dicts(item_data, geo_dicts)

        batch_info = {
            'log_pull_batch_name': batch_name,
            'log_pull_batch_datetime': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            # "typename": item_data['__typename'],
            'count': item['count'],
            'avg_typename': item['avg']['__typename'],
            'avg_sampleInterval': item['avg']['sampleInterval'],
            'sum_edgeResponseBytes': item['sum']['edgeResponseBytes'],
            'sum_visits': item['sum']['visits'],
            'sum_typename': item['sum']['__typename'],
            "accountTag": CLOUDFLARE_ACCOUNT,
            "zoneTag": CLOUDFLARE_ZONE,
        }
        item_data = merge_two_dicts(item_data, batch_info)
        index_name = index_prefix_name + created_at
        create_index_data(index_name=index_name, index_data=item_data,
                          index_id=None)


def main():
    """ Main entry point of the app """

    global item_end_date

    # ---- Read run-time config from env ----
    index_prefix_name = OPENSEARCH_INDEX_PREFIX
    batch_name = os.getenv("LOG_BACTH_NAME", "LOG250731")

    # Dates from env (YYYY-MM-DD), converted to full Zulu timestamps
    start_date_env = os.getenv("LOG_DATE_START", "2025-10-01")
    end_date_env = os.getenv("LOG_DATE_END", "2025-10-31")

    start_date_obj = datetime.strptime(
        f"{start_date_env}T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"
    )
    end_date_obj = datetime.strptime(
        f"{end_date_env}T23:59:00Z", "%Y-%m-%dT%H:%M:%SZ"
    )

    counter = 1
    api_row_limit = 10000
    end_date_timestamp = end_date_obj.timestamp()

    # Explicitly seed the random number generator based on the current time
    random.seed()

    while True:
        if counter == 1:
            start_date = start_date_obj
        else:
            start_date = item_end_date

        item_start_date = start_date
        item_start_date_string = item_start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        item_end_date = item_start_date + timedelta(hours=6)
        item_end_date_string = item_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        print("[item_start_date] {}".format(item_start_date_string))
        print("[item_end_date  ] {}".format(item_end_date_string))

        try:
            r = get_cf_graphql(
                api_row_limit, item_start_date_string, item_end_date_string, INCLUDE_PREMIUM_FIELDS)
            r.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            if r is not None:
                print(f'Response content: {r.content}')
        except requests.exceptions.RequestException as err:
            print(f'Other error occurred: {err}')
        else:
            if r is not None:
                try:
                    sent_to_es(r.text, batch_name, index_prefix_name)
                except json.JSONDecodeError as json_err:
                    print(f'JSON decode error: {json_err}')
                    print(f'Response content: {r.content}')
            else:
                print('No response received')

        # increment the file number
        counter += 1
        print("[tem_counter ] {}".format(counter))
        # convert the start date to unix time
        current_item_date_timestamp = item_start_date.timestamp()
        if current_item_date_timestamp > end_date_timestamp:
            print("End of the loop")
            break

        # Sleep for a random time between 2 and 7 seconds (floating-point)
        sleep_time = random.uniform(7, 12)
        print("[Slow the process ] Sleeping for " +
              str(sleep_time) + " seconds")
        time.sleep(sleep_time)


# Prevents main() from being executed during imports.
if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
