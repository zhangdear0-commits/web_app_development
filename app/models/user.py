import sqlite3

class User:
    def __init__(self, id, email, password_hash, name, role, phone, created_at):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.name = name
        self.role = role
        self.phone = phone
        self.created_at = created_at

    @staticmethod
    def get_db():
        return sqlite3.connect('instance/database.db')

    @classmethod
    def create(cls, email, password_hash, name, role, phone, created_at):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, password_hash, name, role, phone, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (email, password_hash, name, role, phone, created_at)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @classmethod
    def get_all(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def get_by_id(cls, user_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def update(cls, user_id, email, name, phone):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET email = ?, name = ?, phone = ? WHERE id = ?",
            (email, name, phone, user_id)
        )
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, user_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
