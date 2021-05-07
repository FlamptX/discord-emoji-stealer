from discord.ext import commands

bot = commands.Bot(command_prefix='!')

bot.load_extension("cogs.Makeemoji")
bot.load_extension("cogs.StealEmoji")

bot.run("token")
