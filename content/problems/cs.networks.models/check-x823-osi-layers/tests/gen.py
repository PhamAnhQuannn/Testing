"""Inputs of check-x823-osi-layers; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {"id": "s1", "args": [["HTTP", "TCP", "IP", "FOO"]]},
    {"id": "s2", "args": [["ETHERNET", "WIFI", "TLS"]]},
]

HIDDEN = [
    {"id": "h01", "args": [[]], "tags": ["edge", "empty"]},
    {"id": "h02", "args": [["HTTP"]], "tags": ["edge", "single"]},
    {
        "id": "h03",
        "args": [
            [
                "HTTP",
                "DNS",
                "FTP",
                "SMTP",
                "TLS",
                "SSL",
                "TCP",
                "UDP",
                "IP",
                "ICMP",
                "ARP",
                "ETHERNET",
                "MAC",
                "WIFI",
                "ETHERNET_PHY",
            ]
        ],
        "tags": ["all-known"],
    },
    {"id": "h04", "args": [["FOO"]], "tags": ["edge", "unknown"]},
    {"id": "h05", "args": [["BAR", "BAZ", "QUIC"]], "tags": ["unknown"]},
    {"id": "h06", "args": [["DNS", "XYZ", "UDP", "IP", "NOPE"]], "tags": ["mixed"]},
    {"id": "h07", "args": [["TCP", "TCP", "TCP", "HTTP", "HTTP"]], "tags": ["repeated"]},
    {
        "id": "h08",
        "args": [["WIFI", "ETHERNET", "IP", "TCP", "TLS", "HTTP"]],
        "tags": ["every-layer"],
    },
    {"id": "h09", "args": [["ETHERNET_PHY", "MAC", "SSL", "ICMP"]], "tags": ["underscore"]},
    {"id": "h10", "args": [["", "ARP", "SMTP"]], "tags": ["edge", "empty-string"]},
]

KNOWN = [
    "HTTP",
    "DNS",
    "FTP",
    "SMTP",
    "TLS",
    "SSL",
    "TCP",
    "UDP",
    "IP",
    "ICMP",
    "ARP",
    "ETHERNET",
    "MAC",
    "WIFI",
    "ETHERNET_PHY",
]
UNKNOWN = ["FOO", "BAR", "QUIC", "SSH", "NOPE"]
POOL = KNOWN + UNKNOWN


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        length = (x >> 8) % 11
        protocols = []
        for _r in range(length):
            x = (x * 1103515245 + 12345) % 2147483648
            protocols.append(POOL[(x >> 8) % len(POOL)])
        out.append([protocols])
    return out


for _i, _a in enumerate(_lcg(823, 10)):
    HIDDEN.append({"id": f"h{11 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
