import sqlite3


def top_products(rows):
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE sales (product TEXT, qty INTEGER)")
    cur.executemany("INSERT INTO sales(product, qty) VALUES (?, ?)", rows)
    cur.execute(
        "SELECT product, SUM(qty) AS total FROM sales "
        "GROUP BY product ORDER BY total DESC, product ASC"
    )
    result = [list(r) for r in cur.fetchall()]
    con.close()
    return result
