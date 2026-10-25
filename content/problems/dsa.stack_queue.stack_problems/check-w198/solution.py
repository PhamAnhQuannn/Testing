def backspace_equal(s, t):

    def f(x):
        st = []
        for ch in x:
            if ch == "#":
                if st:
                    st.pop()
            else:
                st.append(ch)
        return st

    return f(s) == f(t)
