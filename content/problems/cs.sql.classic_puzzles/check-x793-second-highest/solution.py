import sqlite3


def second_highest(rows):
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE t (name TEXT, score INTEGER)")
    cur.executemany("INSERT INTO t(name, score) VALUES (?, ?)", rows)
    cur.execute(
        "SELECT name FROM t WHERE score = "
        "(SELECT DISTINCT score FROM t ORDER BY score DESC LIMIT 1 OFFSET 1) "
        "ORDER BY name ASC"
    )
    result = [r[0] for r in cur.fetchall()]
    con.close()
    return result
