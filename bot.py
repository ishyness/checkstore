from inspect import ArgSpec
from __future__ import annotations

import asyncio
import json
import os
import sys
import traceback
import random
## pip install discord.py

import aiohttp
import discord
import asyncio
import time
import requests
## pip install requests
import requests as rq
from discord.ext import commands
from discord.ext.commands import ExtensionFailed, ExtensionNotFound, NoEntryPointError
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks
from utils import locale_v2
from utils.valorant.cache import get_cache





load_dotenv()

initial_extensions = ['cogs.admin', 'cogs.errors', 'cogs.notify', 'cogs.valorant']

# intents required
intents = discord.Intents.default()
intents.message_content = True

BOT_PREFIX = '-'

# todo claer white space


## Setup check plaery Fivem
client = commands.Bot(command_prefix=['>'])
client.remove_command('help')


##################


class ValorantBot(commands.Bot):
    debug: bool
    bot_app_info: discord.AppInfo

    def __init__(self) -> None:
        super().__init__(command_prefix=BOT_PREFIX, case_insensitive=True, intents=intents)
        self.session: aiohttp.ClientSession = None
        self.bot_version = '3.3.5'
        self.tree.interaction_check = self.interaction_check

    @staticmethod
    async def interaction_check(interaction: discord.Interaction) -> bool:
        locale_v2.set_interaction_locale(interaction.locale)  # bot responses localized # wait for update
        locale_v2.set_valorant_locale(interaction.locale)  # valorant localized
        return True

    @property
    def owner(self) -> discord.User:
        return self.bot_app_info.owner

    async def on_ready(self) -> None:
        await self.tree.sync()
        print(f"\nLogged in as: {self.user}\n\n BOT IS READY !")
        print(f"Version: {self.bot_version}")

        # bot presence RICH PRESENT
        #activity_type = discord.ActivityType.listening
        #await self.change_presence(activity=discord.Activity(type=activity_type, name="(╯•﹏•╰)"))

    async def setup_hook(self) -> None:
        if self.session is None:
            self.session = aiohttp.ClientSession()

        try:
            self.owner_id = int(os.getenv('OWNER_ID'))
        except ValueError:
            self.bot_app_info = await self.application_info()
            self.owner_id = self.bot_app_info.owner.id

        self.setup_cache()
        await self.load_cogs()
        # await self.tree.sync()

    async def load_cogs(self) -> None:
        for ext in initial_extensions:
            try:
                await self.load_extension(ext)
            except (
                ExtensionNotFound,
                NoEntryPointError,
                ExtensionFailed,
            ):
                print(f'Failed to load extension {ext}.', file=sys.stderr)
                traceback.print_exc()

    @staticmethod
    def setup_cache() -> None:
        try:
            open('data/cache.json')
        except FileNotFoundError:
            get_cache()

    async def close(self) -> None:
        await self.session.close()
        await super().close()

    async def start(self, debug: bool = False) -> None:
        self.debug = debug
        return await super().start(os.getenv('TOKEN'), reconnect=True)







#####################

## Config
class config:
    serverIP = "172.65.194.168:41793" #IP:PORT | Example: 87.98.246.41:30120 | Use 127.0.0.1:PORT if you're running it on same Server as FiveM Server.
    guildID = 853662224547315742 #Your Discord Server ID, must be int. | Example: 721939142455459902
    #Token = "MTAzMzAwMDgzNDYzMzU4MDU3NA.GAWDeQ.r6YxwFGmfIZ9MCu9Zk0cgQlsNO6cfu8r1Cn7Y0" #Your Discord Bot Token
    serverLink = "3bp8kr"


## Events
@client.event
async def on_ready():
    print('Bot Is Ready!')
    print('IF you have any problems, add me in discord, i will help you.!')
    print('SrymC#1202')
    client.my_current_task = live_status.start()

## Players Count Function // Callable Everywhere, returns number
def pc():
    try:
        resp = rq.get('http://'+config.serverIP+'/players.json').json()
        return(len(resp))
    except:
        return('N/A')


########################

