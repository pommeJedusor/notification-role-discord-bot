import discord
from discord import Guild, Role, app_commands
from discord.ext import commands

from model.Permission import Permission


class CogPermissions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ajouter_permission",
        description="rend un rôle capable d'effectuer toute action sur ce bot",
    )
    async def add_permission(
        self, interaction: discord.Interaction, role: discord.Role
    ):
        if not Permission.is_user_powerfull(interaction):
            await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )
            return

        assert type(interaction.guild) is Guild
        Permission.save(interaction.guild.id, role.id)
        await interaction.response.send_message(
            f"tout ceux ayant le role `{role.name}` sont désormais capables d'intéragir avec le bot en toute libértée",
        )

    @app_commands.command(
        name="retirer_permission",
        description="retire à un rôle la capacité d'effectuer toute action sur ce bot",
    )
    async def remove_permission(
        self, interaction: discord.Interaction, role: discord.Role
    ):
        if not Permission.is_user_powerfull(interaction):
            await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )
            return

        assert type(interaction.guild) is Guild
        Permission.delete(interaction.guild.id, role.id)
        await interaction.response.send_message(
            f"le role `{role.name}` n'est désormais plus suffisant pour effectuer toute action sur ce bot",
        )

    @app_commands.command(
        name="voir_permission",
        description="permet de voir les roles pouvant effectuer toute action sur ce bot",
    )
    async def see_permissions(self, interaction: discord.Interaction):
        if not Permission.is_user_powerfull(interaction):
            await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )
            return

        assert type(interaction.guild) is Guild
        permissions = Permission.getByServer(interaction.guild.id)

        roles: list[Role] = []
        for permission in permissions:
            role = interaction.guild.get_role(permission.id_role)
            if role == None:
                Permission.delete(interaction.guild.id, permission.id_role)
            else:
                roles.append(role)
        response = "les roles pouvant effectuer toute action sur ce bot sont:\n"
        response += "\n".join([f"- {role.name}" for role in roles])

        await interaction.response.send_message(response)


async def setup(bot):
    await bot.add_cog(CogPermissions(bot))
