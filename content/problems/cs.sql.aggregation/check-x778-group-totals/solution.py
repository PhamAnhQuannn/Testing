import sqlite3


def group_totals(rows):
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE sales (category TEXT, amount INTEGER)")
    cur.executemany("INSERT INTO sales(category, amount) VALUES (?, ?)", rows)
    cur.execute(
        "SELECT category, COUNT(*) AS n, SUM(amount) AS total FROM sales "
        "GROUP BY category HAVING SUM(amount) > 0 ORDER BY total DESC, category ASC"
    )
    result = [list(r) for r in cur.fetchall()]
    con.close()
    return result
