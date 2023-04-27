import os
import discord
import re
import json
import pytesseract
# import math
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv
from urllib.request import urlopen
import urllib
import io
from PIL import Image

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# intents = discord.Intents(messages=True, guilds=True)

# GUILD = os.getenv('DISCORD_GUILD')
# client = discord.Client(intents = discord.Intents.all())
# client = discord.Client()

async def get_prefix(bot, message):
    if message.guild:
        try:
            with open('prefixes.json', 'r') as f:
                prefixes = json.load(f)
            prefix =  prefixes[str(message.guild.id)]
        except:
            prefix = "-"
    else:
        prefix = "-"

    return prefix


intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix=get_prefix, intents=intents, case_insensitive = True)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'bot {bot.user} is ready')


@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '-'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx,prefix):
    if ctx.guild is None:
        await ctx.send("This command can only be used in a guild.")
        return
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)
@setprefix.error
async def setprefix_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to be an admin to use this command!")
@bot.event
async def on_member_join(member):
    channel_name = 'general'
    channel = discord.utils.get(member.guild.channels, name=channel_name)
    
    if channel is None:
        print(f"Channel '{channel_name}' not found.")
        return

    embed = discord.Embed(description=f"Welcome {member.mention} to {member.guild.name}!", color=discord.Color.blue())
    embed.set_image(url=member.avatar_url)

    await channel.send(embed=embed)
@bot.command()
@commands.has_permissions(administrator=True)
async def setwelcomechannel(ctx,arg):
    if discord.Permissions.administrator :
        with open("welcome.json","r") as r:
            wel = json.load(r)
        wel[str(ctx.guild.id)] = arg
        with open("welcome.json","w") as r:
            json.dump(wel, r, indent = 4)
    else:
        ctx.send("you need to be an admin to use this command")

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

@bot.command()
async def invite(ctx):
    await ctx.send(embed=discord.Embed(description="https://discord.com/api/oauth2/authorize?client_id=1068941693623222353&permissions=8&scope=bot"))
# @bot.command()
# @commands.is_owner()
# async def exec(ctx, arg):
#   await ctx.send(str(exec(str(arg))))
@bot.command()
async def malset(ctx, arg):
    try:
        with open("mal.json", "r") as f:
            acc = json.load(f)
        # if str(ctx.message.author.id) in acc:
        #     ctx.send("you already have an account set"
        #              "would you like to change it?")
        #     while True:
        #         ### wait for the client to send a message and then continue executing the code ###
        #         if ans.lower() = y:
        #             acc[str(ctx.message.author.id)] = arg
        #         elif ans.lower = "cancel":
        #             break
        #         else:
        #             continue
        # else:
        #     acc[str(ctx.message.author.id)] = arg
        try:
            test = urlopen(f"https://myanimelist.net/profile/{arg}")
        except:
            ctx.send(discord.Embed(description="",))
        acc[str(ctx.message.author.id)] = {"profile":f"https://myanimelist.net/profile/{arg}",
                                           "a_l":f"https://myanimelist.net/animelist/{arg}",
                                           "m_l":f"https://myanimelist.net/mangalist/{arg}"}
        with open("mal.json", "w") as f:
            json.dump(acc, f, indent = 4)
        await ctx.send(embed=discord.Embed(description="your account has been set!"))
    except:
        acr = discord.Embed(description= "the username that you entered does not exist")
        await ctx.send(embed=acr)

