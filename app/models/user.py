import sqlite3
import os

class User:
    @staticmethod
    def get_db_connection():
        """
        取得 SQLite 資料庫連線，並設定 row_factory 以便用欄位名稱存取與操作。
        """
        db_path = os.path.join(os.getcwd(), 'instance', 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, data):
        """
        新增一筆 User 記錄
        :param data: dict，包含 email, password_hash, name, role, phone, created_at
        :return: int，新增記錄的 id，若失敗則回傳 None
        """
        try:
            conn = cls.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (email, password_hash, name, role, phone, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (data['email'], data['password_hash'], data['name'], data['role'], data.get('phone'), data['created_at'])
            )
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def get_all(cls):
        """
        取得所有 User 記錄
        :return: list of sqlite3.Row，若失敗則回傳空陣列
        """
        try:
            conn = cls.get_db_connection()
            rows = conn.execute("SELECT * FROM users").fetchall()
            return rows
        except Exception as e:
            print(f"Error fetching all users: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def get_by_id(cls, user_id):
        """
        取得單筆 User 記錄
        :param user_id: int
        :return: sqlite3.Row 或是 None
        """
        try:
            conn = cls.get_db_connection()
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return row
        except Exception as e:
            print(f"Error fetching user {user_id}: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def update(cls, user_id, data):
        """
        更新 User 記錄
        :param user_id: int
        :param data: dict，包含欲更新的欄位
        :return: bool，更新是否成功
        """
        try:
            conn = cls.get_db_connection()
            fields = []
            values = []
            for k, v in data.items():
                fields.append(f"{k} = ?")
                values.append(v)
            query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
            values.append(user_id)
            conn.execute(query, tuple(values))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating user {user_id}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def delete(cls, user_id):
        """
        刪除 User 記錄
        :param user_id: int
        :return: bool，刪除是否成功
        """
        try:
            conn = cls.get_db_connection()
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting user {user_id}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
