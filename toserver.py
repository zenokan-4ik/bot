import requests
from settings import HOST

async def getprofile(login):
    response = requests.get(f'{HOST}getprofile?login={login}')
    return response

async def updatevaldata(login, valdata):
    response = requests.get(f'{HOST}updatevaldata?login={login}&valdata={valdata}')
    return response

async def addbalance(user, amount):
    response = requests.get(f'{HOST}addbalance?user={user}&amount={amount}')
    return response

async def setbalance(user, amount):
    response = requests.get(f'{HOST}setbalance?user={user}&amount={amount}')
    return response

async def getreward(login):
    response = requests.get(f'{HOST}getreward?login={login}')
    return response