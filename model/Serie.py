import os
import sqlite3
from typing import List

from dotenv import load_dotenv

from model.BundleSerie import BundleSerie

load_dotenv()
DATABASE = os.getenv("DATABASE")
if DATABASE is None:
    print("Please set a DATABASE name")
    exit()

conn = sqlite3.connect(DATABASE)


class Serie:
    def __init__(self, server_id: int, role_id: int, serie_name: str, serie_icon: str):
        self.id_server = server_id
        self.id_role = role_id
        self.serie_name = serie_name
        self.serie_icon = serie_icon

    @staticmethod
    def save(server_id: int, role_id: int, serie_name: str, serie_icon: str):
        cursor = None
        try:
            sql = "INSERT OR IGNORE INTO series(`server_id`, `role_id`, `serie_name`, `serie_icon`) VALUES(?,?,?,?)"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, role_id, serie_name, serie_icon))
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
            sql = "DELETE FROM series WHERE `server_id` = ? AND `role_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, role_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            BundleSerie.deleteBySerie(server_id, role_id)

    @classmethod
    def getByServerAndName(cls, server_id: int, serie_name: str) -> List["Serie"]:
        cursor = None
        try:
            sql = "SELECT * FROM series WHERE `server_id` = ? AND `serie_name` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, serie_name))
            results = cursor.fetchall()
            series = []
            for result in results:
                id, server_id, role_id, serie_name, serie_icon = result
                serie = cls(server_id, role_id, serie_name, serie_icon)
                series.append(serie)
            return series
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def getByServerAndRoleId(cls, server_id: int, role_id: int) -> List["Serie"]:
        cursor = None
        try:
            sql = "SELECT * FROM series WHERE `server_id` = ? AND `role_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, role_id))
            results = cursor.fetchall()
            series = []
            for result in results:
                id, server_id, role_id, serie_name, serie_icon = result
                serie = cls(server_id, role_id, serie_name, serie_icon)
                series.append(serie)
            return series
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def getByServer(cls, server_id: int) -> List["Serie"]:
        cursor = None
        try:
            sql = "SELECT * FROM series WHERE `server_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id,))
            results = cursor.fetchall()
            series = []
            for result in results:
                id, server_id, role_id, serie_name, serie_icon = result
                serie = cls(server_id, role_id, serie_name, serie_icon)
                series.append(serie)
            return series
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def getAll(cls) -> List["Serie"]:
        cursor = None
        try:
            sql = "SELECT * FROM series"
            cursor = conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            series = []
            for result in results:
                id, server_id, role_id, serie_name, serie_icon = result
                serie = cls(server_id, role_id, serie_name, serie_icon)
                series.append(serie)
            return series
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
                CREATE TABLE IF NOT EXISTS series (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    server_id INTEGER,
                    role_id INTEGER,
                    serie_name TEXT UNIQUE,
                    serie_icon TEXT UNIQUE,
                    UNIQUE(server_id, role_id)
                );
            """
            cursor.execute(sql)

            conn.commit()
        except Exception as e:
            print(f"failed to init the sqlite table Event\n{e}")
            exit()
