def stock_span(prices):
    res = []
    st = []  # (price, span), prices strictly decreasing
    for p in prices:
        span = 1
        while st and st[-1][0] <= p:
            span += st.pop()[1]
        st.append((p, span))
        res.append(span)
    return res
