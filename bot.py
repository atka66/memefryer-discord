# coding=utf-8
import io
import discord
from discord.ext import commands, tasks
import requests
import base64
import datetime
import configparser
import time

config = configparser.ConfigParser()
config.read_file(open('bot.properties', 'r'))

TOKEN = config.get('Bot', 'token')
CHANNEL_ID = int(config.get('Bot', 'channel.id'))

bot = commands.Bot(command_prefix='!')

def log(message):
    print("%s - %s" % (datetime.datetime.now(), message))

async def sendPreflight(ctx):
    log('Sending preflight to wake up the backend application...')
    r = requests.get('https://memefryer.herokuapp.com/')
    if r.status_code != 200:
        log('Application is probably sleeping. Waiting for a minute...')
        await ctx.send('A rántó még ébredezik, egy pillanat...')
        time.sleep(60)

async def sendmeme(ctx):
    log('Fetching meme...')
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
    await sendPreflight(ctx)
    await sendmeme(ctx)

async def sendScheduledMeme():
    log('Scheduled meme sending...')
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send('Készül a rántás...')
    await sendPreflight(channel)
    await sendmeme(channel)

@tasks.loop(minutes=1)
async def loop():
    currentTime = datetime.datetime.now()
    if currentTime.minute == 0:
        if currentTime.hour == 8:
            await sendScheduledMeme()
        if currentTime.hour == 14:
            await sendScheduledMeme()
        if currentTime.hour == 20:
            await sendScheduledMeme()

@bot.event
async def on_ready():
    print('Meme fryer is UP')
    loop.start()

bot.run(TOKEN)
