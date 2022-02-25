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
CHANNEL_ID = int(config.get('Bot', 'channel.id'))

bot = commands.Bot(command_prefix='!')

def log(message):
    print("%s - %s" % (datetime.datetime.now(), message))

async def sendmeme(ctx):
    r = requests.get('https://memefryer.herokuapp.com/api/images/fry')
    if r.status_code == 200:
        response = r.json()
        f = io.BytesIO(base64.b64decode(response['imageBytes']))
        f.name = 'meme.png'
        await ctx.send(file=discord.File(f))
    else:
        log('Failed response from Memefryer app! No meme sent!')
        await ctx.send('Hmm... Úgy tűnik odaégett...')

@bot.command(name='ránts', help='Ránt egy véletlenszerü mémet.')
async def fry(ctx):
    log('On-demand meme sending...')
    await ctx.send('Egy pillanat...')
    await sendmeme(ctx)

async def sendScheduledMeme():
    log('Scheduled meme sending...')
    await sendmeme(bot.get_channel(CHANNEL_ID))

@tasks.loop(minutes=1)
async def loop():
    currentTime = datetime.datetime.now()
    if currentTime.minute == 0:
        if currentTime.hour == 8:
            await bot.get_channel(CHANNEL_ID).send('Érkezik a reggeli rántás...')
            await sendScheduledMeme()
        if currentTime.hour == 14:
            await bot.get_channel(CHANNEL_ID).send('Érkezik a délutáni rántás...')
            await sendScheduledMeme()
        if currentTime.hour == 20:
            await bot.get_channel(CHANNEL_ID).send('Érkezik az esti rántás...')
            await sendScheduledMeme()

@bot.event
async def on_ready():
    print('Meme fryer is UP')
    loop.start()

bot.run(TOKEN)
