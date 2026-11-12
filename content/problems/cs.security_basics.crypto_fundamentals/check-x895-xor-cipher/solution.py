def xor_cipher(data, key):
    return [b ^ key[i % len(key)] for i, b in enumerate(data)]
