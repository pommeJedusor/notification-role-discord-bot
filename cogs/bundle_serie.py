import discord
from discord import Guild, app_commands
from discord.ext import commands

from model.BundleSerie import BundleSerie
from model.Permission import Permission


class CogBundlesSeries(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ajouter_serie_a_bundle",
        description="ajoute une série à un bundle",
    )
    async def add_serie_to_bundle(
        self,
        interaction: discord.Interaction,
        serie: discord.Role,
        bundle: discord.Role,
    ):
        if not Permission.is_user_powerfull(interaction):
            return await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )

        assert type(interaction.guild) is Guild

        BundleSerie.save(interaction.guild.id, bundle.id, serie.id)
        # TODO add serie to all users that have the bundle
        await interaction.response.send_message(
            f"la série {serie.name} a été ajouté au bundle: {bundle.name}",
        )

    @app_commands.command(
        name="retirer_serie_du_bundle",
        description="retire une série d'un bundle",
    )
    async def remove_serie_from_bundle(
        self,
        interaction: discord.Interaction,
        serie: discord.Role,
        bundle: discord.Role,
    ):
        if not Permission.is_user_powerfull(interaction):
            await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )
            return

        assert type(interaction.guild) is Guild
        BundleSerie.delete(interaction.guild.id, bundle.id, serie.id)
        # TODO remove serie from bundle to all users that have the bundle but not the series
        await interaction.response.send_message(
            f"la série `{serie.name}` a bien été retiré du bundle {bundle.name}",
        )


async def setup(bot):
    await bot.add_cog(CogBundlesSeries(bot))
