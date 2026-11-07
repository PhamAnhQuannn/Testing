import sqlite3


def filter_rows(rows, threshold):
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE t (name TEXT, score INTEGER, active INTEGER)")
    cur.executemany("INSERT INTO t(name, score, active) VALUES (?, ?, ?)", rows)
    cur.execute(
        "SELECT name, score FROM t WHERE score >= ? AND active = 1 ORDER BY score DESC, name ASC",
        (threshold,),
    )
    result = [list(r) for r in cur.fetchall()]
    con.close()
    return result
