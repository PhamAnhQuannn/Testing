import sqlite3


def rank_within(rows):
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE t (grp TEXT, name TEXT, score INTEGER)")
    cur.executemany("INSERT INTO t(grp, name, score) VALUES (?, ?, ?)", rows)
    cur.execute(
        "SELECT grp, name, "
        "ROW_NUMBER() OVER (PARTITION BY grp ORDER BY score DESC, name ASC) AS rn "
        "FROM t ORDER BY grp ASC, rn ASC"
    )
    result = [list(r) for r in cur.fetchall()]
    con.close()
    return result
