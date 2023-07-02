from typing import Dict, List, Literal
from aiohttp import ClientSession
from .api_classes import Item, UserDataResponse, CartItem
from dacite import from_dict


class ApiWrapper:
    def __init__(self):
        self.BASE_URL = "http://62.84.100.13/api/v1"
        self.api_session = ClientSession

    # User

    async def get_user_if_exists(self, user_id: int) -> UserDataResponse:
        try:
            response = await self.__request("GET", self.BASE_URL + f"/users/{user_id}")
        except Exception as e:
            return None
        return from_dict(UserDataResponse, response)

    async def create_user(
        self,
        telegram_id: int,
        first_name: str,
        last_name: str,
        username: str,
        phone_number: str,
    ):
        response = await self.__request(
            "POST",
            self.BASE_URL + "/users",
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
        )
        return response

    # Categories
    async def get_categories(self):
        response = await self.__request("GET", self.BASE_URL + "/categories")
        return response

    async def get_category_items(self, category_id: int):
        response = await self.__request(
            "GET", self.BASE_URL + f"/categories/{category_id}/items"
        )
        return response

    async def create_category(self, name: str):
        response = await self.__request(
            "POST",
            self.BASE_URL + "/categories",
            data={"name": name},
        )
        return response

    async def delete_category(self, category_id: int):
        response = await self.__request(
            "DELETE",
            self.BASE_URL + f"/categories/{category_id}",
        )
        return response

    # Items
    async def get_item_by_id(self, item_id: int) -> Item:
        response = await self.__request("GET", self.BASE_URL + f"/items/{item_id}")
        return response

    async def delete_item(self, item_id: int):
        response = await self.__request("DELETE", self.BASE_URL + f"/items/{item_id}")
        return response

    async def create_item(
        self, name: str, description: str, photo: str, price: int, category_id: int
    ):
        response = await self.__request(
            "POST",
            self.BASE_URL + f"/items/",
            data={
                "name": name,
                "description": description,
                "photo": photo,
                "price": price,
                "category_id": category_id,
            },
        )
        return response

    async def update_item(self, item_id: int, update_type: str, data: int | str):
        response = await self.__request(
            "PATCH", self.BASE_URL + f"/items/{item_id}", data={update_type: data}
        )

    # Cart
    async def get_user_cart(self, user_id: int) -> List[CartItem]:
        response = await self.__request(
            "GET",
            self.BASE_URL + f"/users/{user_id}/cart_items",
        )
        return response

    async def post_cart(self, user_id: int, cart: List[Dict[int, int]]):
        response = await self.__request(
            "POST",
            self.BASE_URL + f"/users/{user_id}/cart_items/",
            data={"items": cart},
        )
        return response

    # Addresses

    async def delete_user_address(self, address_id: int):
        response = await self.__request(
            "DELETE",
            self.BASE_URL + f"/addresses/{address_id}",
        )
        return response

    async def create_user_address(self, address: Dict[str, str]):
        response = await self.__request(
            "POST", self.BASE_URL + f"/addresses", data=address
        )
        return response

    # ----------------------------------- PRIVATE METHODS ----------------------------------- #
    def __build_params(self, **params):
        valued_params = {}

        for key, value in params.items():
            if value is not None:
                valued_params[key] = value
        return valued_params

    async def __request(
        self,
        method: Literal["GET", "POST", "DELETE", "PATCH"],
        url,
        data=None,
        **params,
    ):
        params = self.__build_params(**params)
        async with self.api_session() as session:
            async with session.request(
                method, url, params=params, json=data
            ) as response:
                json_data = await response.json()
                print(url, data, json_data)
                if not json_data.get("ok", True):
                    raise Exception(
                        f"error while recieving data from api\n Response: {json_data}"
                    )
                return json_data.get("data")
