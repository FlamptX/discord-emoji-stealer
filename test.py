import sys
import traceback
import discord
import requests
from discord.ext import commands
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime
import asyncio
try:
    import thread
except ImportError:
    import _thread as thread
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

cluster = MongoClient(MONGO_URI)
db = cluster['python-bot']
collection = db["users"]
guilds = db['guilds']

bot = commands.Bot(command_prefix='!', help_command=None, intents=discord.Intents.all())

# bot.load_extension("Post")
bot.load_extension("StackOverflow")
bot.load_extension("Makeemoji")

@bot.event
async def on_ready():
    print("ready")

@bot.command()
async def ping(ctx):
    start = datetime.datetime.now()
    test_guild = collection.find_one({"_id": 799328665442713600})
    end = datetime.datetime.now()
    seconds = (end - start).total_seconds()
    milliseconds = round(seconds * 1000) - round(bot.latency * 1000)
    if milliseconds < 0:
        milliseconds = 0
    await ctx.send(f"Pong!\nBot latency: **{round(bot.latency * 1000)}ms**\nCluster latency: **{milliseconds}ms**")

@bot.command(aliases=["tag"])
@commands.has_permissions(manage_messages=True)
async def tags(ctx, arg, tag_name=None):
    guild = collection.find_one({"_id": ctx.guild.id})
    if arg == "add" and tag_name is None:
        await ctx.send("You must specify the name for the tag. Example: `tags add rules`")
    elif arg == "add":
        embed = discord.Embed(title="Tags", description=f"Tag name: `{tag_name}`\n\nWhat should be the response? If you want it to be an embed type `embed`\nYou have __5 minutes__ to answer.\nIf you changed your mind send `abort`.", colour=discord.Colour.orange())
        embed.set_footer(text="check the docs for more info about tags")
        await ctx.send(embed=embed)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            msg = await bot.wait_for("message", check=check, timeout=300)
            response = msg.content
            if response.lower() == "abort":
                await ctx.send("Tag creation aborted.")
                return
            elif response.lower() == "embed":
                await ctx.send("What should be the embed **title**? You have 30 seconds to answer.")
                title_msg = await bot.wait_for("message", check=check, timeout=30)
                title = title_msg.content
                await ctx.send("What should be the embed **description**? You have 30 seconds to answer.")
                description_msg = await bot.wait_for("message", check=check, timeout=30)
                description = description_msg.content
                return
            guild_tags = guild["tags"]
            guild_tags[tag_name] = response
            collection.update_one({"_id": ctx.guild.id}, {"$set": {"tags": guild_tags}})
            embed = discord.Embed(title="Tag created",
                                  description=f"Tag {tag_name} was successfully created!\nUse `tag {tag_name}` to use it or `tag view {tag_name}` to view it.", colour=discord.Colour.gold())
            embed.set_footer(text="check the docs for more info about tags")
            await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            await ctx.send("You didn't reply, the tag was not created.")
            return
    elif arg == "remove" and tag_name is None:
        await ctx.send("You must specify the name of the tag you want to remove. Example: `tags remove rules`")
    elif arg == "remove":
        guild_tags = guild["tags"]
        try:
            del guild_tags[tag_name]
            collection.update_one({"_id": ctx.guild.id}, {"$set": {"tags": guild_tags}})
            await ctx.send("Tag successfully deleted.")
        except KeyError:
            await ctx.send("Tag not found, use `tags list` to see all tags.")
            return
    elif arg == "list":
        try:
            guild_tags = guild["tags"]
        except KeyError:
            await ctx.send("There are no tags in the server.")
            return
        if guild_tags == {}:
            await ctx.send("There are no tags in the server.")
            return
        for x in guild_tags:
            description = f"`{x}`\n"
        embed = discord.Embed(title="Tags list", description="All tags in the server:\n" + description, colour=discord.Colour.teal())
        await ctx.send(embed=embed)
    elif arg == "view" and tag_name is None:
        await ctx.send("You must specify the name of the tag you want to view. Example: `tags view rules`")
    elif arg == "view":
        guild_tags = guild["tags"]
        try:
            tag_view = guild_tags[tag_name]
            embed = discord.Embed(title=f"Tag {tag_name}", description=f"Response: \"{tag_view}\"", colour=discord.Colour.dark_blue())
            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send("Tag not found, use `tags list` to see all tags.")
            return
    elif arg in guild["tags"]:
        response = guild["tags"][arg]
        await ctx.send(response)

