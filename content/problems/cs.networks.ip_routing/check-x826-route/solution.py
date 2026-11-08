def _to_int(ip):
    a, b, c, d = (int(p) for p in ip.split("."))
    return a << 24 | b << 16 | c << 8 | d


def route(table, ip):
    x = _to_int(ip)
    best = -1
    hop = None
    for cidr, next_hop in table:
        net, length = cidr.split("/")
        length = int(length)
        matches = length == 0 or (x >> (32 - length)) == (_to_int(net) >> (32 - length))
        if matches and length > best:
            best = length
            hop = next_hop
    return hop
