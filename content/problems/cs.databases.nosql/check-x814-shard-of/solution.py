def shard_of(keys, n):
    return [sum(ord(c) for c in key) % n for key in keys]
