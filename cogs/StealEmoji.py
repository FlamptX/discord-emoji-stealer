from discord.ext import commands
import requests
import re
import discord

class StealEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
       
    @commands.command()
    async def stealemoji(ctx, msg_id: int, name=None):
      message = await ctx.channel.fetch_message(msg_id)
      content = message.content
      if "<:" in content or "<a:" in content:
          pattern = "<(.*?)>"

          content_emoji = re.search(pattern, content).group(1)
          if content_emoji.startswith("a:"):
              content_emoji = content_emoji.replace("a:", "")
              emoji_id = content_emoji.split(":")[1]
              r = requests.get(f"https://cdn.discordapp.com/emojis/{emoji_id}.gif")
              if r.content == b'':
                  await ctx.send("Couldn't find the url for that emoji.")
                  return
              if name is None:
                  name = content_emoji.split(":")[0]
              emoji = await ctx.guild.create_custom_emoji(image=r.content, name=name)
              await ctx.send(f"Emoji <a:{emoji.name}:{emoji.id}> has been stolen and added!")
          else:
              emoji_id = content_emoji.split(":")[2]
              r = requests.get(f"https://cdn.discordapp.com/emojis/{emoji_id}.png")
              if r.content == b'':
                  r = requests.get(f"https://cdn.discordapp.com/emojis/{emoji_id}.jpg")
                  if r.content == b'':
                      await ctx.send("Could't find the url for that emoji.")
                      return
              if name is None:
                  name = content_emoji.split(":")[1]
              emoji = await ctx.guild.create_custom_emoji(image=r.content, name=name)
              await ctx.send(f"Emoji <:{emoji.name}:{emoji.id}> has been stolen and added!")

    @stealemoji.error
    async def stealemoji_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            await ctx.send(":x: Wrong command usage. Correct usage: `stealemoji <message id>`")
            return
        raise error

def setup(bot):
    bot.add_cog(StealEmoji(bot))
