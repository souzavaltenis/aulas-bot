import discord
import utils.times as times
import json

def readJSON(path):
    f = open(path, encoding='utf-8')
    return json.load(f)

async def send_horario(db, infos, configs):

    channel = infos['channel']
    
    id_dia = times.getTimeNow().weekday()
    horario_do_dia = db['horarios'][id_dia]
    nome_dia = db['dias_semana'][horario_do_dia['dia']]
    materias_ids = horario_do_dia['materias']
    inicios = db['inicios']

    await channel.purge(limit=10)
    
    embedGeral = discord.Embed(title='Horário Geral', color=0x00ff00)
    embedGeral.set_image(url=db['img_horario'])
    embedInit = discord.Embed(color=0x0000ff, title=f'Horário de {nome_dia}')
    
    await channel.send(embed=embedGeral)
    await channel.send(embed=embedInit)

    for materia_id, inicio in zip(materias_ids, inicios):
        for materia in db['materias']:
            if(materia['id'] == materia_id):
                textEmbed = f"**[{inicio}]**    *{materia['nome']}*    ({materia['prof']})"
                linkEmbed = materia['link']
                embedAula = discord.Embed(color=0x0000ff, title=textEmbed, url=linkEmbed))
                await channel.send(embed=embedAula)

    new_future_aulas, _ = times.get_seconds_to_wait(configs['info_send'])
    infos['future_aulas'] = new_future_aulas