# -*- coding: utf-8 -*-
import pycountry
from ua_parser import user_agent_parser
from library.parseurl import ParseURL
from urllib.parse import parse_qs

url_parser = ParseURL()


def flatten_dict(dd, separator='_', prefix=''):
    # https://www.geeksforgeeks.org/python-convert-nested-dictionary-into-flattened-dictionary/
    # conversion of nested dictionary
    # into flattened dictionary
    return {prefix + separator + k if prefix else k: v
            for kk, vv in dd.items()
            for k, v in flatten_dict(vv, separator, kk).items()
            } if isinstance(dd, dict) else {prefix: dd}


def merge_two_dicts(dict_x, dict_y):
    """two dictionaries in python using the update"""
    dict_z = dict_x.copy()  # start with x's keys and values
    dict_z.update(dict_y)  # modifies z with y's keys and values & returns None
    return dict_z


def normalize_country(country_name: str | None):
    if country_name is None:
        return ''

    # check if input_string is a string
    if not isinstance(country_name, str):
        return country_name

    try:
        country_name_result = pycountry.countries.get(alpha_2=country_name)
        if country_name_result is not None:
            country_name = country_name_result.name
        else:
            country_name = ''

    except Exception as e:
        print(e)
        pass

    return country_name


def normalize_string(input_string: str | None, max_length: int = 250):
    if input_string is None:
        return ''

    # check if input_string is a string
    if not isinstance(input_string, str):
        return input_string

    if isinstance(input_string, str):
        # max string length for input_string is 100 characters concat with 3 dots
        if len(input_string) > max_length:
            input_string = input_string[:max_length] + '...'
        input_string = input_string.replace(',', ':')

    return input_string


def parse_browser_agent(agent_string: str) -> dict:
    parsed_string = user_agent_parser.Parse(agent_string)
    data_result = {
        'user_agent_device_family': parsed_string.get("device").get("family"),
        'user_agent_device_brand': parsed_string.get("device").get("brand"),
        'user_agent_device_model': parsed_string.get("device").get("model"),
        'user_agent_platform_family': parsed_string.get("os").get("family"),
        'user_agent_platform_major': parsed_string.get("os").get("major"),
        'user_agent_platform_minor': parsed_string.get("os").get("minor"),
        'user_agent_platform_patch': parsed_string.get("os").get("patch"),
        'user_agent_family': parsed_string.get("user_agent").get("family"),
        'user_agent_major': parsed_string.get("user_agent").get("major"),
        'user_agent_minor': parsed_string.get("user_agent").get("minor"),
        'user_agent_patch': parsed_string.get("user_agent").get("patch"),
    }

    return data_result


def parse_url(url):
    parse_result = url_parser.parse_url(url)

    dict_result = parse_qs(parse_result["query"])

    url_dict = {
        'scheme': '',
        'hostname': '',
        'path': '',
        'query': '',
        'utm_source': '',
        'utm_medium': '',
        'utm_campaign': '',
        'utm_content': '',
        'utm_term': '',
        'product': '',
        'search_keyword': '',
        'msclkid': '',
        'gclid': '',
    }

    # if utm_source is not in the query string, return None
    if parse_result['scheme'] is not None:
        url_dict['scheme'] = parse_result['scheme']

    if parse_result['hostname'] is not None:
        url_dict['hostname'] = parse_result['hostname']

    if parse_result['path'] is not None:
        url_dict['path'] = parse_result['path']

    if parse_result['query'] is not None:
        url_dict['query'] = parse_result['query']

    if 'utm_source' in dict_result:
        url_dict['utm_source'] = dict_result['utm_source'][0]

    if 'utm_medium' in dict_result:
        url_dict['utm_medium'] = dict_result['utm_medium'][0]

    if 'utm_campaign' in dict_result:
        url_dict['utm_campaign'] = dict_result['utm_campaign'][0]

    if 'utm_content' in dict_result:
        url_dict['utm_content'] = dict_result['utm_content'][0]

    if 'utm_term' in dict_result:
        url_dict['utm_term'] = normalize_string(dict_result['utm_term'][0])

    if 'product' in dict_result:
        url_dict['product'] = dict_result['product'][0]

    if 'ask' in dict_result:
        url_dict['search_keyword'] = normalize_string(dict_result['ask'][0])

    if 'searchfor' in dict_result:
        url_dict['search_keyword'] = normalize_string(
            dict_result['searchfor'][0])

    if 'wd' in dict_result:
        url_dict['search_keyword'] = normalize_string(dict_result['wd'][0])

    if 'kw' in dict_result:
        url_dict['search_keyword'] = normalize_string(dict_result['kw'][0])

    if 'Q' in dict_result:
        url_dict['search_keyword'] = normalize_string(dict_result['Q'][0])

    if 'query' in dict_result:
        url_dict['search_keyword'] = normalize_string(dict_result['query'][0])

    if 'q' in dict_result:
        url_dict['search_keyword'] = normalize_string(dict_result['q'][0])

    # auto-tagging
    if 'msclkid' in dict_result:
        url_dict['msclkid'] = dict_result['msclkid'][0]

    if 'gclid' in dict_result:
        url_dict['gclid'] = dict_result['gclid'][0]

    return url_dict