@bot.command()
async def mal(ctx, arg=None):
    try:
        if arg:
            with open("mal.json", "r") as f:
                acc2 = json.load(f)
            mal = acc2[arg]
            embed2 = discord.Embed(title="Profile", url=mal["profile"], description= mal["a_l"]+ '\n' + mal["m_l"], color=0xFF5733)
            html = urlopen(mal["profile"])
            bs = BeautifulSoup(html, 'html.parser')
            re1 = re.findall(".*(https:\/\/cdn\.myanimelist\.net\/images\/userimages\/\w*\.jpg\?t=\w*).*", str(bs))
            embed2.set_thumbnail(url= re1[0])
            await ctx.send(embed=embed2)
        else:
            with open("mal.json", "r") as f:
                acc2 = json.load(f)
            mal = acc2[str(ctx.message.author.id)]
            embed2 = discord.Embed(title="Profile", url=mal["profile"], description= mal["a_l"]+ '\n' + mal["m_l"], color=0xFF5733)
            html = urlopen(mal["profile"])
            bs = BeautifulSoup(html, 'html.parser')
            re1 = re.findall(".*(https:\/\/cdn\.myanimelist\.net\/images\/userimages\/\w*\.jpg\?t=\w*).*", str(bs))
            embed2.set_thumbnail(url= re1[0])
            await ctx.send(embed=embed2)
    except:
        await ctx.send("there is no account linked to this profile")
@bot.command()
@commands.is_owner()
async def malremove(ctx, arg):
    try:
        with open("mal.json", "r") as f:
            acc2 = json.load(f)
        del acc2[arg]
        with open("mal.json", "w") as f:
            json.dump(acc2, f, indent = 4)
        ctx.send(embed=discord.Embed(description="the user mal has been removed"))
    except:
        await ctx.send(embed=discord.Embed(description="please specify a valid user to remove"))
@bot.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def clr(ctx,arg=None):
    # msgs = []
    # async for x in ctx.channel.history(limit = num):
    #     msgs.append(x)
    if arg:
        num = int(arg) + 1
        await ctx.channel.purge(limit = num)
    else:
        await ctx.send("")

        # This will make sure that the response will only be registered if the following
        # conditions are met:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["confirm"]

        msg = await bot.wait_for("message", check=check)
        if msg.content.lower() == "confirm":
            await ctx.channel.purge(limit=100)
        else:
            return
@clr.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to be an admin to use this command!")

@bot.command()
@commands.is_owner()
async def status(ctx,arg):
    if arg == "online" or arg == "on":
        await bot.change_presence(status=discord.Status.online)
    elif arg == "dontdisturb" or arg == "dd":
        await bot.change_presence(status=discord.Status.do_not_disturb)
    elif arg == "invisible" or arg == "inv":
        await bot.change_presence(status=discord.Status.invisible)
    elif arg == "idle" :
        await bot.change_presence(status=discord.Status.idle)
    else:
        ctx.send("please select a valid status")

@status.error
async def status_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("this command can only be used by the owner of the bot")

@bot.command()
# @commands.is_owner()
async def p2p(ctx):
    try:
        image_url = ctx.message.attachments[0].url
    except:
        await ctx.send(embed=discord.Embed(description="please attach an image"))
        return
    file_name = f"image-{ctx.message.author.id}-p2p"
    img_file_name = file_name+".png"
    pdf_file_name = file_name+".pdf"

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0'
    }
    request = urllib.request.Request(image_url, headers=headers)
    response = urllib.request.urlopen(request)
    image_data = response.read()

    with open(img_file_name, "wb") as f:
        f.write(image_data)

    image = Image.open(img_file_name)
    if image.mode == "RGBA":
        image = image.convert("RGB")

    image.save(pdf_file_name, 'PDF', resolution=100.0)
    

    with open(pdf_file_name, "rb") as file:
        await ctx.send("the pdf:", file=discord.File(file, "image.pdf"))
    os.system(f'rm {img_file_name}')
    os.system(f'rm {pdf_file_name}')

@bot.command()
# @commands.is_owner()
async def p2t(ctx):
    try:
        image_url = ctx.message.attachments[0].url
    except:
        await ctx.send(embed=discord.Embed(description="please attach an image"))
        return
    file_name = f"image-{ctx.message.author.id}-p2t.png"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0'
    }
    request = urllib.request.Request(image_url, headers=headers)
    response = urllib.request.urlopen(request)
    image_data = response.read()

    with open(file_name, "wb") as f:
        f.write(image_data)

    image = Image.open(file_name)

    gray_img = image.convert('L')

    text = pytesseract.image_to_string(gray_img)

    await ctx.send(text)
    os.system(f'rm {file_name}')

class NewHelpName(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)

bot.help_command = NewHelpName()
bot.run(TOKEN)
