import os
from discord.ext import commands
from dotenv import load_dotenv

import discord

from model.ReactChannel import ReactChannel

if not os.path.exists("db"):
    os.makedirs("db")

from model.Bundle import Bundle
from model.BundleSerie import BundleSerie
from model.Permission import Permission
from model.Serie import Serie
from model.UserSerie import UserSerie
from model.UserBundle import UserBundle


load_dotenv()
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("Please set a TOKEN")
    exit()


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


def startup():
    Permission.init()
    Bundle.init()
    Serie.init()
    BundleSerie.init()
    UserSerie.init()
    UserBundle.init()
    ReactChannel.init()


@bot.event
async def on_ready():
    try:
        # load all files in the cogs directory
        cogs_path = os.getcwd() + "/cogs"
        cogs_files = [
            file[:-3] for file in os.listdir(cogs_path) if file.endswith(".py")
        ]
        for cogs_file in cogs_files:
            await bot.load_extension(f"cogs.{cogs_file}")

        synced = await bot.tree.sync()
        print(f"synced {len(synced) } command(s)")
    except Exception as e:
        print("an error as occured:", e)


@bot.tree.error
async def on_error(
    interaction: discord.Interaction[discord.Client],
    error: discord.app_commands.AppCommandError | Exception,
) -> None:
    await interaction.response.send_message(f"```\n{error}\n```")


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if len(before.roles) == len(after.roles):
        return
    previous_roles = set([role.id for role in before.roles])
    new_roles = set([role.id for role in after.roles])
    if len(before.roles) > len(after.roles):
        for role in new_roles:
            previous_roles.remove(role)
        removed_role = previous_roles.pop()
        serie_of_role = Serie.getByServerAndRoleId(before.guild.id, removed_role)
        bundle_of_role = Bundle.getByServerAndRoleId(before.guild.id, removed_role)
        if not serie_of_role and not bundle_of_role:
            return
        if bundle_of_role:
            UserBundle.delete(before.guild.id, before.id, bundle_of_role.id_role)
            # check wether he should still have the series and remove the discord role if such
            users_series = UserSerie.getByUserAndBundle(
                before.guild.id, before.id, bundle_of_role.id_role
            )
            UserSerie.deleteByBundleAndUser(
                before.guild.id, bundle_of_role.id_role, before.id
            )
            series = [
                before.guild.get_role(user_serie.serie_role_id)
                for user_serie in users_series
                if not UserSerie.getByUserAndSerie(
                    before.guild.id, before.id, user_serie.serie_role_id
                )
            ]
            series = [serie for serie in series if serie]
            await after.remove_roles(*series)
        elif serie_of_role:
            UserSerie.delete(before.guild.id, before.id, serie_of_role.id_role, 0)
            user_serie = UserSerie.getByUserAndSerie(
                before.guild.id, before.id, serie_of_role.id_role
            )
            if user_serie:
                UserSerie.save(
                    before.guild.id, before.id, serie_of_role.id_role, False, 0
                )

    elif len(before.roles) < len(after.roles):
        for role in previous_roles:
            new_roles.remove(role)
        added_role = new_roles.pop()
        serie_of_role = Serie.getByServerAndRoleId(before.guild.id, added_role)
        bundle_of_role = Bundle.getByServerAndRoleId(before.guild.id, added_role)
        if serie_of_role:
            if not Serie.getByServerAndRoleId(before.guild.id, serie_of_role.id_role):
                return

            UserSerie.delete(before.guild.id, before.id, serie_of_role.id_role, 0)
            UserSerie.save(before.guild.id, before.id, serie_of_role.id_role, True, 0)
        elif bundle_of_role:
            if not Bundle.getByServerAndRoleId(before.guild.id, bundle_of_role.id_role):
                return

            UserBundle.save(before.guild.id, before.id, bundle_of_role.id_role)
            UserSerie.addBundleSeriesToUser(
                before.guild.id, bundle_of_role.id_role, before.id
            )

            # add discord roles for series in bundle
            users_series = UserSerie.getByUserAndBundle(
                before.guild.id, before.id, bundle_of_role.id_role
            )
            series = []
            for user_serie in users_series:
                global_user_serie = UserSerie.getByUserAndSerie(
                    before.guild.id, before.id, user_serie.serie_role_id
                )
                if not global_user_serie or global_user_serie.has_role:
                    series.append(before.guild.get_role(user_serie.serie_role_id))
            series = [serie for serie in series if serie]
            await before.add_roles(*series)


startup()
bot.run(TOKEN)