@bot.command()
async def test(ctx, item):
    print(int(item))

@test.error
async def test_error(ctx, error):
    msg1 = traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])[2][-48:]
    msg2 = traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])[3]
    embed = discord.Embed(title="Error", description=f'```\n"{msg1}\n{msg2}\n```', colour=discord.Colour.red())
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    name = ctx.guild.name

    owner = ctx.guild.owner
    guild_id = ctx.guild.id
    region = ctx.guild.region
    member_count = ctx.guild.member_count
    verification_level = str(ctx.guild.verification_level)
    created_at = str(ctx.guild.created_at.replace(microsecond=0))

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=f"Info for {name}",
        description=f"Verification level: `{verification_level}`\nBoost level: `{ctx.guild.premium_tier}`\nText channels: `{len(ctx.guild.text_channels)}`\nVoice channels: `{len(ctx.guild.voice_channels)}`",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=f"{owner.name}#{owner.discriminator}", inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=member_count, inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Created At", value=created_at, inline=True)

    await ctx.send(embed=embed)

@bot.command()
async def widget(ctx):
    r = requests.get("https://top.gg/api/widget/upvotes/824770960435314708.svg?noavatar=true")

    with open('widget.svg', 'wb') as f:
        f.write(r.content)

    drawing = svg2rlg("widget.svg")
    renderPM.drawToFile(drawing, "widget.png", fmt="PNG")

    with open("widget.png", "rb") as file:
        await ctx.send(file=discord.File(file))

@bot.command()
async def widgeturl(ctx):
    r = requests.get("https://top.gg/api/widget/upvotes/824770960435314708.svg?noavatar=true")

    with open('widget.svg', 'wb') as f:
        f.write(r.content)

    drawing = svg2rlg("widget.svg")
    renderPM.drawToFile(drawing, "widget.png", fmt="PNG")

    with open("widget.png", "rb") as file:
        await ctx.send(file=discord.File(file))

    embed = discord.Embed(title="Widget", description="Idk")
    file = discord.File("widget.png")
    embed.set_image(url="attachment://widget.png")
    await ctx.send(file=file, embed=embed)

@bot.command(aliases=["ranks", "rank", "lb", "leaderboards"])
async def leaderboard(ctx, t=None):
    users_levels = {}
    users_money = {}

    for member in ctx.guild.members:
        member_exists = collection.find_one({"_id": member.id})
        if member_exists:
            users_levels[member.id] = round(float(member_exists["level"]))

    for member in ctx.guild.members:
        member_exists = collection.find_one({"_id": member.id})
        if member_exists:
            users_money[member.id] = member_exists["money"]

    if t == "-l" or t == "-level":
        users = {k: v for k, v in sorted(users_levels.items(), key=lambda item: item[1], reverse=True)}
    elif t in ["-c", "-m", "-b", "-balance", "-cash", "-money", "-bal"]:
        users = {k: v for k, v in sorted(users_money.items(), key=lambda item: item[1], reverse=True)}
    else:
        users = {k: v for k, v in sorted(users_levels.items(), key=lambda item: item[1], reverse=True)}
    rank = 1
    embed = discord.Embed(title="Server leaderboard", description="", colour=discord.Color.green())
    for x in users:
        if ctx.author.id != x:
            user = bot.get_user(x) or await bot.fetch_user(x)
            embed.add_field(name=f"{rank}. {user.name}#{user.discriminator}",
                            value=f"Level: `{users_levels[x]}` • Money: ${users_money[x]}", inline=False)
        else:
            user_rank = rank
            embed.add_field(name=f"{rank}. {ctx.author.name}#{ctx.author.discriminator}",
                            value=f"Level: `{users_levels[x]}` • Money: ${users_money[x]}", inline=False)
        rank += 1
    # noinspection PyUnboundLocalVariable
    if user_rank == 1:
        rank_text = f"Your rank: {user_rank}st"
    elif user_rank == 2:
        rank_text = f"Your rank: {user_rank}nd"
    else:
        rank_text = f"Your rank: {user_rank}th"
    embed.set_footer(text=rank_text)
    await ctx.send(embed=embed)

bot.run("ODIwMjc3ODI2MDA3MzM0OTE0.YEy1QQ.Y95ZQ3iV70QdqntwVcEc7pCycNc")
