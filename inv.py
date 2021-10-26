import sqlite3

class InvData:
    def __init__(self, inv):
        self.conn = sqlite3.connect(inv)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY, retailer text, part text, "
                         "price real, quantity integer, total real)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM inventory")
        rows = self.cur.fetchall()
        return rows

    def insert(self, retailer, part, price, quantity, total):
        self.cur.execute("INSERT INTO inventory VALUES (Null, ?, ?, ?, ?, ?)", (retailer, part, price, quantity, total))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM inventory WHERE id=?", (id,))  # comma after single value tuple
        self.conn.commit()

    def update(self, id, retailer, part, price, quantity, total):
        self.cur.execute("UPDATE inventory SET retailer = ?, part = ?, price = ?, quantity = ?, total = ? WHERE id = ?",
                         (retailer, part, price, quantity, total, id))
        self.conn.commit()

    def sum(self):
        findsum = "SELECT sum(total) FROM inventory"
        self.cur.execute(findsum)
        return self.cur.fetchmany()[0]

    def __del__(self):
        self.conn.close()

# inv = InvData('inventory.db')
# inv.insert("Bakelab", "muffins", 5, 100, 500)