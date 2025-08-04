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


class Bundle:
    def __init__(
        self, server_id: int, role_id: int, bundle_name: str, bundle_icon: str
    ):
        self.id_server = server_id
        self.id_role = role_id
        self.bundle_name = bundle_name
        self.bundle_icon = bundle_icon

    @staticmethod
    def save(server_id: int, role_id: int, bundle_name: str, bundle_icon: str):
        cursor = None
        try:
            sql = "INSERT OR IGNORE INTO bundles(`server_id`, `role_id`, `bundle_name`, `bundle_icon`) VALUES(?,?,?,?)"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, role_id, bundle_name, bundle_icon))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def delete(server_id: int, role_id: int):
        cursor = None
        try:
            sql = "DELETE FROM bundles WHERE `server_id` = ? AND `role_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, role_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def getByServerAndName(cls, server_id: int, bundle_name: str) -> List["Bundle"]:
        cursor = None
        try:
            sql = "SELECT * FROM bundles WHERE `server_id` = ? AND `bundle_name` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, bundle_name))
            results = cursor.fetchall()
            permissions = []
            for result in results:
                id, server_id, role_id, bundle_name, bundle_icon = result
                permission = cls(server_id, role_id, bundle_name, bundle_icon)
                permissions.append(permission)
            return permissions
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def getByServer(cls, server_id: int) -> List["Bundle"]:
        cursor = None
        try:
            sql = "SELECT * FROM bundles WHERE `server_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id,))
            results = cursor.fetchall()
            permissions = []
            for result in results:
                id, server_id, role_id, bundle_name, bundle_icon = result
                permission = cls(server_id, role_id, bundle_name, bundle_icon)
                permissions.append(permission)
            return permissions
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def getAll(cls) -> List["Bundle"]:
        cursor = None
        try:
            sql = "SELECT * FROM bundles"
            cursor = conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            permissions = []
            for result in results:
                id, server_id, role_id, bundle_name, bundle_icon = result
                permission = cls(server_id, role_id, bundle_name, bundle_icon)
                permissions.append(permission)
            return permissions
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
                CREATE TABLE IF NOT EXISTS bundles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    server_id INTEGER,
                    role_id INTEGER,
                    bundle_name TEXT UNIQUE,
                    bundle_icon TEXT UNIQUE,
                    UNIQUE(server_id, role_id)
                );
            """
            cursor.execute(sql)

            conn.commit()
        except Exception as e:
            print(f"failed to init the sqlite table Event\n{e}")
            exit()
