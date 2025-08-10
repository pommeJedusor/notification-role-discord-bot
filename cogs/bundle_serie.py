import discord
from discord import Guild, app_commands
from discord.ext import commands

from model.BundleSerie import BundleSerie
from model.Serie import Serie
from model.UserBundle import UserBundle
from model.Permission import Permission
from model.UserSerie import UserSerie


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

        # add the series of the bundle for all users that have the bundle
        user_bundles = UserBundle.getByBundle(interaction.guild.id, bundle.id)
        bundle_series = BundleSerie.getByBundle(interaction.guild.id, bundle.id)
        for user_bundle in user_bundles:
            UserSerie.addBundleSeriesToUser(
                interaction.guild.id, bundle.id, user_bundle.user_id
            )

            member = interaction.guild.get_member(user_bundle.user_id)
            roles = [
                interaction.guild.get_role(bundle_serie.serie_role_id)
                for bundle_serie in bundle_series
            ]
            roles = [role for role in roles if role]
            if member:
                await member.add_roles(*roles)

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
        users_series = UserSerie.getUsersAndSeriesByBundle(
            interaction.guild.id, bundle.id
        )
        UserSerie.deleteByBundle(interaction.guild.id, bundle.id)
        for user_id, serie_id in users_series:
            member = interaction.guild.get_member(user_id)
            if not member:
                continue
            user_series = UserSerie.getByUser(interaction.guild.id, user_id)
            user_series = [user.serie_role_id for user in user_series]
            if not serie_id in user_series:
                role = interaction.guild.get_role(serie_id)
                if not role:
                    continue
                await member.remove_roles(role)

        await interaction.response.send_message(
            f"la série `{serie.name}` a bien été retiré du bundle {bundle.name}",
        )

    @app_commands.command(
        name="voir_bundle_series",
        description="permet de voir les tous les series d'un bundle",
    )
    async def see_series_of_bundle(
        self, interaction: discord.Interaction, bundle_role: discord.Role
    ):
        if not Permission.is_user_powerfull(interaction):
            await interaction.response.send_message(
                "vous n'avez pas les permissions requises pour effectuer cette action",
                ephemeral=True,
            )
            return

        assert type(interaction.guild) is Guild
        bundles_series = BundleSerie.getByBundle(interaction.guild.id, bundle_role.id)
        series = [
            Serie.getByServerAndRoleId(interaction.guild.id, bundle_serie.serie_role_id)
            for bundle_serie in bundles_series
        ]

        response = "les series:\n"
        response += "\n".join(
            [f"- {serie.serie_icon} {serie.serie_name}" for serie in series]
        )

        await interaction.response.send_message(response)


async def setup(bot):
    await bot.add_cog(CogBundlesSeries(bot))
