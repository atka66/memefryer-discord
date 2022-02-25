# coding=utf-8
import io
import discord
from discord.ext import commands, tasks
import requests
import base64
import datetime
import configparser

config = configparser.ConfigParser()
config.read_file(open('bot.properties', 'r'))

TOKEN = config.get('Bot', 'token')

bot = commands.Bot(command_prefix='!')
channel_id = config.get('Bot', 'channel.id')

def log(message):
    print("%s - %s" % (datetime.datetime.now(), message))

def getmeme():
    response = requests.get('https://memefryer.herokuapp.com/api/images/fry').json()
    f = io.BytesIO(base64.b64decode(response['imageBytes']))
    f.name = 'meme.png'
    return discord.File(f)

@bot.command(name='ránts', help='Ránt egy véletlenszerü mémet.')
async def fry(ctx):
    log('On-demand meme sending...')
    await ctx.send('Egy pillanat...')
    await ctx.send(file=getmeme())

async def sendScheduledMeme():
    log('Scheduled meme sending...')
    await bot.get_channel(channel_id).send(file=getmeme())

@tasks.loop(minutes=1)
async def loop():
    currentTime = datetime.datetime.now()
    if currentTime.minute == 0:
        if currentTime.hour == 8:
            await bot.get_channel(channel_id).send('Érkezik a reggeli rántás...')
            await sendScheduledMeme()
        if currentTime.hour == 14:
            await bot.get_channel(channel_id).send('Érkezik a délutáni rántás...')
            await sendScheduledMeme()
        if currentTime.hour == 20:
            await bot.get_channel(channel_id).send('Érkezik az esti rántás...')
            await sendScheduledMeme()

@bot.event
async def on_ready():
    print('Meme fryer is UP')
    loop.start()

bot.run(TOKEN)
