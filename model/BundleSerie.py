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


class BundleSerie:
    def __init__(self, server_id: int, bundle_role_id: int, serie_role_id: int):
        self.server_id = server_id
        self.bundle_role_id = bundle_role_id
        self.serie_role_id = serie_role_id

    @staticmethod
    def save(server_id: int, bundle_role_id: int, serie_role_id: int):
        cursor = None
        try:
            sql = "INSERT OR IGNORE INTO bundle_has_serie(`server_id`, `bundle_role_id`, `serie_role_id`) VALUES(?,?,?)"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, bundle_role_id, serie_role_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def deleteBySerie(server_id: int, serie_role_id: int):
        cursor = None
        try:
            sql = "DELETE FROM bundle_has_serie WHERE `server_id` = ? AND `serie_role_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, serie_role_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def deleteByBundle(server_id: int, bundle_role_id: int):
        cursor = None
        try:
            sql = "DELETE FROM bundle_has_serie WHERE `server_id` = ? AND `bundle_role_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, bundle_role_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def delete(server_id: int, bundle_role_id: int, serie_role_id: int):
        cursor = None
        try:
            sql = "DELETE FROM bundle_has_serie WHERE `server_id` = ? AND `bundle_role_id` = ? AND `serie_role_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, bundle_role_id, serie_role_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def getByBundle(cls, server_id: int, bundle_role_id: int) -> List["BundleSerie"]:
        cursor = None
        try:
            sql = "SELECT * FROM bundle_has_serie WHERE `server_id` = ? AND `bundle_role_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, bundle_role_id))
            results = cursor.fetchall()
            bundles_series = []
            for result in results:
                id, server_id, bundle_role_id, serie_role_id = result
                bundles_serie = cls(server_id, bundle_role_id, serie_role_id)
                bundles_series.append(bundles_serie)
            return bundles_series
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
                CREATE TABLE IF NOT EXISTS bundle_has_serie (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    server_id INTEGER,
                    bundle_role_id INTEGER,
                    serie_role_id INTEGER,
                    UNIQUE(server_id, bundle_role_id, serie_role_id)
                );
            """
            cursor.execute(sql)

            conn.commit()
        except Exception as e:
            print(f"failed to init the sqlite table Event\n{e}")
            exit()
