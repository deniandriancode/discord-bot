import discord
from discord.ext import commands
import logging
import requests
import json
import random

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='.', intents=intents, log_handler=handler, log_level=logging.DEBUG)

@bot.command(name='qr',
             description='Make QR code from text or url.')
async def _qr(ctx, *arg):
    link = arg
    if len(arg) == 0:
        await ctx.send("Link cannot be empty")
        return
    elif len(arg) > 1:
        link = '%20'.join(arg)
    url = f'https://chart.googleapis.com/chart?cht=qr&chs=200x200&chl={link}'
    response = requests.get(url).content
    filename = 'qr_code.png'
    with open(filename,'wb') as fp:
        fp.write(response)
    await ctx.send(file=discord.File(filename))

@bot.command(name='joke',
             description='Generate Joke with various category.')
async def _joke(ctx, category='any', joke_type='2'):
    # categories
    # Any, Misc, Programming, Dark, Pun, Spooky, Christmas
    category_pair = {
        'any': 'Any',
        'misc': 'Misc',
        'prg': 'Programming',
        'dark': 'Dark',
        'pun': 'Pun',
        'spk': 'Spooky',
        'chr': 'Christmas'
    }
    joke_type_pair = {
        '1': 'single',
        '2': 'twopart'
    }

    # option
    opt_category = category_pair[category]
    opt_type = joke_type_pair[joke_type]

    url = 'https://v2.jokeapi.dev/joke/{}?type={}'.format(
        opt_category,
        opt_type
    )
    response = requests.get(url).json()
    joke = ''
    if response['error']:
        joke = 'Not found, please use another type.'
        await ctx.send(joke)
    else:
        try:
            joke = response['setup'] + '\n' + response['delivery']
        except Exception:
            joke = response['joke']
        await ctx.send(joke)


@bot.command(name='emb',
             description='Embed message demo')
async def _emb(ctx):
    msg_embed = discord.Embed(
        title='Embed Title',
        description=' Hac habitasse platea dictumst quisque sagittis, purus sit amet volutpat consequat, mauris nunc congue nisi, vitae suscipit tellus mauris? Donec ultrices tincidunt arcu, non sodales neque sodales ut etiam sit? '
    )
    message = await ctx.send(embed=msg_embed)
    await message.add_reaction('💪')
    message = await bot.wait_for('reaction_add')
    await ctx.send("OK")


@bot.command(name='hi',
             description='Greet the user.')
async def _hi(ctx):
    await ctx.send(f'Hi <@{ctx.author.id}>')































































bot.run('<BOT_TOKEN>')
