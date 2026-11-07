from urllib.parse import parse_qsl, urlsplit


def parse_query(url):
    result = {}
    for k, v in parse_qsl(urlsplit(url).query):
        result[k] = v
    return result
