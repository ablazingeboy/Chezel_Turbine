import os
import discord
from discord.errors import NotFound
from dotenv import load_dotenv
import random
from fuzzywuzzy import fuzz
from threading import Timer

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
global is_angry
global anger_threshold
is_angry = False
anger_threshold = 0

client = discord.Client()

@client.event
async def on_ready():
    print('login successful')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.bot:
        return
    if message.content.startswith('_help'):
        await help(message)
        return
    if message.content.startswith('_invite'):
        await invite(message)
        return
    if 295234517839380481 in message.raw_mentions:
        await imitate_xezel(message)
    elif 'xezel' in message.content.lower():
        await imitate_xezel(message)
    if check_cheese_triggers(message):
        await imitate_cheese(message)
    

async def imitate_xezel(message):
    xez =  295234517839380481
    content = fetch_random_from_text('xezelrefs.txt')
    await send_webhook(message, content, xez)

async def imitate_cheese(message):
    global is_angry
    global anger_threshold
    ches = 536870694827589633
    print('successfully triggered')
    anger_threshold = anger_threshold + 10
    randomnum = random.randint(0, 100)
    print(f'{randomnum} | {anger_threshold}')
    if  randomnum < anger_threshold:
        anger_cheese()
    if is_angry:
        i = random.randint(0, 5)
        if i == 0:
            i = 9
        while i > 0:
            response = fetch_random_from_text('cheeseangryresponse.txt')
            await send_webhook(message, response, ches)
            i = i - 1
    else:
        i = random.randint(1, 3)
        while i > 0:
            response = fetch_random_from_text('cheesenotangryresponse.txt')
            await send_webhook(message, response, ches)
            i = i - 1

async def send_webhook(message, content, userid):
    user = await client.fetch_user(userid)
    try:
        member = await message.guild.fetch_member(userid)
    except NotFound as e:
        displayname = user.display_name
    else:
        displayname = member.display_name
    avatar_url = user.avatar_url
    web = await message.channel.webhooks()
    if not web:
        webhook = await message.channel.create_webhook(name='Chezel_Turbine')
    web = await message.channel.webhooks()
    webhook = web[0]
    await webhook.send(content=content, username=displayname, avatar_url=avatar_url)

async def send_embed(message, title, content, footer):
    embed = discord.Embed(
        title=title,
        description=content, 
        color=discord.Color.red()
    )
    embed.set_footer(text=footer)
    await message.channel.send(embed=embed)

def fetch_random_from_text(filename):
    with open(filename, 'r') as file:
        refs = file.readlines()
    return refs[random.randint(0, len(refs) - 1)]

def check_cheese_triggers(message):
    cheese_match = match_triggers(message, 'cheesetrigger.txt') or (536870694827589633 in message.raw_mentions)
    short_match = match_triggers(message, 'shorttrigger.txt')
    return cheese_match and short_match

def match_triggers(message, filename):
    with open(filename, 'r') as file:
        triggers = file.read().splitlines()
    splitstring = message.content.lower().split(' ')
    for word in splitstring:
        for trigger in triggers:
            ratio = fuzz.ratio(word, trigger)
            if ratio > 75:
                print(f'{trigger} | {word} | {ratio}')
                return True
    return False

def anger_cheese():
    global is_angry
    global anger_threshold
    print('cheese angy')
    is_angry = True
    t = Timer(interval=600.0, function=calm_cheese)
    t.start()

def calm_cheese():
    global is_angry
    global anger_threshold
    print('he not angy no more')
    is_angry = False
    anger_threshold = 0

async def help(message):
    await send_embed(
        message=message,
        title= "What is this thing?",
        content='Ping xezel, and he might say something funny...\nCall cheese short, and you\'ll regret it...', 
        footer = f'Made with <3 by ablazingeboy#7375 | This bot is in {len(client.guilds)} servers!'
        )

async def invite(message):
    embed = discord.Embed(
        title='Invite Chezel_Turbine to **YOUR** server!',
        url='https://discord.com/api/oauth2/authorize?client_id=819025824229359685&permissions=604064832&scope=bot', 
        color=discord.Color.red()
    )
    await message.channel.send(embed=embed)

client.run(TOKEN)