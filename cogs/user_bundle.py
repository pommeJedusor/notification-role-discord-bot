import discord
from discord import Guild, app_commands
from discord.ext import commands

from model.UserBundle import UserBundle
from model.Permission import Permission


class CogUsersBundles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="voir_bundles_utilisateur",
        description="montre les bundles d'un utilisateur",
    )
    async def see_bundle_for_user(
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

        bundles = UserBundle.getByUser(interaction.guild.id, user.id)
        result = "les bundles sont:"
        for bundle in bundles:
            result += f"\nbundle_id: {bundle.bundle_id}"
        await interaction.response.send_message(result)


async def setup(bot):
    await bot.add_cog(CogUsersBundles(bot))
