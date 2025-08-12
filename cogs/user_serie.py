import discord
from discord import Guild, app_commands
from discord.ext import commands

from model.UserSerie import UserSerie
from model.Permission import Permission


class CogUsersSeries(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
