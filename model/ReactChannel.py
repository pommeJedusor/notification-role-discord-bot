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


class ReactChannel:
    def __init__(self, server_id: int, channel_id: int):
        self.id_server = server_id
        self.channel_id = channel_id

    @staticmethod
    def save(server_id: int, channel_id: int):
        cursor = None
        try:
            sql = "INSERT OR IGNORE INTO react_channels(`server_id`, `channel_id`) VALUES(?,?)"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, channel_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def deleteByServer(server_id: int):
        cursor = None
        try:
            sql = "DELETE FROM react_channels WHERE `server_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id,))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def getByServer(cls, server_id: int) -> List["ReactChannel"]:
        cursor = None
        try:
            sql = "SELECT * FROM react_channels WHERE `server_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id,))
            results = cursor.fetchall()
            permissions = []
            for result in results:
                id, server_id, channel_id = result
                permission = cls(
                    server_id,
                    channel_id,
                )
                permissions.append(permission)
            return permissions
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def getAll(cls) -> List["ReactChannel"]:
        cursor = None
        try:
            sql = "SELECT * FROM react_channels"
            cursor = conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            permissions = []
            for result in results:
                id, server_id, channel_id = result
                permission = cls(
                    server_id,
                    channel_id,
                )
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
                CREATE TABLE IF NOT EXISTS react_channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    server_id INTEGER,
                    channel_id INTEGER,
                    UNIQUE(server_id, channel_id)
                );
            """
            cursor.execute(sql)

            conn.commit()
        except Exception as e:
            print(f"failed to init the sqlite table Event\n{e}")
            exit()
