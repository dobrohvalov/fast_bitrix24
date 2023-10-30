import asyncio

import loguru
import requests

from fast_bitrix24 import BitrixAsync

"""
    Образец функции для выдочи токена авторизации из Битрикс24 
    Можно получении организовать из БД
"""


async def token_func(update_token: bool = False):
    loguru.logger.debug(update_token)
    if update_token:
        params = {
            "grant_type": 'refresh_token',
            "client_id": '',
            'client_secret': '',
            'refresh_token': ''
        }
        request = requests.post('https://oauth.bitrix.info/rest/', params=params)
        loguru.logger.debug(request)
    return 'access_token'


b = BitrixAsync(
    webhook="https://test.bitrix24.ru/rest/",
    verbose=True,
    respect_velocity_policy=True,
    token_func=token_func)


async def test():
    deal = await b.get_by_ID('crm.deal.get', [2])
    return deal

rel = test()
asyncio.run(rel)
