import sqlite3

class Registration:
    def __init__(self, id, event_id, user_id, status, custom_form_data, qr_code_token, created_at):
        self.id = id
        self.event_id = event_id
        self.user_id = user_id
        self.status = status
        self.custom_form_data = custom_form_data
        self.qr_code_token = qr_code_token
        self.created_at = created_at

    @staticmethod
    def get_db():
        return sqlite3.connect('instance/database.db')

    @classmethod
    def create(cls, event_id, user_id, status, custom_form_data, qr_code_token, created_at):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO registrations 
            (event_id, user_id, status, custom_form_data, qr_code_token, created_at) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (event_id, user_id, status, custom_form_data, qr_code_token, created_at)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @classmethod
    def get_all(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registrations")
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def get_by_id(cls, registration_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registrations WHERE id = ?", (registration_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None
        
    @classmethod
    def get_by_event_and_user(cls, event_id, user_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registrations WHERE event_id = ? AND user_id = ?", (event_id, user_id))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def update_status(cls, registration_id, status):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE registrations SET status = ? WHERE id = ?", (status, registration_id))
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, registration_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM registrations WHERE id = ?", (registration_id,))
        conn.commit()
        conn.close()
