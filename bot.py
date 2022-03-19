import os
import discord
import re
import random
import json
import datetime
# import math
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv
from urllib.request import urlopen

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
# intents = discord.Intents()
# intents.members = True
client = discord.Client()

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix = get_prefix)
bot.remove_command('help')

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
async def setprefix(ctx,prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.invisible)
    print('bot is ready')
# @bot.event
# async def on_member_join(member):
#     with open("welcome.json", "r") as w:
#         welcome = json.load(w)
#     if "801878392198135818" in welcome.keys():
#         print(int(welcome["801878392198135818"]))
#         pfp = member.avatar_url
#         s = discord.Embed(description=f"hello {member.mention}"
#                                       f"welcome to the server!")
#         s.set_image(url=(pfp))
#         channel = client.get_channel(int(welcome["801878392198135818"]))
#         await channel.send(embed = s)
#     else:
#         print(":/")
#         return
@bot.command(pass_context=True)
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

# @bot.command()
# @commands.is_owner()
# async def giveaway(ctx):
#
#     file = open("giveaway.txt", "r", encoding='utf-8')
#     galist = []
#     count = 1
#     for line in file:
#         if "|||" in line.strip():
#
#             temp = ""
#             for i in galist:
#                 temp += i + "\n"
#             embed = discord.Embed(title=count, description=temp, color=0xFF5733)
#             await ctx.send( embed = embed )
#             count += 1
#             galist = []
#
#         else:
#
#             galist.append(line.strip())


@bot.command()
async def kanji(ctx):

    def kanji_list():
        in_file = open('kanji.txt', "r", encoding="utf-8")
        kanjilist = []

        for line in in_file:
            kanjilist.append(line.strip())

        return kanjilist

    def dump_kanji(kanji):

        with open("kanji.json", "r", encoding="utf-8") as f:
            kanji_u = json.load(f)
        if str(ctx.message.author.id) in kanji_u:
            kanji_l = kanji_u["kanji"].append(kanji)
            kanji_u[str(ctx.message.author.id)] = {'kanji' : kanji_l, 'time' : datetime.datetime.now().strftime("%X")}
        else:
            kanji_l = []
            # kanji_u[str(ctx.message.author.id)] = {}
            kanji_l.append(kanji)
            kanji_u[str(ctx.message.author.id)] = {'kanji': kanji_l, 'time': datetime.datetime.now().strftime("%X")}
        with open('kanji.json', 'w', encoding='utf8') as f:
            json.dump(kanji_u, f, indent=4, ensure_ascii=False)

    def v_kanji(kanji):

        with open("kanji.json", "r", encoding="utf-8") as f:
            kanji_u2 = json.load(f)
        time =datetime.datetime.now() - kanji_u2[str(ctx.message.author.id)]["time"].datetime.strptime(datetime_str, '%H:%M:%S')

        if (time.seconds/3600) >= 24 and kanji not in kanji_u2[str(ctx.message.author.id)]['kanji']:
            return True

        return False

    kanjilist=kanji_list()
    randk = random.choice(kanjilist)
    with open("kanji.json", "r", encoding="utf-8") as f:
        kanji_u3 = json.load(f)
    if str(ctx.message.author.id) in kanji_u3.keys():
        valid = v_kanji(randk)

        if valid is True:
            dump_kanji(randk)
            await ctx.send(randk)
    else:
        dump_kanji(randk)
        await ctx.send(randk)
@bot.command()
async def invite(ctx):

    await ctx.send(embed="https://discord.com/api/oauth2/authorize?client_id=717009258532831262&permissions=8&scope=bot")

@bot.command()
async def randch(ctx, *, args):

    msg = args
    list1 = msg.split(" ")
    list2 = []

    for i in list1:

        if i != '':

            list2.append(i)

    rand = random.choice(list2)
    await ctx.send(rand)

@bot.command()
async def rank(ctx, *,args):
    def rank(ranklist, count):
        dict1 = {}

        if ranklist == []:

            return {'26uy2d11iuefs08ts3': '1'}

        else:

            rand2 = random.choice(ranklist)
            dict1[rand2] = dict1.get(rand2, count)

            if ranklist == []:

                return {'26uy2d11iuefs08ts3': '1'}

            else:

                ranklist.pop(ranklist.index(rand2))

                dict2 = rank(ranklist, count + 1)

                for i in dict2:
                    dict1[i] = dict1.get(i, dict2[i])

                return dict1
    msg = args
    list1 = msg.split(" ")
    list2 = []
    for i in list1:

        if i != '':

            list2.append(i)

    ranked = rank(list2,1)
    del ranked['26uy2d11iuefs08ts3']
    # for i in ranked:
    #
    #     rn = str(ranked[i]) + " " + ":" + " " + str(i) + "\n"
    #     await ctx.channel.send(rn)
    lists = ""
    for i in ranked:
        lists += str(ranked[i]) + ":" + " " + str(i) + "\n"
    embed = discord.Embed(title="top", description=lists, color=0xFF5733)
    await ctx.send(embed=embed)


@bot.command()
async def randnums(ctx, arg1, arg2):
    # def mkstr(list1):
    #     str1 = ""
    #     for i in list1:
    #         str1 += i
    #     return str1
    list10= []
    int1 = int(arg2)
    for x in range(int1):

        # reg2 = int(str(arg1))
        reg2 = int(arg1)
        while True:

            ran = random.randint(0, reg2)

            if str(ran) not in list10:

                list10.append(str(ran))
                break
    nums = ""
    for i in list10:
        nums += i + '\n'
    await ctx.send(embed=discord.Embed(description=nums))
# @bot.command()
# async def math(ctx, arg):
#
#     try:
#         math = ("math." + arg)
#         await ctx.send(exec(math))
#     except:
#         return

# @bot.command()
# async def exec(ctx, arg):
#
#     if str(ctx.message.author.id) == '483317936862527499':
#         await ctx.send(str(exec(str(arg))))
#     else:
#         print(str(ctx.message.author.id))
#         print("no")
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
@bot.command()
@commands.is_owner()
async def restart(ctx):
    await bot.logout()
    await bot.login(TOKEN, bot=True)
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
            return msg.author == ctx.author and msg.channel == ctx.channel and \
                   msg.content.lower() in ["confirm"]

        msg = await client.wait_for("message", check=check)
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

class NewHelpName(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)
bot.help_command = NewHelpName()
bot.run(TOKEN)
