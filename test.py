from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix='!')

bot.load_extension("Makeemoji")

bot.run(TOKEN)
