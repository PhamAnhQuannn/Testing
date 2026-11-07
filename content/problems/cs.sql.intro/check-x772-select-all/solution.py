import sqlite3


def select_all(rows):
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE people (name TEXT, score INTEGER)")
    cur.executemany("INSERT INTO people(name, score) VALUES (?, ?)", rows)
    cur.execute("SELECT name, score FROM people ORDER BY score DESC, name ASC")
    result = [list(r) for r in cur.fetchall()]
    con.close()
    return result
