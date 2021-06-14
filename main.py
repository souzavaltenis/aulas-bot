import discord
import utils.utilidades as util
from discord.ext import commands, tasks
import utils.times as times
import asyncio

db = util.readJSON('database/db.json')
configs = util.readJSON('configs.json')

bot = commands.Bot(command_prefix=configs['prefix'])

infos = {
    'channel': None,
    'future_aulas': None
}

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=configs['nome_server'])
    infos['channel'] = discord.utils.get(guild.channels, name=configs['nome_sala'], type=discord.ChannelType.text)
    task_send_aulas.start()
    await asyncio.sleep(5)
    change_status_bot.start()

@tasks.loop(hours=24)
async def task_send_aulas():
    future_aulas, secs_to_wait_aulas = times.get_seconds_to_wait(configs['info_send'])
    infos['future_aulas'] = future_aulas
    await asyncio.sleep(secs_to_wait_aulas)
    await util.send_horario(db, infos, configs)

@tasks.loop(minutes=1)
async def change_status_bot():
    hours, minutes = times.get_remaing_time(infos['future_aulas'])
    status_msg = f"+Aulas em {hours}Hr {minutes}Min"
    await bot.change_presence(activity=discord.Game(name=status_msg))

@bot.command(name='aulas')
async def view_horario(ctx):
    await util.send_horario(db, infos, configs)

@bot.command(name='db')
async def view_db(ctx):
    await ctx.channel.send(db)

if(__name__ == "__main__"):
    bot.run(configs['token_bot'])