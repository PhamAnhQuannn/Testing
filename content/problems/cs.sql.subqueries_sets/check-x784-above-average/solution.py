import sqlite3


def above_average(rows):
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE t (name TEXT, score INTEGER)")
    cur.executemany("INSERT INTO t(name, score) VALUES (?, ?)", rows)
    cur.execute(
        "SELECT name, score FROM t WHERE score > (SELECT AVG(score) FROM t) "
        "ORDER BY score DESC, name ASC"
    )
    result = [list(r) for r in cur.fetchall()]
    con.close()
    return result
