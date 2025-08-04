import discord
from discord import Guild, app_commands
from discord.ext import commands

from model.Permission import Permission
from model.Serie import Serie


class CogSeries(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ajouter_serie",
        description="Créer un serie dans lequel ajouter des séries",
    )
    async def add_serie(self, interaction: discord.Interaction, name: str, icon: str):
        if not Permission.is_user_powerfull(interaction):
            return await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )

        assert type(interaction.guild) is Guild
        if Serie.getByServerAndName(interaction.guild.id, name):
            return await interaction.response.send_message(
                "le rôle existe déjà",
                ephemeral=True,
            )

        role = await interaction.guild.create_role(name=name, mentionable=True)
        Serie.save(interaction.guild.id, role.id, name, icon)
        # Permission.save(interaction.guild.id, role.id)
        await interaction.response.send_message(
            f"nom: {name}\nicon: {icon}",
        )

    @app_commands.command(
        name="retirer_serie",
        description="supprime un serie",
    )
    async def remove_serie(self, interaction: discord.Interaction, role: discord.Role):
        if not Permission.is_user_powerfull(interaction):
            await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )
            return

        assert type(interaction.guild) is Guild
        Serie.delete(interaction.guild.id, role.id)
        await role.delete()
        await interaction.response.send_message(
            f"le role `{role.name}` a bien été supprimé",
        )

    @app_commands.command(
        name="voir_series",
        description="permet de voir les tous les series",
    )
    async def see_series(self, interaction: discord.Interaction):
        if not Permission.is_user_powerfull(interaction):
            await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )
            return

        assert type(interaction.guild) is Guild
        series = Serie.getByServer(interaction.guild.id)

        response = "les series:\n"
        response += "\n".join(
            [f"- {serie.serie_icon} {serie.serie_name}" for serie in series]
        )

        await interaction.response.send_message(response)


async def setup(bot):
    await bot.add_cog(CogSeries(bot))
