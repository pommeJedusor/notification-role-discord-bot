import os
import sqlite3
from typing import List

from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE")
if DATABASE is None:
    print("Please set a DATABASE name")
    exit()

conn = sqlite3.connect(DATABASE)


class UserBundle:
    def __init__(
        self,
        server_id: int,
        user_id: int,
        bundle_id: int,
    ):
        self.server_id = server_id
        self.user_id = user_id
        self.bundle_id = bundle_id

    @staticmethod
    def save(
        server_id: int,
        user_id: int,
        bundle_id: int,
    ):
        cursor = None
        try:
            sql = "INSERT OR IGNORE INTO user_has_bundle(`server_id`, `user_id`, `bundle_id`) VALUES(?,?,?)"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, user_id, bundle_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def deleteByBundle(server_id: int, bundle_id: int):
        cursor = None
        try:
            sql = (
                "DELETE FROM user_has_bundle WHERE `server_id` = ? AND `bundle_id` = ?"
            )
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, bundle_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def delete(server_id: int, user_id: int, bundle_id: int):
        cursor = None
        try:
            sql = "DELETE FROM user_has_bundle WHERE `server_id` = ? AND `user_id` = ? AND `bundle_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, user_id, bundle_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def getByUser(cls, server_id: int, user_id: int) -> List["UserBundle"]:
        cursor = None
        try:
            sql = (
                "SELECT * FROM user_has_bundle WHERE `server_id` = ? AND `user_id` = ?"
            )
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, user_id))
            results = cursor.fetchall()
            users_bundles = []
            for result in results:
                id, server_id, user_id, bundle_id = result
                user_bundles = cls(server_id, user_id, bundle_id)
                users_bundles.append(user_bundles)
            return users_bundles
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def getByBundle(cls, server_id: int, bundle_id: int) -> List["UserBundle"]:
        cursor = None
        try:
            sql = "SELECT * FROM user_has_bundle WHERE `server_id` = ? AND `bundle_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, bundle_id))
            results = cursor.fetchall()
            users_bundles = []
            for result in results:
                id, server_id, user_id, bundle_id = result
                user_bundles = cls(server_id, user_id, bundle_id)
                users_bundles.append(user_bundles)
            return users_bundles
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def init():
        try:
            cursor = conn.cursor()
            sql = """
                CREATE TABLE IF NOT EXISTS user_has_bundle (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    server_id INTEGER,
                    user_id INTEGER,
                    bundle_id INTEGER,
                    UNIQUE(server_id, user_id, bundle_id)
                );
            """
            cursor.execute(sql)

            conn.commit()
        except Exception as e:
            print(f"failed to init the sqlite table Event\n{e}")
            exit()
