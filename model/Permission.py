import os
import sqlite3
from typing import List

import discord
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE")
if DATABASE is None:
    print("Please set a DATABASE name")
    exit()

conn = sqlite3.connect(DATABASE)


class Permission:
    def __init__(self, server_id: int, role_id: int):
        self.id_server = server_id
        self.id_role = role_id

    @classmethod
    def is_user_powerfull(cls, interaction: discord.Interaction) -> bool:
        if type(interaction.user) is not discord.Member:
            raise Exception("user is not member")
        if interaction.guild == None:
            raise Exception("guild not found")

        if interaction.guild.owner_id == interaction.user.id:
            return True

        powerfull_id_roles = [
            perm.id_role for perm in cls.getByServer(interaction.guild.id)
        ]
        for role in interaction.user.roles:
            if role.id in powerfull_id_roles:
                return True

        return False

    @staticmethod
    def save(server_id: int, role_id: int):
        cursor = None
        try:
            sql = "INSERT OR IGNORE INTO perms(`server_id`, `role_id`) VALUES(?,?)"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, role_id))
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
            sql = "DELETE FROM perms WHERE `server_id` = ? AND `role_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id, role_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getByServer(server_id: int) -> List["Permission"]:
        cursor = None
        try:
            sql = "SELECT * FROM perms WHERE `server_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (server_id,))
            results = cursor.fetchall()
            permissions = []
            for result in results:
                id, server_id, role_id = result
                permission = Permission(
                    server_id,
                    role_id,
                )
                permissions.append(permission)
            return permissions
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getAll() -> List["Permission"]:
        cursor = None
        try:
            sql = "SELECT * FROM perms"
            cursor = conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            permissions = []
            for result in results:
                id, server_id, role_id = result
                permission = Permission(
                    server_id,
                    role_id,
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
                CREATE TABLE IF NOT EXISTS perms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    server_id INTEGER,
                    role_id INTEGER,
                    UNIQUE(server_id, role_id)
                );
            """
            cursor.execute(sql)

            conn.commit()
        except Exception as e:
            print(f"failed to init the sqlite table Event\n{e}")
            exit()
