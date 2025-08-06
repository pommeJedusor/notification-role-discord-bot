import discord
from discord import Guild, app_commands
from discord.ext import commands

from model.UserSerie import UserSerie
from model.Permission import Permission


class CogUsersSeries(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ajouter_serie_a_user",
        description="ajoute une série à un user",
    )
    async def add_serie_to_user(
        self,
        interaction: discord.Interaction,
        serie: discord.Role,
        user: discord.Member,
    ):
        if (
            not Permission.is_user_powerfull(interaction)
            and not user.id == interaction.user.id
        ):
            return await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )
        # TODO check if role is in the bot

        assert type(interaction.guild) is Guild
        if not user.get_role(serie.id):
            await user.add_roles(serie)

        UserSerie.delete(interaction.guild.id, user.id, serie.id, 0)
        UserSerie.save(interaction.guild.id, user.id, serie.id, True, 0)
        await interaction.response.send_message(
            f"la série {serie.name} a été ajouté au user: {user.name}",
        )

    @app_commands.command(
        name="retirer_serie_du_user",
        description="retire une série d'un user",
    )
    async def remove_serie_from_user(
        self,
        interaction: discord.Interaction,
        serie: discord.Role,
        user: discord.Member,
    ):
        if (
            not Permission.is_user_powerfull(interaction)
            and not user.id == interaction.user.id
        ):
            return await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )
        # TODO check if role is in the bot

        assert type(interaction.guild) is Guild
        if user.get_role(serie.id):
            await user.remove_roles(serie)

        UserSerie.delete(interaction.guild.id, user.id, serie.id, 0)
        await interaction.response.send_message(
            f"la série `{serie.name}` a bien été retiré du user {user.name}",
        )

    @app_commands.command(
        name="desactiver_serie_pour_user",
        description="empêche un utilisateur d'avoir une série même s'il a un bundle qui l'inclut",
    )
    async def disable_serie_for_user(
        self,
        interaction: discord.Interaction,
        serie: discord.Role,
        user: discord.Member,
    ):
        if (
            not Permission.is_user_powerfull(interaction)
            and not user.id == interaction.user.id
        ):
            return await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )
        # TODO check if role is in the bot

        assert type(interaction.guild) is Guild
        if user.get_role(serie.id):
            await user.remove_roles(serie)

        UserSerie.delete(interaction.guild.id, user.id, serie.id, 0)
        UserSerie.save(interaction.guild.id, user.id, serie.id, False, 0)
        await interaction.response.send_message(
            f"la série `{serie.name}` a bien été désactivé pour l'utilisateur {user.name}",
        )

    @app_commands.command(
        name="voir_series_utilisateur",
        description="montre les séries d'un utilisateur",
    )
    async def see_serie_for_user(
        self, interaction: discord.Interaction, user: discord.User
    ):
        if (
            not Permission.is_user_powerfull(interaction)
            and not user.id == interaction.user.id
        ):
            await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )
            return

        assert type(interaction.guild) is Guild
        series = UserSerie.getByUser(interaction.guild.id, user.id)
        result = "les séries sont:"
        for serie in series:
            result += f"\nserie_id: {serie.serie_role_id}, has_role: {serie.has_role}"
        await interaction.response.send_message(result)


async def setup(bot):
    await bot.add_cog(CogUsersSeries(bot))
