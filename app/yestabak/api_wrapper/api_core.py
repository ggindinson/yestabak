from typing import Literal
from aiohttp import ClientSession


class ApiWrapper:
    def __init__(self):
        self.BASE_URL = "http://62.84.100.13/api/v1/"
        self.api_session = ClientSession

    async def get_categories(self):
        response = await self.__request("GET", self.BASE_URL + "/categories")
        return response

    # ----------------------------------- PRIVATE METHODS ----------------------------------- #
    def __build_params(self, **params):
        valued_params = {}

        for key, value in params.items():
            if value is not None:
                valued_params[key] = value
        return valued_params

    async def __request(self, method: Literal['GET', 'POST', 'DELETE'], url, **params):
        params = self.__build_params(**params)
        async with self.api_session() as session:
            async with session.request(method, url, **params) as response:
                json_data = await response.json()
                if not json_data['ok']:
                    raise Exception('error while recieving data from api')
                return json_data['data']
