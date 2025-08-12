from typing import Optional
import discord
from discord import Guild, TextChannel, app_commands
from discord.ext import commands

from model.Bundle import Bundle
from model.Permission import Permission
from model.ReactChannel import ReactChannel
from model.Serie import Serie


class CogReactChannels(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="definir_salon_roles",
        description="définit le salon dans lequel les utilisateur pouront s'ajouter/se retirer des séries/bundles",
    )
    async def set_react_channel(
        self, interaction: discord.Interaction, channel: Optional[discord.TextChannel]
    ):
        await interaction.response.defer(ephemeral=True)
        if not Permission.is_user_powerfull(interaction):
            return await interaction.edit_original_response(
                content="vous n'avez pas les permissions requises pour effectuer cette action"
            )

        if not channel:
            channel_id = interaction.channel_id
            assert channel_id != None
            assert interaction.guild != None
            guild_channel = interaction.guild.get_channel(channel_id)
            if not type(guild_channel) is discord.TextChannel:
                return await interaction.edit_original_response(
                    content="le salon doit être textuel"
                )
            channel = guild_channel

        assert type(interaction.guild) is Guild
        ReactChannel.save(interaction.guild.id, channel.id)
        await actualise_role_messages(self.bot, interaction.guild.id)
        await interaction.edit_original_response(
            content=f"{channel.name} est désormais le salon pour ajouter les séries et bundles aux utilisateurs"
        )


async def actualise_role_messages(bot: commands.Bot, server_id: int):
    # remove recent bot's messages to avoid duplicates
    channel = bot.get_channel(ReactChannel.getByServer(server_id)[0].channel_id)
    assert type(channel) is TextChannel
    messages = [message async for message in channel.history(limit=10)]
    for message in messages:
        if message.author.id == bot.application_id:
            await message.delete()

    bundles = Bundle.getByServer(server_id)
    series = Serie.getByServer(server_id)

    bundles_text = "liste des bundles:"
    for bundle in bundles:
        bundles_text += f"\n- {bundle.bundle_icon} {bundle.bundle_name}"

    series_text = "liste des series:"
    for serie in series:
        series_text += f"\n- {serie.serie_icon} {serie.serie_name}"

    info_text = """
réagissez pour obtenir le role correspondant
les bundles contiennent plusieurs séries et leurs roles vous seront automatiquement ajouté
si vous voulez ne plus avoir un rôle retirer la réaction correspondante
(si la réaction a disparu ajouter puis retirer la)
    """
    info_message = await channel.send(info_text)
    bundle_message = await channel.send(bundles_text)
    serie_message = await channel.send(series_text)

    for bundle in bundles:
        await bundle_message.add_reaction(bundle.bundle_icon)
    for serie in series:
        await serie_message.add_reaction(serie.serie_icon)


async def setup(bot: commands.Bot):
    await bot.add_cog(CogReactChannels(bot))
