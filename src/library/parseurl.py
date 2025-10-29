# -*- coding: utf-8 -*-
import hashlib
from urllib import parse


class ParseURL:

    def __init__(self):
        self.url = None

    def validateURL(self, url: str):
        """ Validate a URL """
        try:
            result = parse.urlparse(url)
            return True
        # return all([result.scheme, result.netloc, result.path])
        except:
            return False

    def parse(self, url_string: str) -> dict:
        url = {
            "isvalid": None,
            'netloc': '',
            'scheme': '',
            'path': '',
            'query': '',
            'fragment': '',
            'hostname': '',
            'port': '',
            'host_hash': '',
            'path_hash': '',
            'url': ''
        }

        self.url = url_string
        return self.parse_url(url_string)

    def parse_url(self, url_string: str, lowercase: bool = False) -> dict:
        """ Parse a URL into 5 components:
        <scheme>://<netloc>/<path>?<query>#<fragment>
        https://docs.python.org/3/library/urllib.parse.html
        """
        url = {
            "isvalid": False,
            'netloc': '',
            'scheme': '',
            'path': '',
            'query': '',
            'fragment': '',
            'hostname': '',
            'port': '',
            'host_hash': '',
            'path_hash': '',
            'url': url_string
        }

        if self.validateURL(url_string) is False:
            return url

        try:
            if lowercase:
                url_string = url_string.lower()

            parsed = parse.urlsplit(url_string)

            url["url"] = url_string

            if parsed.hostname:
                url["hostname"] = parsed.hostname
            if parsed.netloc:
                url["netloc"] = parsed.netloc

            if parsed.port:
                url["port"] = parsed.port

            if parsed.scheme:
                url["scheme"] = parsed.scheme

            if parsed.path:
                url["path"] = parsed.path

            if parsed.fragment:
                url["fragment"] = parsed.fragment

            if parsed.query:
                url["query"] = parsed.query

            # set default http/https port
            if parsed.scheme and not parsed.port:
                if parsed.scheme == "https":
                    url["port"] = 443
                if parsed.scheme == "http":
                    url["port"] = 80

            #
            url["host_hash"] = self.host_hash_identifier(url)
            url["path_hash"] = self.path_hash_identifier(url)

            url["isvalid"] = True

        except:
            print("Error parsing url_string. ParseURL")

        return url

    def parse_query(self):
        query_result = parse.parse_qsl(parse.urlsplit(self.url).query)
        return dict(query_result)

    def path_hash_identifier(self, parsed: dict):
        scheme = parsed["scheme"]
        host = parsed["hostname"]
        port = parsed["port"]
        path = parsed["path"]

        # initializing string
        url_string = "{scheme}://{host}:{port}{path}".format(
            scheme=scheme, host=host, port=port, path=path)

        # encoding url_string using encode()
        # then sending to SHA1()
        result = hashlib.sha1(url_string.encode())

        # return the equivalent hexadecimal value.
        return result.hexdigest()

    def host_hash_identifier(self, parsed: dict):
        scheme = parsed["scheme"]
        host = parsed["hostname"]
        port = parsed["port"]

        # initializing string
        url_string = "{scheme}://{host}:{port}".format(
            scheme=scheme, host=host, port=port)

        # encoding url_string using encode()
        # then sending to SHA1()
        result = hashlib.sha1(url_string.encode())

        # return the equivalent hexadecimal value.
        return result.hexdigest()
