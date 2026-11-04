from unittest.mock import Mock


def fetch_with_fallback(outcomes):
    client = Mock()
    client.fetch.side_effect = [ConnectionError("down") if o is None else o for o in outcomes]

    def get_price(c, item):
        try:
            return c.fetch(item)
        except ConnectionError:
            return -1

    results = [get_price(client, i) for i in range(len(outcomes))]
    called_with = [call.args[0] for call in client.fetch.call_args_list]
    return [results, client.fetch.call_count, called_with]
