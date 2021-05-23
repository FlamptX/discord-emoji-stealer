from discord.ext import commands
import aiohttp
import re
import discord

class StealEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
       
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def stealemoji(self, ctx, msg_id: int, name=None):
        message = await ctx.channel.fetch_message(msg_id)
        content = message.content
        if "<:" in content or "<a:" in content:
            pattern = "<(.*?)>"

            content_emoji = re.search(pattern, content).group(1)
            if content_emoji.startswith("a:"):
                content_emoji = content_emoji.replace("a:", "")
                emoji_id = content_emoji.split(":")[1]
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://cdn.discordapp.com/emojis/{emoji_id}.gif", allow_redirects=True) as resp:
                        r = await resp.read()
                if r == b'':
                    await ctx.send("Couldn't find the url for that emoji.")
                    return
                if name is None:
                    name = content_emoji.split(":")[0]
                emoji = await ctx.guild.create_custom_emoji(image=r, name=name)
                await ctx.send(f"Emoji <a:{emoji.name}:{emoji.id}> has been stolen and added!")
            else:
                emoji_id = content_emoji.split(":")[2]
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://cdn.discordapp.com/emojis/{emoji_id}.png", allow_redirects=True) as resp:
                        r = await resp.read()
                if r == b'':
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"https://cdn.discordapp.com/emojis/{emoji_id}.jpg", allow_redirects=True) as resp:
                            r = await resp.read()
                    if r == b'':
                        await ctx.send("Could't find the url for that emoji.")
                        return
                if name is None:
                    name = content_emoji.split(":")[1]
                emoji = await ctx.guild.create_custom_emoji(image=r, name=name)
                await ctx.send(f"Emoji <:{emoji.name}:{emoji.id}> has been stolen and added!")

    @stealemoji.error
    async def stealemoji_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            await ctx.send(":x: Wrong command usage. Correct usage: `stealemoji <message id>`")
            return
        raise error

def setup(bot):
    bot.add_cog(StealEmoji(bot))
