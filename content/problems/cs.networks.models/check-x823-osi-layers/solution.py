TABLE = {
    "HTTP": 7,
    "DNS": 7,
    "FTP": 7,
    "SMTP": 7,
    "TLS": 6,
    "SSL": 6,
    "TCP": 4,
    "UDP": 4,
    "IP": 3,
    "ICMP": 3,
    "ARP": 3,
    "ETHERNET": 2,
    "MAC": 2,
    "WIFI": 1,
    "ETHERNET_PHY": 1,
}


def osi_layers(protocols):
    return [TABLE.get(p, 0) for p in protocols]
