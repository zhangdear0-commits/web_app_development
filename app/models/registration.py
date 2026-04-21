import sqlite3
import os

class Registration:
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
        新增一筆 Registration 記錄
        :param data: dict，包含 event_id, user_id, status, custom_form_data, qr_code_token, created_at
        :return: int，新增記錄的 id，若失敗則回傳 None
        """
        try:
            conn = cls.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO registrations 
                (event_id, user_id, status, custom_form_data, qr_code_token, created_at) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                (data['event_id'], data['user_id'], data['status'], data.get('custom_form_data'), 
                 data.get('qr_code_token'), data['created_at'])
            )
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        except Exception as e:
            print(f"Error creating registration: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def get_all(cls):
        """
        取得所有 Registration 記錄
        :return: list of sqlite3.Row，若失敗則回傳空陣列
        """
        try:
            conn = cls.get_db_connection()
            rows = conn.execute("SELECT * FROM registrations").fetchall()
            return rows
        except Exception as e:
            print(f"Error fetching all registrations: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def get_by_id(cls, registration_id):
        """
        取得單筆 Registration 記錄
        :param registration_id: int
        :return: sqlite3.Row 或是 None
        """
        try:
            conn = cls.get_db_connection()
            row = conn.execute("SELECT * FROM registrations WHERE id = ?", (registration_id,)).fetchone()
            return row
        except Exception as e:
            print(f"Error fetching registration {registration_id}: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def update(cls, registration_id, data):
        """
        更新 Registration 記錄
        :param registration_id: int
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
            query = f"UPDATE registrations SET {', '.join(fields)} WHERE id = ?"
            values.append(registration_id)
            conn.execute(query, tuple(values))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating registration {registration_id}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def delete(cls, registration_id):
        """
        刪除 Registration 記錄
        :param registration_id: int
        :return: bool，刪除是否成功
        """
        try:
            conn = cls.get_db_connection()
            conn.execute("DELETE FROM registrations WHERE id = ?", (registration_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting registration {registration_id}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
