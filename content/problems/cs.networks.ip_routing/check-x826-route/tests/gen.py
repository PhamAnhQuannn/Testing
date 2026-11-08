"""Inputs of check-x826-route; `expected` comes from solution.py via gen_hidden."""

SAMPLES = [
    {
        "id": "s1",
        "args": [
            [["0.0.0.0/0", "R0"], ["10.0.0.0/8", "R1"], ["10.1.0.0/16", "R2"]],
            "10.1.2.3",
        ],
    },
    {
        "id": "s2",
        "args": [
            [["0.0.0.0/0", "R0"], ["10.0.0.0/8", "R1"], ["10.1.0.0/16", "R2"]],
            "8.8.8.8",
        ],
    },
]

HIDDEN = [
    {
        "id": "h01",
        "args": [[["10.0.0.0/8", "R1"], ["192.168.0.0/16", "R2"]], "11.1.1.1"],
        "tags": ["edge", "no-match"],
    },
    {"id": "h02", "args": [[], "1.2.3.4"], "tags": ["edge", "empty-table"]},
    {
        "id": "h03",
        "args": [[["0.0.0.0/0", "GW"]], "203.0.113.9"],
        "tags": ["edge", "default-only"],
    },
    {
        "id": "h04",
        "args": [[["10.0.0.0/8", "A"], ["10.0.0.5/32", "B"]], "10.0.0.5"],
        "tags": ["exact-32"],
    },
    {
        "id": "h05",
        "args": [[["10.0.0.5/32", "B"], ["10.0.0.0/8", "A"]], "10.0.0.6"],
        "tags": ["exact-32", "no-match-32"],
    },
    {
        "id": "h06",
        "args": [[["10.0.0.0/8", "A"], ["10.1.0.0/16", "B"], ["10.1.2.0/24", "C"]], "10.1.2.200"],
        "tags": ["overlap", "longest-wins"],
    },
    {
        "id": "h07",
        "args": [[["10.1.2.0/24", "C"], ["10.1.0.0/16", "B"], ["10.0.0.0/8", "A"]], "10.1.9.9"],
        "tags": ["overlap", "longest-listed-first"],
    },
    {
        "id": "h08",
        "args": [[["10.0.0.0/8", "A"], ["10.5.0.0/8", "B"]], "10.200.1.1"],
        "tags": ["tie", "first-wins"],
    },
    {
        "id": "h09",
        "args": [
            [["172.16.0.0/12", "X"], ["172.16.0.0/12", "Y"], ["0.0.0.0/0", "D"]],
            "172.31.255.255",
        ],
        "tags": ["tie", "first-wins"],
    },
    {
        "id": "h10",
        "args": [[["192.168.1.0/24", "LAN"], ["0.0.0.0/0", "WAN"]], "192.168.1.0"],
        "tags": ["ip-equals-network"],
    },
    {
        "id": "h11",
        "args": [[["0.0.0.0/0", "D"], ["192.168.1.0/24", "LAN"]], "192.168.2.1"],
        "tags": ["default-first", "boundary"],
    },
    {
        "id": "h12",
        "args": [[["10.0.0.0/31", "P"], ["10.0.0.2/31", "Q"]], "10.0.0.3"],
        "tags": ["boundary", "slash31"],
    },
    {
        "id": "h13",
        "args": [[["128.0.0.0/1", "HI"], ["0.0.0.0/1", "LO"]], "255.255.255.255"],
        "tags": ["edge", "slash1"],
    },
    {
        "id": "h14",
        "args": [[["0.0.0.0/0", "D"], ["0.0.0.0/0", "E"]], "0.0.0.0"],
        "tags": ["tie", "default-twice"],
    },
]

POOL = [0, 10, 172, 192]
LENS = [0, 8, 16, 24, 32, 8, 16]


def _lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        count = 1 + (x >> 8) % 5
        table = []
        for _r in range(count):
            octets = []
            for _o in range(4):
                x = (x * 1103515245 + 12345) % 2147483648
                octets.append(POOL[(x >> 8) % len(POOL)])
            x = (x * 1103515245 + 12345) % 2147483648
            length = LENS[(x >> 8) % len(LENS)]
            x = (x * 1103515245 + 12345) % 2147483648
            hop = "R" + str((x >> 8) % 6)
            table.append([".".join(str(o) for o in octets) + "/" + str(length), hop])
        octets = []
        for _o in range(4):
            x = (x * 1103515245 + 12345) % 2147483648
            octets.append(POOL[(x >> 8) % len(POOL)])
        out.append([table, ".".join(str(o) for o in octets)])
    return out


for _i, _a in enumerate(_lcg(61, 12)):
    HIDDEN.append({"id": f"h{15 + _i:02d}", "args": _a, "tags": []})


def sample_inputs():
    return SAMPLES


def hidden_inputs():
    return HIDDEN


def small_inputs(seed, n):
    return [{"id": f"r{i}", "args": a} for i, a in enumerate(_lcg(seed, n))]