## Say Commands
@client.command(pass_content=True, aliases=['s'])
@commands.has_permissions(administrator=True)
async def say(ctx, *, text):
    try:
        await ctx.message.delete()
        timenow = time.strftime("%H:%M")
        embed=discord.Embed(title="FEAR BOT", description=" ", color=0xfff705)
        embed.set_author(name="FEAR BOT", url="http://mastercity.ir/", icon_url="https://pbs.twimg.com/profile_images/1115158697976770560/p1_a7nJX_400x400.jpg")
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.add_field(name="Tin nhắn:", value=text, inline=False)
        embed.set_footer(text=f"{ctx.message.author} | FEAR BOT | {timenow}")
        await ctx.send(embed=embed)
    except Exception as err:
        print(err)
    
@client.command(pass_context=True, aliases=['hs'])
@commands.has_permissions(administrator=True) 
async def hsay(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(text)

## Players Lookup
@client.command(aliases=['playerid', 'loid', 'server'])
@commands.has_permissions(administrator=True) 
async def pid(ctx, pids):
    if not pid:
        await ctx.send('<@{}>, Nhập đúng ID log check từ FEAR BOT dùm!')
        return
    resp = rq.get('http://'+config.serverIP+'/players.json')
    for _ in resp.json():
        if _['id'] == int(pids):
            pembed = discord.Embed(title='Thông tin người chơi từ ID bạn cần!', color=discord.Color.dark_blue())
            pembed.add_field(name='Tên Steam: {}\n ID Log : {}'.format(_['name'], _['id']), value='Ping : {}'.format(_['ping']), inline=False)
            [pembed.add_field(name=args.split(':')[0].capitalize(), value=args.split(':')[1], inline=False) for args in _['identifiers']]

            await ctx.send(embed=pembed)
        else:
            pass

## DiscordID Lookup
@client.command(aliases=['discord', 'did', 'discordid'])
@commands.has_permissions(administrator=True) 
async def discord_identifier(ctx, disid: int=None):
    
    if not disid:
        await ctx.send('<@{}>, Nhập đúng Discord ID lấy từ >pid !'.format(ctx.message.author.id))
        return
    try:
        obj = await client.fetch_user(disid)
        if not obj:
            await ctx.send('Người dùng `{}` không tồn tại!'.format(disid))
        else:
            dembed = discord.Embed(title='Check hồ sơ người dùng thành công!', descrption='API Returted Values :', color=discord.Color.dark_gold())
            dembed.add_field(name='Tên:', value=obj)
            dembed.add_field(name='DiscordID :', value=obj.id)
            dembed.set_image(url=obj.avatar_url)
            await ctx.send(embed=dembed)
    except Exception as err:
        print(err)
    
## Server run
@client.command()
@commands.has_permissions(administrator=True) 
async def gcity(ctx):
    
    await ctx.message.delete()
    content = "~~@everyone~~"
    timenow = time.strftime("%H:%M")
    embed=discord.Embed(title="FEAR Check G-City", description="Cách kết nối server G-City", color=0x8A2BE2)
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1115158697976770560/p1_a7nJX_400x400.jpg")
    embed.add_field(name="✅ Bỏ Cái này vào F8 ✅", value=f"connect {config.serverLink}", inline=False)
    embed.set_footer(text=f"{timenow}")
    await ctx.send(embed=embed, content=content)
    
## Help Command
@client.command()
@commands.has_permissions(administrator=True) 
async def help(ctx):
    
    embed=discord.Embed(title="***FEAR Check G-City***", description="**Lệnh để check người chơi**", color=0x8A2BE2)
    embed.set_author(name="Welcome To FEAR BOT", url="http://mastercity.ir/", icon_url="https://pbs.twimg.com/profile_images/1115158697976770560/p1_a7nJX_400x400.jpg")
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1115158697976770560/p1_a7nJX_400x400.jpg")
    embed.add_field(name="Prefix = >", value="```Vui lòng dùng dấu > trước câu lệnh :)```", inline=False)
    embed.add_field(name=">check", value="```Danh sách người chơi đang Online```", inline=False)
    embed.add_field(name=">pid", value="```Check người chơi đang Online bằng ID```", inline=False)
    embed.add_field(name=">discordid", value="```Check ID Discord```", inline=False)
    embed.add_field(name=">say", value="```Nói gì đó bằng BOT```", inline=False)
    embed.add_field(name=">hsay", value="```Chat ẩn danh [Hidden Mode]```", inline=False)
    embed.add_field(name=">gcity", value="```Lấy IP connect Server G-City```", inline=False)
    embed.set_footer(text="Made With 💖 by SrymC#1202")
    await ctx.send(embed=embed)



## Players Command
@client.command()
@commands.has_permissions(administrator=True) 
async def check(ctx):
##   _ngcontent-cfx-ui-c49
    timenow = time.strftime("%H:%M")
    resp = rq.get('http://'+config.serverIP+'/players.json').json()
    toida = rq.get('http://'+config.serverIP+'/dynamic.json').json()
    total_players = len(resp)
    p = requests.get(f'http://'+config.serverIP+'/dynamic.json')
    server = p.json()
    # maxPlayers & Players
    maxPlayers = server['sv_maxclients']
 # maxPlayers
    ##maxPlayers = server['sv_maxclients']
    if len(resp) > 100:
        for i in range(round(len(resp) / 100)):
            embed = discord.Embed(title='FEAR BOT', description='Danh sách người chơi đang Online G-City', color=discord.Color.blurple())
            embed.set_footer(text=f'Tổng người chơi : {total_players} / {maxPlayers} Bé Iu💖 | FEAR BOT | {timenow}')
            count = 0
            for player in resp:
                embed.description += f"\n" + "> " + "[" + str(player["id"]) + "] " + "***" + str(player["name"]) + "***" 
                
                ##embed.add_field(name=player['name'], value='ID : ' + str(player['id']))
                resp.remove(player)
                count += 1
                if count == 100:
                    break
                else:
                    continue

            await ctx.send(embed=embed)
    else:
        #embed.description += f"\n" + "> " + "[" + str(player["id"]) + "] " + "***" + str(player["name"]) + "***" 
        embed = discord.Embed(title='FEAR BOT', description='Danh sách người chơi', color=discord.Color.blurple())
        embed.set_footer(text=f'Tổng người chơi : {total_players} / {maxPlayers} Bé Iu💖 | FEAR BOT | {timenow}')
        for player in resp:
            #embed.add_field(name=player['name'], value='ID : ' + str(player['id']))
            embed.description += f"\n" + "> " + "[" + str(player["id"]) + "] " + "***" + str(player["name"]) + "***"
        await ctx.send(embed=embed)
@client.command()
@commands.has_permissions(administrator=True)
async def ip(ctx, *, ip=None):
    if not ip:
        await ctx.send('<@{}>, Nhập đúng IP chưa!'.format(ctx.message.author.id))
        return
    rsp = rq.get('http://ip-api.com/json/'+ip).json()
    if rsp['status'] == 'fail':
        #await ctx.send('Error !\nAPI Respond: '+rsp['message']+'\nQuery: '+rsp['query'])
        embed=discord.Embed(color=0xFF0000)
        embed.add_field(name="❌ Hàng chờ lỗi", value="❓ Lý do: "+rsp['message'])
        embed.set_footer(text="Query: "+ip)
        await ctx.send(embed=embed)
        return
    embed=discord.Embed(color=0x00FFFF)
    embed.add_field(name="✅Trạng thái: "+rsp['status'], value=f"\n\n🌍Quốc gia: {rsp['country']} \n\n🌏Mã quốc gia: {rsp['countryCode']} \n\n🔷Khu vực: {rsp['region']} \n\n🔷Tên khu vực: {rsp['regionName']} \n\n🔷City: {rsp['city']} \n\n🕑TimeZone: {rsp['timezone']} \n\n🏢ISP: {rsp['isp']}\n\n🏢ISP OrgName: {rsp['org']}\n\n🏢ISP MoreInfo: {rsp['as']}", inline=False)
    embed.set_footer(text="Yêu cầu IP: "+ip)
    await ctx.send(embed=embed)

## Live Status
@tasks.loop()
async def live_status(seconds=75):
    pcount = pc()
    p = requests.get(f'http://'+config.serverIP+'/dynamic.json')
    server = p.json()
    # maxPlayers & Players
    maxPlayers = server['sv_maxclients']
 # maxPlayers
    ##maxPlayers = server['sv_maxclients']
    Dis = client.get_guild(config.guildID) #Intzz

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'{pcount}/{maxPlayers}Bé iu ở G-City')
    await client.change_presence(activity=activity)
    await asyncio.sleep(15)

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'SrymC#1202')
    await client.change_presence(activity=activity)
    await asyncio.sleep(15)

## Xúc xắc
@client.command(name='xucxac', aliases=['xx'], help='Tung xúc xắc.')
async def xucxac(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

## check công việc


#client.run(os.getenv('TOKEN'))
def run_bot() -> None:
    bot = ValorantBot()
    asyncio.run(bot.start())


if __name__ == '__main__':
    run_bot()
