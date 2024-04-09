from settings import TOKEN
import json
import datetime
from interactions import Client, slash_command, OptionType, SlashContext, Intents, slash_option, Embed, Color, ButtonStyle, Button, listen
from interactions.api.events import Component
import toserver
import time

ADMINS = [
    '@zenokan4ik',
    '@prostokarasik'
]
DAILY_REWARD = 1000

bot = Client(intents=Intents.ALL)

@slash_command(name='hello', description='xdd')
@slash_option(name='text', description='xdddd', required=True, opt_type=OptionType.STRING)
async def hello(ctx: SlashContext, text: str):
    await ctx.send(text)

@slash_command(name='profile', description='Нажмите чтобы посмотреть свой профиль')
async def profile(ctx: SlashContext):
    response = await toserver.getprofile(ctx.author)
    response = json.loads(response.content.decode('UTF-8'))
    embed = Embed(
        title='Профиль',
        color=Color.random(),
        timestamp=datetime.datetime.now(datetime.UTC)
    )
    components = Button(
        style=ButtonStyle.BLUE,
        label='Получить',
        disabled=False,
        custom_id='get_reward'
    )
    login, valdata, balance, last_reward = response['login'], response['valdata'], response['balance'], response['last_reward']
    embed.add_field(name='Логин', value=login)
    embed.add_field(name='Аккаунт валорант', value=valdata if len(valdata)!=0 else '*/valorant чтобы обновить данные*')
    embed.add_field(name='Баланс', value=balance, inline=True)
    embed.add_field(name='Последняя награда', value=last_reward, inline=True)
    await ctx.send(embed=embed, components=components)

@listen(Component)
async def onclick(event: Component):
    ctx = event.ctx
    match ctx.custom_id:
        case "get_reward":
            response = await toserver.getreward(login=ctx.author)
            response = response.content.decode("UTF-8")
            await ctx.send(response)

@slash_command(name='valorant', description='Обновить/добавить данные аккаунта валорант (в будущем статистика с tracker.gg)')
@slash_option(name='valdata', description='Убедитесь что данные соответствуют формату: nickname#tag. Валидация данных отсутствует!!', opt_type=OptionType.STRING, required=True)
async def valorant(ctx: SlashContext, valdata: str):
    valdata = '%23'.join(valdata.split('#'))
    response = await toserver.updatevaldata(ctx.author, valdata)
    response = response.content.decode("UTF-8")
    await ctx.send(response)

@slash_command(name='addbalance', description='Добавить баланс')
@slash_option(name='user', description='user', required=True, opt_type=OptionType.STRING)
@slash_option(name='amount', description='Лаве', required=True, opt_type=OptionType.INTEGER)
async def addbalance(ctx: SlashContext, user: str, amount: int):
    if str(ctx.author) in ADMINS:
        user = user if user[0]=='@' else '@'+user
        response = await toserver.addbalance(user=user, amount=amount)
        response = response.content.decode("UTF-8")
        await ctx.send(response)
    else:
        await ctx.send('Запрещено')

@slash_command(name='setbalance', description='Поменять баланс на ...')
@slash_option(name='user', description='user', required=True, opt_type=OptionType.STRING)
@slash_option(name='amount', description='Лаве', required=True, opt_type=OptionType.INTEGER)
async def setbalance(ctx: SlashContext, user: str, amount: int):
    if str(ctx.author) in ADMINS:
        user = user if user[0]=='@' else '@'+user
        response = await toserver.addbalance(user=user, amount=amount)
        response = response.content.decode("UTF-8")
        await ctx.send(response)
    else:
        await ctx.send('Запрещено')

bot.start(TOKEN)