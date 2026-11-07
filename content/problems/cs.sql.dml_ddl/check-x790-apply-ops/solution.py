import sqlite3


def apply_ops(ops):
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE t (name TEXT PRIMARY KEY, score INTEGER)")
    for op in ops:
        if op[0] == "insert":
            cur.execute("INSERT OR REPLACE INTO t(name, score) VALUES (?, ?)", (op[1], op[2]))
        elif op[0] == "update":
            cur.execute("UPDATE t SET score = ? WHERE name = ?", (op[2], op[1]))
        elif op[0] == "delete":
            cur.execute("DELETE FROM t WHERE name = ?", (op[1],))
    cur.execute("SELECT name, score FROM t ORDER BY name ASC")
    result = [list(r) for r in cur.fetchall()]
    con.close()
    return result
