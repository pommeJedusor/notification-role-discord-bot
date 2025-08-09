import os
import sqlite3
from typing import List

from dotenv import load_dotenv

from model.BundleSerie import BundleSerie
from model.UserBundle import UserBundle
from model.UserSerie import UserSerie

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
    def delete(server_id: int, role_id: int) -> list[tuple[int, int]]:
        """
        return list of tuple: (user_id, serie_id) for each serie that was attributed for a user
        by the bundle so that we can check if we should remove the discord role
        """
        cursor = None
        try:
            sql = "DELETE FROM bundles WHERE `server_id` = ? AND `role_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, role_id))
            conn.commit()
            users_and_series: list[tuple[int, int]] = (
                UserSerie.getUsersAndSeriesByBundle(server_id, role_id)
            )
            UserBundle.deleteByBundle(server_id, role_id)
            UserSerie.deleteByBundle(server_id, role_id)
            return users_and_series
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            BundleSerie.deleteByBundle(server_id, role_id)

    @classmethod
    def getByServerAndRoleId(cls, server_id: int, role_id: int) -> List["Bundle"]:
        cursor = None
        try:
            sql = "SELECT * FROM bundles WHERE `server_id` = ? AND `role_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, role_id))
            results = cursor.fetchall()
            bundles = []
            for result in results:
                id, server_id, role_id, bundle_name, bundle_icon = result
                bundle = cls(server_id, role_id, bundle_name, bundle_icon)
                bundles.append(bundle)
            return bundles
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
            bundles = []
            for result in results:
                id, server_id, role_id, bundle_name, bundle_icon = result
                bundle = cls(server_id, role_id, bundle_name, bundle_icon)
                bundles.append(bundle)
            return bundles
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
            bundles = []
            for result in results:
                id, server_id, role_id, bundle_name, bundle_icon = result
                bundle = cls(server_id, role_id, bundle_name, bundle_icon)
                bundles.append(bundle)
            return bundles
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
            bundles = []
            for result in results:
                id, server_id, role_id, bundle_name, bundle_icon = result
                bundle = cls(server_id, role_id, bundle_name, bundle_icon)
                bundles.append(bundle)
            return bundles
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
