from typing import Optional
import discord
from discord import Guild, app_commands
from discord.ext import commands

from cogs import react_channel
from model.Permission import Permission
from model.Bundle import Bundle
from model.Serie import Serie
from model.UserBundle import UserBundle


class CogBundles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ajouter_bundle",
        description="Créer un bundle dans lequel ajouter des séries",
    )
    async def add_bundle(
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
        if Bundle.getByServerAndName(interaction.guild.id, name):
            return await interaction.response.send_message(
                "le bundle existe déjà",
                ephemeral=True,
            )

        if not role:
            role = await interaction.guild.create_role(name=name, mentionable=True)
        elif Serie.getByServerAndRoleId(
            interaction.guild.id, role.id
        ) or Bundle.getByServerAndRoleId(interaction.guild.id, role.id):
            return await interaction.response.send_message(
                "le rôle est déjà utilisé pour une série ou bundle",
                ephemeral=True,
            )
        Bundle.save(interaction.guild.id, role.id, name, icon)
        await interaction.response.send_message(
            f"nom: {name}\nicon: {icon}",
        )
        await react_channel.actualise_role_messages(self.bot, interaction.guild.id)

    @app_commands.command(
        name="retirer_bundle",
        description="supprime un bundle",
    )
    async def remove_bundle(self, interaction: discord.Interaction, role: discord.Role):
        if not Permission.is_user_powerfull(interaction):
            return await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )

        assert type(interaction.guild) is Guild

        if not Bundle.getByServerAndRoleId(interaction.guild.id, role.id):
            return await interaction.response.send_message(
                "le rôle ne correspond à aucun bundle",
                ephemeral=True,
            )

        Bundle.delete(interaction.guild.id, role.id)
        UserBundle.deleteByBundle(interaction.guild.id, role.id)
        await role.delete()
        await interaction.response.send_message(
            f"le role `{role.name}` a bien été supprimé",
        )
        await react_channel.actualise_role_messages(self.bot, interaction.guild.id)

    @app_commands.command(
        name="voir_bundles",
        description="permet de voir les tous les bundles",
    )
    async def see_bundles(self, interaction: discord.Interaction):
        if not Permission.is_user_powerfull(interaction):
            return await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )

        assert type(interaction.guild) is Guild
        bundles = Bundle.getByServer(interaction.guild.id)

        response = "les bundles:\n"
        response += "\n".join(
            [f"- {bundle.bundle_icon} {bundle.bundle_name}" for bundle in bundles]
        )

        await interaction.response.send_message(response)


async def setup(bot):
    await bot.add_cog(CogBundles(bot))
