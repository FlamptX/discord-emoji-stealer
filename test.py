from discord.ext import commands

bot = commands.Bot(command_prefix='!')

bot.load_extension("Makeemoji")

bot.run("token")
