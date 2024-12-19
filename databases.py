import sqlite3


class Database:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def get_user(self, user_id):
        return self.cur.execute("""SELECT * FROM users WHERE user_id = ?""", (user_id,)).fetchone()

    def new_user(self, user_id, name, phone):
        self.cur.execute("""INSERT INTO users VALUES(?, ?, ?)""", (user_id, name, phone))
        self.con.commit()

    def get_tasks(self, user_id):
        return self.cur.execute("""SELECT * FROM tasks WHERE user_id = ?""", (user_id,)).fetchall()

    def new_tasks(self, user_id, text):
        self.cur.execute("""INSERT INTO tasks(user_id, text) VALUES(?, ?)""", (user_id, text))
        self.con.commit()

    def del_task(self, id):
        self.cur.execute("""DELETE FROM tasks WHERE id = ?""", (id,))
        self.con.commit()