# -*- coding: utf-8 -*-
import typing as t
import geoip2.database
import geoip2.errors
import os
import logging

logger = logging.getLogger(__name__)


# a class that will geoip2_city_reader and geoip2_asn_reader
# and return a dict with the geoip2 data
class GeoInfo:
    def __init__(self):
        # Get the directory where this script is located (src/library/)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate to the db directory (src/db/)
        db_dir = os.path.join(os.path.dirname(script_dir), 'db')

        self.geoip2_city_reader = geoip2.database.Reader(os.path.join(db_dir, 'GeoLite2-City.mmdb'))
        self.geoip2_asn_reader = geoip2.database.Reader(os.path.join(db_dir, 'GeoLite2-ASN.mmdb'))

    def get_asn_info(self, ip: str) -> t.Dict[str, str]:
        try:
            asn_data = self.geoip2_asn_reader.asn(ip)
        except:
            # except geoip2.errors.AddressNotFoundError as e:
            #     print("AddressNotFoundError: {}".format(e))
            pass
            return {
                'asn': '',
                'asn_org': '',
            }

        return {
            'asn': asn_data.autonomous_system_number,
            'asn_org': asn_data.autonomous_system_organization,
        }

    def get_ip_info(self, ip: str) -> t.Dict[str, str]:
        try:
            city_data = self.geoip2_city_reader.city(ip)
            asn_data = self.geoip2_asn_reader.asn(ip)
        except:
            # except geoip2.errors.AddressNotFoundError as e:
            #     print("AddressNotFoundError: {}".format(e))
            pass
            return {
                'city': '',
                'country': '',
                'country_iso_code': '',
                'continent': '',
                'province': '',
                'postal_code': '',
                'latitude': '',
                'longitude': '',
                'geocoding': '',
                'is_anonymous': '',
                'is_anonymous_vpn': '',
                'is_public_proxy': '',
                'is_residential_proxy': '',
                'is_tor_exit_node': '',
                'is_hosting_provider': '',
                'asn': '',
                'asn_org': '',
            }

        asn = ''
        asn_org = ''
        if asn_data is not None:
            asn = asn_data.autonomous_system_number
            asn_org = asn_data.autonomous_system_organization

        latitude = ''
        longitude = ''
        if city_data is not None and city_data.city.name:
            latitude = city_data.location.latitude
            longitude = city_data.location.longitude

        return {
            'city': city_data.city.name,
            'country': city_data.country.name,
            'country_iso_code': city_data.country.iso_code,
            'continent': city_data.continent.name,
            'province': city_data.subdivisions.most_specific.name,
            'postal_code': city_data.postal.code,
            'latitude': latitude,
            'longitude': longitude,
            'geocoding': "{},{}".format(latitude, longitude),
            'is_anonymous': city_data.traits.is_anonymous,
            'is_anonymous_vpn': city_data.traits.is_anonymous_vpn,
            'is_public_proxy': city_data.traits.is_public_proxy,
            'is_residential_proxy': city_data.traits.is_residential_proxy,
            'is_tor_exit_node': city_data.traits.is_tor_exit_node,
            'is_hosting_provider': city_data.traits.is_hosting_provider,
            'asn': asn,
            'asn_org': asn_org,
        }
