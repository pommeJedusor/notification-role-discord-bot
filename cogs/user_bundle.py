import discord
from discord import Guild, app_commands
from discord.ext import commands

from model.Bundle import Bundle
from model.UserBundle import UserBundle
from model.Permission import Permission
from model.UserSerie import UserSerie


class CogUsersBundles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ajouter_bundle_a_user",
        description="ajoute un bundle à un user",
    )
    async def add_bundle_to_user(
        self,
        interaction: discord.Interaction,
        bundle: discord.Role,
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

        assert type(interaction.guild) is Guild

        if not Bundle.getByServerAndRoleId(interaction.guild.id, bundle.id):
            return await interaction.response.send_message(
                "le role que vous avez entrez ne correspond à aucun bundle",
                ephemeral=True,
            )

        if not user.get_role(bundle.id):
            await user.add_roles(bundle)

        UserBundle.save(interaction.guild.id, user.id, bundle.id)
        UserSerie.addBundleSeriesToUser(interaction.guild.id, bundle.id, user.id)

        # add discord roles for series in bundle
        users_series = UserSerie.getByUserAndBundle(
            interaction.guild.id, user.id, bundle.id
        )
        series = []
        for user_serie in users_series:
            global_user_serie = UserSerie.getByUserAndSerie(
                interaction.guild.id, user.id, user_serie.serie_role_id
            )
            if not global_user_serie or global_user_serie.has_role:
                series.append(interaction.guild.get_role(user_serie.serie_role_id))
        series = [serie for serie in series if serie]
        await user.add_roles(*series)

        await interaction.response.send_message(
            f"le bundle {bundle.name} a été ajouté au user: {user.name}",
        )

    @app_commands.command(
        name="retirer_bundle_du_user",
        description="retire un bundle d'un user",
    )
    async def remove_bundle_from_user(
        self,
        interaction: discord.Interaction,
        bundle: discord.Role,
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

        assert type(interaction.guild) is Guild

        if not Bundle.getByServerAndRoleId(interaction.guild.id, bundle.id):
            return await interaction.response.send_message(
                "le role que vous avez entrez ne correspond à aucun bundle",
                ephemeral=True,
            )

        if user.get_role(bundle.id):
            await user.remove_roles(bundle)

        UserBundle.delete(interaction.guild.id, user.id, bundle.id)
        # check wether he should still have the series and remove the discord role if such
        users_series = UserSerie.getByUserAndBundle(
            interaction.guild.id, user.id, bundle.id
        )
        UserSerie.deleteByBundleAndUser(interaction.guild.id, bundle.id, user.id)
        series = [
            interaction.guild.get_role(user_serie.serie_role_id)
            for user_serie in users_series
            if not UserSerie.getByUserAndSerie(
                interaction.guild.id, user.id, user_serie.serie_role_id
            )
        ]
        series = [serie for serie in series if serie]
        await user.remove_roles(*series)
        await interaction.response.send_message(
            f"le bundle `{bundle.name}` a bien été retiré du user {user.name}",
        )

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
