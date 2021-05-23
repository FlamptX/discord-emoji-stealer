from discord.ext import commands
import aiohttp
import discord
import re

class Putemoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def putemoji(self, ctx, name=None):
      if name.startswith('<'):
        name=None
      else:
        name=name.split('<')[0]
      content = ctx.message.content
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
                  await ctx.send("Emoji bulunamadı.")
                  return
              if name is None:
                  name = content_emoji.split(":")[0]
              emoji = await ctx.guild.create_custom_emoji(image=r, name=name)
              await ctx.send(f"Emoji <a:{emoji.name}:{emoji.id}> başarıyla dızlandı!")
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
                      await ctx.send("Emoji bulunamadı.")
                      return
              if name is None:
                  name = content_emoji.split(":")[1]
              emoji = await ctx.guild.create_custom_emoji(image=r, name=name)
              await ctx.send(f"Emoji <:{emoji.name}:{emoji.id}> başarıyla dızlandı!")

def setup(bot):
    bot.add_cog(Putemoji(bot))
