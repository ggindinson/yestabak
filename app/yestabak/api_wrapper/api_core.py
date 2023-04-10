from typing import Literal
from aiohttp import ClientSession
from .api_classes import UserDataResponse
from dacite import from_dict


class ApiWrapper:
    def __init__(self):
        self.BASE_URL = "http://62.84.100.13/api/v1/"
        self.api_session = ClientSession

    async def get_user_if_exists(self, user_id: int) -> UserDataResponse:
        try:
            response = await self.__request("GET", self.BASE_URL + f"/users/{user_id}")
        except:
            return None
        return from_dict(UserDataResponse, response)

    async def create_user(self, user_id: int, first_name: str, last_name: str, username: str, phone: str):
        response = await self.__request("POST", self.BASE_URL + "/users", telegram_id=user_id, first_name=first_name, last_name=last_name, username=username, phone_number=phone)
        return response

    async def get_categories(self):
        response = await self.__request("GET", self.BASE_URL + "/categories")
        return response

    async def get_category_items(self, category_id: int):
        response = await self.__request("GET", self.BASE_URL + f"/categories/{category_id}/items")
        return response

    # ----------------------------------- PRIVATE METHODS ----------------------------------- #
    def __build_params(self, **params):
        valued_params = {}

        for key, value in params.items():
            if value is not None:
                valued_params[key] = value
        return valued_params

    async def __request(self, method: Literal['GET', 'POST', 'DELETE', 'PATCH'], url, **params):
        params = self.__build_params(**params)
        async with self.api_session() as session:
            async with session.request(method, url, params=params) as response:
                json_data = await response.json()
                if not json_data['ok']:
                    raise Exception(
                        f'error while recieving data from api\n Response: {json_data}')
                return json_data['data']
