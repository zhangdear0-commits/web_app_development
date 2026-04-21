import sqlite3
import os

class Event:
    @staticmethod
    def get_db_connection():
        """
        取得 SQLite 資料庫連線，並設定 row_factory。
        """
        db_path = os.path.join(os.getcwd(), 'instance', 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, data):
        """
        新增一筆 Event 記錄
        :param data: dict，包含 organizer_id, title, description, capacity, location, start_time, end_time, custom_form_schema, created_at
        :return: int，新增記錄的 id，若失敗則回傳 None
        """
        try:
            conn = cls.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO events 
                (organizer_id, title, description, capacity, location, start_time, end_time, custom_form_schema, created_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (data['organizer_id'], data['title'], data.get('description'), data['capacity'], 
                 data['location'], data['start_time'], data['end_time'], data.get('custom_form_schema'), data['created_at'])
            )
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        except Exception as e:
            print(f"Error creating event: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def get_all(cls):
        """
        取得所有 Event 記錄
        :return: list of sqlite3.Row，若失敗則回傳空陣列
        """
        try:
            conn = cls.get_db_connection()
            rows = conn.execute("SELECT * FROM events").fetchall()
            return rows
        except Exception as e:
            print(f"Error fetching all events: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def get_by_id(cls, event_id):
        """
        取得單筆 Event 記錄
        :param event_id: int
        :return: sqlite3.Row 或是 None
        """
        try:
            conn = cls.get_db_connection()
            row = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
            return row
        except Exception as e:
            print(f"Error fetching event {event_id}: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def update(cls, event_id, data):
        """
        更新 Event 記錄
        :param event_id: int
        :param data: dict，欲更新的欄位
        :return: bool，更新是否成功
        """
        try:
            conn = cls.get_db_connection()
            fields = []
            values = []
            for k, v in data.items():
                fields.append(f"{k} = ?")
                values.append(v)
            query = f"UPDATE events SET {', '.join(fields)} WHERE id = ?"
            values.append(event_id)
            conn.execute(query, tuple(values))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating event {event_id}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def delete(cls, event_id):
        """
        刪除 Event 記錄
        :param event_id: int
        :return: bool，刪除是否成功
        """
        try:
            conn = cls.get_db_connection()
            conn.execute("DELETE FROM events WHERE id = ?", (event_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting event {event_id}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
