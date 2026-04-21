import sqlite3

class Event:
    def __init__(self, id, organizer_id, title, description, capacity, location, start_time, end_time, custom_form_schema, created_at):
        self.id = id
        self.organizer_id = organizer_id
        self.title = title
        self.description = description
        self.capacity = capacity
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
        self.custom_form_schema = custom_form_schema
        self.created_at = created_at

    @staticmethod
    def get_db():
        return sqlite3.connect('instance/database.db')

    @classmethod
    def create(cls, organizer_id, title, description, capacity, location, start_time, end_time, custom_form_schema, created_at):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO events 
            (organizer_id, title, description, capacity, location, start_time, end_time, custom_form_schema, created_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (organizer_id, title, description, capacity, location, start_time, end_time, custom_form_schema, created_at)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @classmethod
    def get_all(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events")
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def get_by_id(cls, event_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def update(cls, event_id, title, description, capacity, location, start_time, end_time, custom_form_schema):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE events 
            SET title = ?, description = ?, capacity = ?, location = ?, start_time = ?, end_time = ?, custom_form_schema = ? 
            WHERE id = ?""",
            (title, description, capacity, location, start_time, end_time, custom_form_schema, event_id)
        )
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, event_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        conn.commit()
        conn.close()
