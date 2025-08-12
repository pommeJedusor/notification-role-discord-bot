from typing import Optional
import discord
from discord import Guild, app_commands
from discord.ext import commands

from cogs import react_channel
from model.Bundle import Bundle
from model.Permission import Permission
from model.Serie import Serie
from model.UserSerie import UserSerie


class CogSeries(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ajouter_serie",
        description="Créer un serie dans lequel ajouter des séries",
    )
    async def add_serie(
        self,
        interaction: discord.Interaction,
        name: str,
        icon: str,
        role: Optional[discord.Role],
    ):
        if not Permission.is_user_powerfull(interaction):
            return await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )

        assert type(interaction.guild) is Guild
        if Serie.getByServerAndName(interaction.guild.id, name):
            return await interaction.response.send_message(
                "la série existe déjà",
                ephemeral=True,
            )
        if role and Serie.getByServerAndRoleId(interaction.guild.id, role.id):
            return await interaction.response.send_message(
                "le role est déjà utilisé pour une série",
                ephemeral=True,
            )
        if role and Bundle.getByServerAndRoleId(interaction.guild.id, role.id):
            return await interaction.response.send_message(
                "le role est déjà utilisé pour un bundle",
                ephemeral=True,
            )

        if not role:
            role = await interaction.guild.create_role(name=name, mentionable=True)
        Serie.save(interaction.guild.id, role.id, name, icon)
        await interaction.response.send_message(
            f"nom: {name}\nicon: {icon}",
        )
        await react_channel.actualise_role_messages(self.bot, interaction.guild.id)

    @app_commands.command(
        name="retirer_serie",
        description="supprime un serie",
    )
    async def remove_serie(self, interaction: discord.Interaction, role: discord.Role):
        if not Permission.is_user_powerfull(interaction):
            return await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )

        assert type(interaction.guild) is Guild

        if not Serie.getByServerAndRoleId(interaction.guild.id, role.id):
            return await interaction.response.send_message(
                "le role ne correspond à aucune série",
                ephemeral=True,
            )

        Serie.delete(interaction.guild.id, role.id)
        UserSerie.deleteBySerie(interaction.guild.id, role.id)
        await role.delete()
        await interaction.response.send_message(
            f"le role `{role.name}` a bien été supprimé",
        )
        await react_channel.actualise_role_messages(self.bot, interaction.guild.id)

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
