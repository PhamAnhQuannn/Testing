def cache_decision(req_headers, resp_headers):
    if "no-store" in resp_headers:
        return "network"
    if "no-cache" in resp_headers:
        return "revalidate"
    if (
        "max-age" in resp_headers
        and "age" in req_headers
        and int(req_headers["age"]) < int(resp_headers["max-age"])
    ):
        return "cache"
    return "network"
