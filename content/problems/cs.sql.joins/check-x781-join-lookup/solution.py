import sqlite3


def join_lookup(orders, customers):
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE orders (order_id INTEGER, customer_id INTEGER, amount INTEGER)")
    cur.execute("CREATE TABLE customers (customer_id INTEGER, name TEXT)")
    cur.executemany("INSERT INTO orders(order_id, customer_id, amount) VALUES (?, ?, ?)", orders)
    cur.executemany("INSERT INTO customers(customer_id, name) VALUES (?, ?)", customers)
    cur.execute(
        "SELECT o.order_id, c.name, o.amount FROM orders o "
        "JOIN customers c ON o.customer_id = c.customer_id "
        "ORDER BY o.order_id ASC, c.name ASC, o.amount ASC"
    )
    result = [list(r) for r in cur.fetchall()]
    con.close()
    return result
