from discord.ext import commands
import aiohttp
import discord
import re

class Fastput(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fastput(self, ctx):
      await ctx.send("quick emoji mode is activated, emojis you send this message will added to server quickly, type 'stop' to exit")
      cancelled=False
      def check(message):
        return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id
      while not cancelled:
          msg = await bot.wait_for('message', check=check)
          if msg.content == "stop":
            await ctx.reply("Finished")
            canceled = True
            break
          try:
              if "<:" in msg.content or "<a:" in msg.content:
                pattern = "<(.*?)>"
                content_emoji = re.search(pattern, msg.content).group(1)
                if content_emoji.startswith("a:"):
                    content_emoji = content_emoji.replace("a:", "")
                    emoji_id = content_emoji.split(":")[1]
                    async with aiohttp.ClientSession() as session:
                     async with session.get(f"https://cdn.discordapp.com/emojis/{emoji_id}.gif", allow_redirects=True) as resp:
                      r = await resp.read()
                    if r == b'':
                        await ctx.send("Couldn't find the url for that emoji.")
                        return
                    name = content_emoji.split(":")[0]
                    try:
                      emoji = await ctx.guild.create_custom_emoji(image=r, name=name)
                      await ctx.send(f"Emoji <a:{emoji.name}:{emoji.id}> was stolen and addded!")
                    except:
                      await ctx.send("I can't add emoji to the server, may the emoji slot be full?")
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
                            await ctx.send("Couldn't find the url for that emoji.")
                            return
                    name = content_emoji.split(":")[1]
                    try:
                      emoji = await ctx.guild.create_custom_emoji(image=r, name=name)
                      await ctx.send(f"Emoji <:{emoji.name}:{emoji.id}> was stolen and added!")
                    except:
                      await ctx.send("I can't add emoji to the server, may the emoji slot be full?")
              else:
               await ctx.reply("I couldn't find emoji in this message, maybe you wanted to exit? type `stop` to exit."n
          except:
              ctx.send('an unexpected error occurred')

def setup(bot):
    bot.add_cog(Fastput(bot))
