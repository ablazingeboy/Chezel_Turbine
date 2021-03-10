import os
import discord
from discord.ext import commands
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

bot = commands.Bot(command_prefix='_')
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.listen('on_message')
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    if 295234517839380481 in message.raw_mentions:
        await imitate_xezel(message)
    elif 'xezel' in message.content.lower():
        await imitate_xezel(message)
    elif 755737263585099776 in message.raw_mentions:
        await imitate_xezel(message)
    if check_cheese_triggers(message):
        await imitate_cheese(message)

@bot.command(name='invite', help='Provides a link to invite me to your server!')
async def invite(ctx):
    invite_embed = discord.Embed(
        title='Invite Chezel_Turbine to **YOUR** server!',
        url='https://discord.com/api/oauth2/authorize?client_id=819025824229359685&permissions=355392&scope=bot',
        color=discord.Color.red()
    )
    invite_embed.set_footer(text=f'Currently in {len(bot.guilds)} servers! | Made with <3 by ablazingeboy#7375')
    await ctx.send(embed=invite_embed)

@bot.command(name='help', help='Shows this page.')
async def help(ctx, args=None):
    help_embed = discord.Embed(title="**Command Usage**", color=discord.Color.red())
    command_names_list = [x.name for x in bot.commands]

    if not args:
        help_embed.add_field(
            name="*Who are you and what did you to do xezelBot and cheeseBot?*",
            value='If you ping xezel, he might say something funny...\nIf you call Cheese short, you might regret it...',
            inline=False
        )
        help_embed.add_field(
            name="*What commands does this thing support?*",
            value="\n".join([str(i+1)+".  `"+x.name+"`" for i,x in enumerate(bot.commands)]),
            inline=False
        )
        help_embed.set_footer(
            text="Type \'_help <command name>\' for more details about each command."
        )

    elif args in command_names_list:
        help_embed.add_field(
            name='`_' + args + '`',
            value=bot.get_command(args).help
        )

    else:
        help_embed.add_field(
            name="**Oopsy Woopsy**",
            value="You did a fucky wucky and asked me for a command that doesnt exist!"
        )

    await ctx.send(embed=help_embed)

@bot.command(name='ping', help='Basically useless, just tells you if the bot is running.')
async def ping(ctx):
    if round(bot.latency * 1000) <= 50:
        embed=discord.Embed(title="Pong!", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0x44ff44)
    elif round(bot.latency * 1000) <= 100:
        embed=discord.Embed(title="Pong!", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0xffd000)
    elif round(bot.latency * 1000) <= 200:
        embed=discord.Embed(title="Pong!", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0xff6600)
    else:
        embed=discord.Embed(title="Pong!", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0x990000)
    await ctx.send(embed=embed)

@bot.command(name='sigmafy', help='Sigma-fies the text you feed him.')
async def sigmafy(ctx, *args):
    channel = ctx.message.channel
    await ctx.message.delete()
    sig = 406679351820681216
    send_as = fetch_random_from_text('sigmanames.txt')
    if not args:
        text = 'methinks you should give me something to say next time'
    else:
        text = ' '.join(args)
        text = text.lower()
        text = text.replace('i think', 'methinks')
        text = text.replace('haha', 'heehoo')
        text = text.replace('hehe', 'heehoo')
        text = text.replace('whew', 'wew')
        text = text.replace('phew', 'wew')
        text = text.replace('i am', 'am')
        text = text.replace('goodnight', 'gn')
        text = text.replace('good night', 'gn')
        text = text.replace('to be honest', 'tbh')
        text = text.replace('to be fair', 'tbf')
        text = text.replace('right now', 'rn')
        text = text.replace('boy', 'lad')
        text = text.replace('child', 'lad')
        text = text.replace('kid', 'lad')
    await send_webhook(channel, text, sig, send_as)

async def imitate_xezel(message):
    xez =  295234517839380481
    content = fetch_random_from_text('xezelrefs.txt')
    await send_webhook(message.channel, content, xez, await get_name(message, xez))

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
            await send_webhook(message.channel, response, ches, await get_name(message, ches))
            i = i - 1
    else:
        i = random.randint(1, 3)
        while i > 0:
            response = fetch_random_from_text('cheesenotangryresponse.txt')
            await send_webhook(message.channel, response, ches, await get_name(message, ches))
            i = i - 1

async def get_name(message, userid):
    user = await bot.fetch_user(userid)
    try:
        member = await message.guild.fetch_member(userid)
    except NotFound:
        displayname = user.display_name
    else:
        displayname = member.display_name
    return displayname

async def send_webhook(channel, content, userid, displayname):
    user = await bot.fetch_user(userid)
    avatar_url = user.avatar_url
    web = await channel.webhooks()
    if not web:
        webhook = await channel.create_webhook(name='Chezel_Turbine')
    web = await channel.webhooks()
    webhook = web[0]
    await webhook.send(content=content, username=displayname, avatar_url=avatar_url, allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))

def fetch_random_from_text(filename):
    with open(filename, 'r') as file:
        refs = file.readlines()
    return refs[random.randint(0, len(refs) - 1)]

def check_cheese_triggers(message):
    cheese_match = match_triggers(message, 'cheesetrigger.txt') or ((536870694827589633 in message.raw_mentions) or (803685807587328070 in message.raw_mentions))
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

bot.run(TOKEN)