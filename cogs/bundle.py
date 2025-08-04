import discord
from discord import Guild, app_commands
from discord.ext import commands

from model.Permission import Permission
from model.Bundle import Bundle


class CogBundles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ajouter_bundle",
        description="Créer un bundle dans lequel ajouter des séries",
    )
    async def add_bundle(self, interaction: discord.Interaction, name: str, icon: str):
        if not Permission.is_user_powerfull(interaction):
            return await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )

        assert type(interaction.guild) is Guild
        if Bundle.getByServerAndName(interaction.guild.id, name):
            return await interaction.response.send_message(
                "le rôle existe déjà",
                ephemeral=True,
            )

        role = await interaction.guild.create_role(name=name, mentionable=True)
        Bundle.save(interaction.guild.id, role.id, name, icon)
        # Permission.save(interaction.guild.id, role.id)
        await interaction.response.send_message(
            f"nom: {name}\nicon: {icon}",
        )

    @app_commands.command(
        name="retirer_bundle",
        description="supprime un bundle",
    )
    async def remove_bundle(self, interaction: discord.Interaction, role: discord.Role):
        if not Permission.is_user_powerfull(interaction):
            await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )
            return

        assert type(interaction.guild) is Guild
        Bundle.delete(interaction.guild.id, role.id)
        await role.delete()
        await interaction.response.send_message(
            f"le role `{role.name}` a bien été supprimé",
        )

    @app_commands.command(
        name="voir_bundles",
        description="permet de voir les tous les bundles",
    )
    async def see_bundles(self, interaction: discord.Interaction):
        if not Permission.is_user_powerfull(interaction):
            await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )
            return

        assert type(interaction.guild) is Guild
        bundles = Bundle.getByServer(interaction.guild.id)

        response = "les bundles:\n"
        response += "\n".join(
            [f"- {bundle.bundle_icon} {bundle.bundle_name}" for bundle in bundles]
        )

        await interaction.response.send_message(response)


async def setup(bot):
    await bot.add_cog(CogBundles(bot))
