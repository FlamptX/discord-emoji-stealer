from discord.ext import commands
import aiohttp
import discord
import re

class AddEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def addemoji(self, ctx, emoji: discord.Emoji, name=None):
        asset = emoji.url_as()
        if not name:
            name = emoji.name
        emoji = await ctx.guild.create_custom_emoji(image=await asset.read(), name=name)
        await ctx.send(f"Emoji <:{emoji.name}:{emoji.id}> was added!")

    @addemoji.error
    async def addemoji_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument given, it must be an emoji.")
            return
        raise error
        
def setup(bot):
    bot.add_cog(AddEmoji(bot))
