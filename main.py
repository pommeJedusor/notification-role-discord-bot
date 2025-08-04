import os
from discord.ext import commands
from dotenv import load_dotenv

import discord

from model.Permission import Permission


if not os.path.exists("db"):
    os.makedirs("db")


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


startup()
bot.run(TOKEN)
