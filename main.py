from discord.ext import commands

bot = commands.Bot(command_prefix='!')

bot.load_extension("cogs.MakeEmoji")
bot.load_extension("cogs.StealEmoji")
bot.load_extension("cogs.AddEmoji")

bot.run("token")
