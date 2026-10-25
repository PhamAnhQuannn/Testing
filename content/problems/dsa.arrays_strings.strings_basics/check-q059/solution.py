def add_binary(a, b):
    i, j, carry, out = (len(a) - 1, len(b) - 1, 0, [])
    while i >= 0 or j >= 0 or carry:
        t = carry
        if i >= 0:
            t += int(a[i])
            i -= 1
        if j >= 0:
            t += int(b[j])
            j -= 1
        out.append(str(t % 2))
        carry = t // 2
    return "".join(reversed(out))