def get_search_keyword(query_string: str | None = None):
    dict_result = parse_qs(query_string)
    query_dict = {'search_keyword': ''}

    # if utm_source is not in the query string, return None
    if 'q' in dict_result:
        query_dict['search_keyword'] = dict_result['q'][0]

    if 'ask' in dict_result:
        query_dict['search_keyword'] = normalize_string(dict_result['ask'][0])

    if 'searchfor' in dict_result:
        query_dict['search_keyword'] = normalize_string(
            dict_result['searchfor'][0])

    if 'wd' in dict_result:
        query_dict['search_keyword'] = normalize_string(dict_result['wd'][0])

    if 'kw' in dict_result:
        query_dict['search_keyword'] = normalize_string(dict_result['kw'][0])

    if 'Q' in dict_result:
        query_dict['search_keyword'] = normalize_string(dict_result['Q'][0])

    if 'query' in dict_result:
        query_dict['search_keyword'] = normalize_string(
            dict_result['query'][0])

    if 'q' in dict_result:
        query_dict['search_keyword'] = normalize_string(dict_result['q'][0])

    return query_dict


def get_http_code_desc(http_status_code: str | None = None):
    if http_status_code is not None and http_status_code != '':
        http_status_code = int(http_status_code)  # cast to int
    else:
        http_status_code = 000
    # https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
    # https://www.iana.org/assignments/as-numbers/as-numbers.xhtml
    responses = {
        000: 'Unknown',
        100: 'Continue',
        101: 'Switching Protocols',
        102: 'Processing',
        103: 'Early Hints',
        # 104 - 199: 'Unassigned,
        200: 'OK',
        201: 'Created',
        202: 'Accepted',
        203: 'Non-Authoritative Information',
        204: 'No Content',
        205: 'Reset Content',
        206: 'Partial Content',
        207: 'Multi-Status',
        208: 'Already Reported',
        # 209 - 225: 'Unassigned,
        226: 'IM Used',
        # 227 - 299: 'Unassigned,
        300: 'Multiple Choices',
        301: 'Moved Permanently',
        302: 'Found',
        303: 'See Other',
        304: 'Not Modified',
        305: 'Use Proxy',
        306: '(Unused)',
        307: 'Temporary Redirect',
        308: 'Permanent Redirect',
        # 309 - 399: 'Unassigned,
        400: 'Bad Request',
        401: 'Unauthorized',
        402: 'Payment Required',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        407: 'Proxy Authentication Required',
        408: 'Request Timeout',
        409: 'Conflict',
        410: 'Gone',
        411: 'Length Required',
        412: 'Precondition Failed',
        413: 'Content Too Large',
        414: 'URI Too Long',
        415: 'Unsupported Media Type',
        416: 'Range Not Satisfiable',
        417: 'Expectation Failed',
        418: '(Unused)',
        # 419 - 420: 'Unassigned,
        421: 'Misdirected Request',
        422: 'Unprocessable Content',
        423: 'Locked',
        424: 'Failed Dependency',
        425: 'Too Early',
        426: 'Upgrade Required',
        427: 'Unassigned',
        428: 'Precondition Required',
        429: 'Too Many Requests',
        430: 'Unassigned',
        431: 'Request Header Fields Too Large',
        # 432 - 450: 'Unassigned,
        451: 'Unavailable For Legal Reasons',
        # 452 - 499: 'Unassigned,
        500: 'Internal Server Error',
        501: 'Not Implemented',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout',
        505: 'HTTP Version Not Supported',
        506: 'Variant Also Negotiates',
        507: 'Insufficient Storage',
        508: 'Loop Detected',
        509: 'Unassigned',
        510: 'Not Extended (OBSOLETED)',
        511: 'Network Authentication Required',
        # 512 - 599: 'Unassigned,
    }
    if http_status_code not in responses:
        # return f'{http_status_code} - Unknown'
        return f'Unknown'
    else:
        desc = responses[http_status_code]
        return f'{desc}'
        # return f'{http_status_code} - {desc}'


def parse_client_referer_url_string(url_string: str) -> dict:
    parsed_url_result = parse_url(url_string)
    utm_dict = {
        'clientRefererScheme': parsed_url_result['scheme'],
        'clientRefererHost': parsed_url_result['hostname'],
        'clientRefererPath': parsed_url_result['path'],
        'clientRefererQuery': parsed_url_result['query'],
        'clientReferer_utm_source': parsed_url_result['utm_source'],
        'clientReferer_utm_medium': parsed_url_result['utm_medium'],
        'clientReferer_utm_campaign': parsed_url_result['utm_campaign'],
        'clientReferer_utm_content': parsed_url_result['utm_content'],
        'clientReferer_utm_term': parsed_url_result['utm_term'],
        'clientReferer_product': parsed_url_result['product'],
        'clientReferer_search_keyword': parsed_url_result['search_keyword'],
        'clientReferer_msclkid': parsed_url_result['msclkid'],
        'clientReferer_gclid': parsed_url_result['gclid']
    }

    return utm_dict


def parse_client_request_query_string(url_string: str) -> dict:
    parsed_url_result = parse_url(url_string)
    utm_dict = {
        'clientRequest_utm_source': parsed_url_result['utm_source'],
        'clientRequest_utm_medium': parsed_url_result['utm_medium'],
        'clientRequest_utm_campaign': parsed_url_result['utm_campaign'],
        'clientRequest_utm_content': parsed_url_result['utm_content'],
        'clientRequest_utm_term': parsed_url_result['utm_term'],
        'clientRequest_product': parsed_url_result['product'],
        'clientRequest_search_keyword': parsed_url_result['search_keyword'],
        'clientRequest_msclkid': parsed_url_result['msclkid'],
        'clientRequest_gclid': parsed_url_result['gclid']
    }
    return utm_dict
