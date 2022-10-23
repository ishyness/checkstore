from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import discord
from discord import Interaction, app_commands, ui
from discord.ext import commands

if TYPE_CHECKING:
    from bot import ValorantBot


class Admin(commands.Cog):
    """Error handler"""

    def __init__(self, bot: ValorantBot) -> None:
        self.bot: ValorantBot = bot

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, sync_type: Literal['guild', 'global']) -> None:
        """Sync the application commands"""

        async with ctx.typing():
            if sync_type == 'guild':
                self.bot.tree.copy_global_to(guild=ctx.guild)
                await self.bot.tree.sync(guild=ctx.guild)
                await ctx.reply(f"Synced guild !")
                return

            await self.bot.tree.sync()
            await ctx.reply(f"Synced global !")

    @commands.command()
    @commands.is_owner()
    async def unsync(self, ctx: commands.Context, unsync_type: Literal['guild', 'global']) -> None:
        """Unsync the application commands"""

        async with ctx.typing():
            if unsync_type == 'guild':
                self.bot.tree.clear_commands(guild=ctx.guild)
                await self.bot.tree.sync(guild=ctx.guild)
                await ctx.reply(f"Un-Synced guild !")
                return

            self.bot.tree.clear_commands()
            await self.bot.tree.sync()
            await ctx.reply(f"Un-Synced global !")

    @app_commands.command(description='Thông tin cơ bản của FEAR BOT.')
    async def about(self, interaction: Interaction) -> None:
        """Một số thông tin của FEAR Bot."""

        owner_url = f'https://discord.com/users/1001781433385365526'
        github_project = 'https://github.com/ishyness'
        support_url = 'https://discord.gg/63A5DSP5ZZ'

        embed = discord.Embed(color=0xFFFFFF)
        embed.set_author(name='FEAR - VALORANT BOT CHECK', url=github_project)
        embed.set_thumbnail(url='https://i.pinimg.com/564x/bc/ac/33/bcac337003cee8b782506a8c4f23c1b5.jpg')
        embed.add_field(name='Mod by :', value=f"[SrymC#1202]({owner_url})", inline=False)
        embed.add_field(
            name='Người đóng góp:',
            value=f"[Saber](https://discord.com/users/897084641125748746)\n"
            "[DEAD LINE CUSTOM](https://discord.gg/63A5DSP5ZZ)\n"
            inline=False,
        )
        view = ui.View()
        view.add_item(ui.Button(label='GITHUB', url=github_project, row=0))
        view.add_item(ui.Button(label='Donate Me', url='https://atplink.com/ishyness', row=0))
        view.add_item(ui.Button(label='Hỗ trợ', url=support_url, row=0))

        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: ValorantBot) -> None:
    await bot.add_cog(Admin(bot))
