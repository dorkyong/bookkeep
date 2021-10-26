import sqlite3

class EmployeeData:
    def __init__(self, emp):
        self.conn = sqlite3.connect(emp)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS employee (id INTEGER PRIMARY KEY, name text, pay real)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM employee")
        rows = self.cur.fetchall()
        return rows

    def insert(self, name, pay):
        self.cur.execute("INSERT INTO employee VALUES (Null, ?, ?)", (name, pay))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM employee WHERE id=?", (id,))  # comma after single value tuple
        self.conn.commit()

    def update(self, id, name, pay):
        self.cur.execute("UPDATE employee SET retailer = ?, part = ?, price = ?, quantity = ?, total = ? WHERE id = ?",
                         (retailer, part, price, quantity, total, id))
        self.conn.commit()

    def sum(self):
        findsum = "SELECT sum(pay) FROM employee"
        self.cur.execute(findsum)
        return self.cur.fetchmany()[0]

    def __del__(self):
        self.conn.close()
#
# emp = EmployeeData('employee.db')
# emp.insert("Toby", 4000)
# emp.insert("William", 3000)