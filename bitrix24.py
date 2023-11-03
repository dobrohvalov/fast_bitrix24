import asyncio

import loguru
import requests

from app.Client import crud, schemas
from fast_bitrix24 import BitrixAsync


class Bitrix24(BitrixAsync):
    def __init__(self, Client):
        self.Client = Client
        super().__init__(webhook=self.Client.oauth.client_endpoint, token_func=self.token_func(self.Client))

    @staticmethod
    async def token_func(Client, update_token: bool = False):
        """
            Образец функции для выдочи токена авторизации из Битрикс24
            Можно получении организовать из БД
        """
        loguru.logger.debug(update_token)
        if update_token:
            params = {
                "grant_type": 'refresh_token',
                "client_id": Client.oauth.client_id,
                'client_secret': Client.oauth.client_secret,
                'refresh_token': Client.oauth.refresh_token,
            }
            request = requests.post('https://oauth.bitrix.info/rest/', params=params)
            Client.oauth = schemas.ClientOauth(**request.json())
            crud_client = crud.Client.update(Client)
            loguru.logger.debug(crud_client)
        else:
            return Client.oauth.access_token


    # async def get_by_ID(self, method: str, ID: list):
    #     """ Получаем сделку по ID """
    #     params = {
    #         "id": ID,
    #     }
    #     return await self.call(method, params=params)
#
# b = Bitrix24(
#     webhook="https://test.bitrix24.ru/rest/",
#     verbose=True,
#     respect_velocity_policy=True,
#     )
#
#
# async def test():
#     deal = await b.get_by_ID('crm.deal.get', [2])
#     return deal
#
# rel = test()
# asyncio.run(rel)
