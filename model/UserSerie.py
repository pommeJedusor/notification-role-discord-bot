import os
import sqlite3

from dotenv import load_dotenv

from model.BundleSerie import BundleSerie

load_dotenv()
DATABASE = os.getenv("DATABASE")
if DATABASE is None:
    print("Please set a DATABASE name")
    exit()

conn = sqlite3.connect(DATABASE)


class UserSerie:
    def __init__(
        self,
        server_id: int,
        user_id: int,
        serie_role_id: int,
        has_role: bool,
        bundle_id: int,
    ):
        self.server_id = server_id
        self.user_id = user_id
        self.serie_role_id = serie_role_id
        self.has_role = has_role
        self.bundle_id = bundle_id

    @staticmethod
    def save(
        server_id: int, user_id: int, serie_role_id: int, has_role: bool, bundle_id: int
    ):
        cursor = None
        try:
            sql = "INSERT OR IGNORE INTO user_has_serie(`server_id`, `user_id`, `serie_role_id`, `has_role`, `bundle_id`) VALUES(?,?,?,?,?)"
            cursor = conn.cursor()
            cursor.execute(
                sql, (server_id, user_id, serie_role_id, int(has_role), bundle_id)
            )
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
            sql = "DELETE FROM user_has_serie WHERE `server_id` = ? AND `serie_role_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, serie_role_id))
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
            sql = "DELETE FROM user_has_serie WHERE `server_id` = ? AND `bundle_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, bundle_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def deleteByBundleAndUser(server_id: int, bundle_id: int, user_id: int):
        cursor = None
        try:
            sql = "DELETE FROM user_has_serie WHERE `server_id` = ? AND `bundle_id` = ? AND `user_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, bundle_id, user_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def delete(server_id: int, user_id: int, serie_role_id: int, bundle_id: int):
        cursor = None
        try:
            sql = "DELETE FROM user_has_serie WHERE `server_id` = ? AND `user_id` = ? AND `serie_role_id` = ? AND `bundle_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, user_id, serie_role_id, bundle_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def getUsersAndSeriesByBundle(
        cls, server_id: int, bundle_id: int
    ) -> list[tuple[int, int]]:
        cursor = None
        try:

            sql = "SELECT user_id, serie_role_id FROM user_has_serie WHERE `server_id` = ? AND `bundle_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, bundle_id))
            results = cursor.fetchall()
            assert type(results) is list
            return results
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def getByUser(cls, server_id: int, user_id: int) -> list["UserSerie"]:
        cursor = None
        try:
            sql = "SELECT id, server_id, user_id, serie_role_id, MIN(has_role), bundle_id FROM user_has_serie WHERE `server_id` = ? AND `user_id` = ? GROUP BY serie_role_id"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, user_id))
            results = cursor.fetchall()
            users_series = []
            for result in results:
                id, server_id, user_id, serie_role_id, has_role, bundle_id = result
                users_serie = cls(
                    server_id, user_id, serie_role_id, bool(has_role), bundle_id
                )
                users_series.append(users_serie)
            return users_series
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def getByUserAndBundle(
        cls, server_id: int, user_id: int, bundle_id: int
    ) -> list["UserSerie"]:
        cursor = None
        try:
            sql = "SELECT * FROM user_has_serie WHERE `server_id` = ? AND `user_id` = ? AND `bundle_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, user_id, bundle_id))
            results = cursor.fetchall()
            users_series = []
            for result in results:
                id, server_id, user_id, serie_role_id, has_role, bundle_id = result
                users_serie = cls(
                    server_id, user_id, serie_role_id, bool(has_role), bundle_id
                )
                users_series.append(users_serie)
            return users_series
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def addBundleSeriesToUser(server_id: int, bundle_id: int, user_id: int):
        has_role = True
        rows = [
            (server_id, user_id, serie.serie_role_id, has_role, bundle_id)
            for serie in BundleSerie.getByBundle(server_id, bundle_id)
        ]
        cursor = None
        try:
            sql = "INSERT INTO `user_has_serie`(`server_id`, `user_id`, `serie_role_id`, `has_role`, `bundle_id`) VALUES(?,?,?,?,?);"
            cursor = conn.cursor()
            cursor.executemany(sql, rows)
            conn.commit()
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
                CREATE TABLE IF NOT EXISTS user_has_serie (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    server_id INTEGER,
                    user_id INTEGER,
                    serie_role_id INTEGER,
                    has_role Boolean,
                    bundle_id INTEGER,
                    UNIQUE(server_id, user_id, serie_role_id, bundle_id)
                );
            """
            cursor.execute(sql)

            conn.commit()
        except Exception as e:
            print(f"failed to init the sqlite table Event\n{e}")
            exit()
