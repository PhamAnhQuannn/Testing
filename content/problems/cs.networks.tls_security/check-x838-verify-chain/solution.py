def verify_chain(certs):
    if not certs:
        return False
    for i in range(len(certs) - 1):
        if certs[i][1] != certs[i + 1][0]:
            return False
    return certs[-1][0] == certs[-1][1]
