import json


def json_summary(text):
    items = json.loads(text)
    return {
        "count": len(items),
        "total_qty": sum(it["qty"] for it in items),
        "total_value": sum(it["price"] * it["qty"] for it in items),
    }
