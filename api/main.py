from werkzeug.exceptions import HTTPException
from sqlalchemy.orm import Session
from flask import Flask, request, Response, jsonify, redirect, url_for, send_file
from yestabak.core.db import Base, engine
from sqlalchemy.orm import Session, joinedload
from yestabak.models import Item, CartItem, User, Category
from yestabak.functions import (
    # User
    get_user,
    get_users,
    create_user,
    update_user,
    delete_user,
    # Cart
    get_cart_items,
    update_cart_items,
    # Item
    get_item,
    get_items,
    get_items_by_category_id,
    create_item,
    update_item,
    delete_item,
    # Category
    get_category_by_id,
    get_category_by_name,
    get_categories,
    create_category,
    update_category,
    delete_category,
    # Address
    get_address,
    create_address,
    delete_address,
    # Affiliate
    get_affiliate,
    get_affiliates,
    create_affiliate,
    delete_affiliate,
)
from yestabak.core.api_configs import HOST, PORT
from yestabak.functions import model_to_dict, models_to_dict_list
import json


app = Flask("YesTabak API")


@app.route("/api/v1/integrations/freekassa/", methods=["GET", "POST"])
def freekassa_integration():
    data = request.json if request.is_json else request.args
    print(data)
    return "YES"


# ERROR HANDLER - START
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "error": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


# ERROR HANDLER - END


# USER - START
@app.post("/api/v1/users/")
def create_user_v1():
    try:
        data = request.json if request.is_json else request.args
        missing_data = list(
            map(
                lambda tuple: tuple[1],
                list(
                    filter(
                        lambda value: isinstance(value, tuple) and value[0] is None,
                        [
                            data.get("telegram_id", (None, "telegram_id")),
                            data.get("first_name", (None, "first_name")),
                            data.get("last_name", (None, "last_name")),
                            data.get("username", (None, "username")),
                            data.get("phone_number", (None, "phone_number")),
                        ],
                    )
                ),
            )
        )

        if len(missing_data) > 0:
            return (
                jsonify(
                    {
                        "ok": False,
                        "message": f"missing parameters: {'' + ', '.join(missing_data)}",
                    }
                ),
                400,
            )

        is_succeed, result = create_user(
            session=Session(engine),
            telegram_id=data.get("telegram_id", None),
            first_name=data.get("first_name", None),
            last_name=data.get("last_name", None),
            username=data.get("username", None),
            phone_number=data.get("phone_number", None),
        )

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        return jsonify({"ok": True, "data": model_to_dict(result)}), 200
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.get("/api/v1/users/")
def get_users_v1():
    try:
        is_succeed, result = get_users(session=Session(engine))

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        if len(result) == 0:
            return jsonify({"ok": True, "data": []}), 200

        return jsonify({"ok": True, "data": models_to_dict_list(result)}), 200
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.get("/api/v1/users/<int:telegram_id>")
def get_user_v1(telegram_id: int):
    try:
        is_succeed, result = get_user(session=Session(engine), telegram_id=telegram_id)

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        if is_succeed is None:
            return jsonify({"ok": False, "message": result}), 404

        cart_items = list(
            map(
                lambda cart: {**model_to_dict(cart.item), "quantity": cart.quantity},
                result.cart_items,
            )
        )

        return (
            jsonify(
                {
                    "ok": True,
                    "data": {
                        "user": model_to_dict(result),
                        "addresses": list(
                            map(
                                lambda address: {
                                    "id": address.id,
                                    "data": address.data,
                                },
                                result.addresses,
                            ),
                        ),
                        "cart_items": cart_items,
                    },
                }
            ),
            200,
        )
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.patch("/api/v1/users/<int:telegram_id>")
def update_user_v1(telegram_id: int):
    data = request.json if request.is_json else request.args

    try:
        is_succeed, result = update_user(
            session=Session(engine),
            telegram_id=telegram_id,
            first_name=data.get("first_name", None),
            last_name=data.get("last_name", None),
            username=data.get("username", None),
            role=data.get("role", None),
            phone_number=data.get("phone_number", None),
        )

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        if is_succeed is None:
            return jsonify({"ok": False, "message": result}), 404

        return jsonify({"ok": True, "data": model_to_dict(result)}), 200
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.delete("/api/v1/users/<int:telegram_id>")
def delete_user_v1(telegram_id: int):
    is_succeed, result = delete_user(Session(engine), telegram_id)

    if is_succeed is False:
        return (
            jsonify({"ok": False, "message": f"unknown error when deleting: {result}"}),
            500,
        )

    if is_succeed is None:
        return (
            jsonify({"ok": False, "message": result}),
            404,
        )

    return jsonify({"ok": True, "data": {"telegram_id": result, "deleted": True}}), 200


# USER- END


# ADDRESS - START
@app.post("/api/v1/addresses/")
def create_address_v1():
    try:
        data = request.json if request.is_json and request.json else None

        if not data:
            return (
                jsonify(
                    {
                        "ok": False,
                        "message": 'Please, pass these json values: telegram_id, data. For example: {"telegram_id": 1234567, "data": {...}}',
                    }
                ),
                400,
            )

        missing_data = list(
            map(
                lambda tuple: tuple[1],
                filter(
                    lambda value: isinstance(value, tuple) and value[0] is None,
                    [
                        data.get("telegram_id", (None, "telegram_id")),
                        data.get("data", (None, "data")),
                    ],
                ),
            )
        )

        if len(missing_data) > 0:
            return (
                jsonify(
                    {
                        "ok": False,
                        "message": f"missing parameters: {'' + ', '.join(missing_data)}",
                    }
                ),
                400,
            )

        is_succeed, result = create_address(
            session=Session(engine),
            telegram_id=data.get("telegram_id", None),
            data=data.get("data", None),
        )

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        return jsonify({"ok": True, "data": model_to_dict(result)}), 200
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.get("/api/v1/addresses/")
def get_addresses_of_user_v1():
    telegram_id = request.args.get("telegram_id", None)

    if not telegram_id:
        return (
            jsonify(
                {
                    "ok": False,
                    "message": "Please, provide this value as query: telegram_id",
                }
            ),
            400,
        )

    # print(url_for("get_user_v1", telegram_id=telegram_id))
    return redirect(url_for("get_user_v1", telegram_id=telegram_id))


@app.get("/api/v1/addresses/<int:address_id>")
def get_address_v1(address_id: int):
    try:
        is_succeed, result = get_address(session=Session(engine), id=address_id)

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        if is_succeed is None:
            return jsonify({"ok": False, "message": result}), 404

        # result.data["user_id"] = result.user_id

        return (
            jsonify(
                {
                    "ok": True,
                    "data": result.data,
                }
            ),
            200,
        )
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.delete("/api/v1/addresses/<int:address_id>")
def delete_address_v1(address_id: int):
    is_succeed, result = delete_address(Session(engine), address_id)

    if is_succeed is False:
        return (
            jsonify({"ok": False, "message": f"unknown error when deleting: {result}"}),
            500,
        )

    if is_succeed is None:
        return (
            jsonify({"ok": False, "message": result}),
            404,
        )

    return jsonify({"ok": True, "data": {"address_id": result, "deleted": True}}), 200


# ADDRESS- END


# AFFILIATE - START
@app.post("/api/v1/affiliates/")
def create_affiliate_v1():
    try:
        data = request.json if request.is_json and request.json else None

        if not data:
            return (
                jsonify(
                    {
                        "ok": False,
                        "message": 'Please, pass these json values: group_id, data. For example: {"group_id": 1234567, "data": {...}}',
                    }
                ),
                400,
            )

        missing_data = list(
            map(
                lambda tuple: tuple[1],
                filter(
                    lambda value: isinstance(value, tuple) and value[0] is None,
                    [
                        data.get("group_id", (None, "group_id")),
                        data.get("data", (None, "data")),
                    ],
                ),
            )
        )

        if len(missing_data) > 0:
            return (
                jsonify(
                    {
                        "ok": False,
                        "message": f"missing parameters: {'' + ', '.join(missing_data)}",
                    }
                ),
                400,
            )

        is_succeed, result = create_affiliate(
            session=Session(engine),
            group_id=data.get("group_id", None),
            data=data.get("data", None),
        )

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        return jsonify({"ok": True, "data": model_to_dict(result)}), 200
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.get("/api/v1/affiliates/")
def get_affiliates_v1():
    try:
        is_succeed, result = get_affiliates(session=Session(engine))

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        if len(result) == 0:
            return jsonify({"ok": True, "data": []}), 200

        return (
            jsonify(
                {
                    "ok": True,
                    "data": models_to_dict_list(result),
                },
            ),
            200,
        )
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.get("/api/v1/affiliates/<int:affiliate_id>")
def get_affiliate_v1(affiliate_id: int):
    try:
        is_succeed, result = get_affiliate(session=Session(engine), id=affiliate_id)

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        if is_succeed is None:
            return jsonify({"ok": False, "message": result}), 404

        result.data[0]["id"] = result.id
        result.data[0]["group_id"] = result.group_id
        result.data[0]["created_at"] = result.created_at
        result.data[0]["last_updated_at"] = result.last_updated_at

        return (
            jsonify(
                {
                    "ok": True,
                    "data": result.data[0],
                }
            ),
            200,
        )
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.delete("/api/v1/affiliates/<int:affiliate_id>")
def delete_affiliate_v1(affiliate_id: int):
    is_succeed, result = delete_affiliate(Session(engine), affiliate_id)

    if is_succeed is False:
        return (
            jsonify({"ok": False, "message": f"unknown error when deleting: {result}"}),
            500,
        )

    if is_succeed is None:
        return (
            jsonify({"ok": False, "message": result}),
            404,
        )

    return jsonify({"ok": True, "data": {"affiliate_id": result, "deleted": True}}), 200


# AFFILIATE- END


# ITEM- START
@app.post("/api/v1/items/")
def create_item_v1():
    try:
        data = request.json if request.is_json else request.args
        missing_data = list(
            map(
                lambda tuple: tuple[1],
                list(
                    filter(
                        lambda value: isinstance(value, tuple) and value[0] is None,
                        [
                            data.get("category_id", (None, "category_id")),
                            data.get("name", (None, "name")),
                            data.get("description", (None, "description")),
                            data.get("price", (None, "price")),
                            data.get("photo", (None, "photo")),
                        ],
                    )
                ),
            )
        )

        if len(missing_data) > 0:
            return (
                jsonify(
                    {
                        "ok": False,
                        "message": f"missing parameters: {'' + ', '.join(missing_data)}",
                    }
                ),
                400,
            )

        is_succeed, result = create_item(
            session=Session(engine),
            category_id=data.get("category_id", None),
            name=data.get("name", None),
            description=data.get("description", None),
            price=data.get("price", None),
            photo=data.get("photo", None),
        )

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        return jsonify({"ok": True, "data": model_to_dict(result)}), 200
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.get("/api/v1/items/")
def get_items_v1():
    try:
        is_succeed, result = get_items(session=Session(engine))

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        if len(result) == 0:
            return jsonify({"ok": True, "data": []}), 200

        return (
            jsonify(
                {
                    "ok": True,
                    "data": models_to_dict_list(result),
                },
            ),
            200,
        )
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.get("/api/v1/items/<int:item_id>")
def get_item_v1(item_id: int):
    try:
        is_succeed, result = get_item(session=Session(engine), id=item_id)

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        if is_succeed is None:
            return jsonify({"ok": False, "message": result}), 404

        return (
            jsonify(
                {
                    "ok": True,
                    "data": model_to_dict(result),
                },
            ),
            200,
        )
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.patch("/api/v1/items/<int:item_id>")
def update_item_v1(item_id: int):
    data = request.json if request.is_json else request.args

    try:
        is_succeed, result = update_item(
            session=Session(engine),
            id=item_id,
            category_id=data.get("category_id", None),
            name=data.get("name", None),
            description=data.get("description", None),
            price=data.get("price", None),
            photo=data.get("photo", None),
        )

        if is_succeed is False:
            return (
                jsonify(
                    {
                        "ok": False,
                        "message": f"unknown error: {result}",
                    }
                ),
                500,
            )

        if is_succeed is None:
            return jsonify({"ok": False, "message": result}), 404

        return jsonify({"ok": True, "data": model_to_dict(result)}), 200
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.delete("/api/v1/items/<int:item_id>")
def delete_item_v1(item_id: int):
    is_deleted, result = delete_item(Session(engine), item_id)

    if is_deleted is False:
        return (
            jsonify({"ok": False, "message": f"unknown error when deleting: {result}"}),
            500,
        )

    if is_deleted is None:
        return jsonify({"ok": False, "message": result}), 404

    return jsonify({"ok": True, "data": {"item_id": result, "deleted": True}}), 200


@app.post("/api/v1/items/import")
def import_items_v1():
    data: dict = request.json if request.is_json else request.args
    keys = data.keys()
    for key in keys:
        is_succeed, category = get_category_by_name(Session(engine), name=key)
        for item in data[key]:
            is_created, result = create_item(
                Session(engine),
                category_id=category.id,
                name=item.get("name"),
                description="Описание временно недоступно",
                price=item.get("price"),
                photo="https://creditportal.by/images/tools/no-image_s.jpg",
            )

    return jsonify({"ok": True, "data": {"imported": "yes"}}), 200


# ITEM - END


# CATEGORY - START
@app.post("/api/v1/categories/")
def create_category_v1():
    try:
        data = request.json if request.is_json else request.args

        if data.get("name", None) is None:
            return (
                jsonify(
                    {
                        "ok": False,
                        "message": f"missing parameter: name",
                    }
                ),
                400,
            )

        is_succeed, result = create_category(
            session=Session(engine),
            name=data.get("name", None),
        )

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        return jsonify({"ok": True, "data": model_to_dict(result)}), 200
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.get("/api/v1/categories/")
def get_categories_v1():
    try:
        is_succeed, result = get_categories(session=Session(engine))

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        if len(result) == 0:
            return jsonify({"ok": True, "data": []}), 200

        return (
            jsonify(
                {
                    "ok": True,
                    "data": models_to_dict_list(result),
                },
            ),
            200,
        )
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.get("/api/v1/categories/<int:category_id>")
def get_category_v1(category_id: int):
    try:
        is_succeed, result = get_category_by_id(session=Session(engine), id=category_id)

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        if is_succeed is None:
            return jsonify({"ok": False, "message": result}), 404

        return (
            jsonify(
                {
                    "ok": True,
                    "data": model_to_dict(result),
                },
            ),
            200,
        )
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.get("/api/v1/categories/<int:category_id>/items/")
def get_category_items_v1(category_id: int):
    try:
        is_succeed, result = get_items_by_category_id(
            session=Session(engine), category_id=category_id
        )

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        if is_succeed is None:
            return jsonify({"ok": False, "message": result}), 404

        if len(result) == 0:
            return jsonify({"ok": True, "data": []}), 200

        return (
            jsonify(
                {
                    "ok": True,
                    "data": models_to_dict_list(result),
                },
            ),
            200,
        )
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.patch("/api/v1/categories/<int:category_id>")
def update_category_v1(category_id: int):
    data = request.json if request.is_json else request.args

    try:
        is_succeed, result = update_category(
            session=Session(engine),
            id=category_id,
            name=data.get("name", None),
        )

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        if is_succeed is None:
            return jsonify({"ok": False, "message": result}), 404

        return jsonify({"ok": True, "data": model_to_dict(result)}), 200
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.delete("/api/v1/categories/<int:category_id>")
def delete_category_v1(category_id: int):
    is_deleted, result = delete_category(Session(engine), category_id)

    if is_deleted is False:
        return (
            jsonify({"ok": False, "message": f"unknown error when deleting: {result}"}),
            500,
        )

    if is_deleted is None:
        return (
            jsonify({"ok": False, "message": result}),
            404,
        )

    return jsonify({"ok": True, "data": {"category_id": result, "deleted": True}}), 200


# CATEGORY - END


# CART - START
@app.post("/api/v1/users/<int:telegram_id>/cart_items/")
def create_cart_item_v1(telegram_id: int):
    """
    Add item/items to cart.
    """
    try:
        data = request.json if request.is_json and request.json else {}

        is_succeed, result = update_cart_items(
            session=Session(engine),
            telegram_id=telegram_id,
            items=data.get("items", []),
        )

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        cart_items = list(
            map(
                lambda cart: {**model_to_dict(cart.item), "quantity": cart.quantity},
                result,
            )
        )

        return (
            jsonify(
                {
                    "ok": True,
                    "data": cart_items,
                },
            ),
            200,
        )
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


# @app.delete("/api/v1/users/<int:telegram_id>/cart/<int:item_id>")
# def remove_cart_item_v1(telegram_id: int, item_id: int):
#     """
#     Reduce item quantity in cart by 1 (item_quantity - 1)
#     """
#     try:
#         is_succeed, result = remove_cart_item(
#             session=Session(engine),
#             telegram_id=telegram_id,
#             item_id=item_id,
#         )

#         if is_succeed is False:
#             return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

#         is_succeed, result = get_cart_items(
#             session=Session(engine), telegram_id=telegram_id
#         )

#         if is_succeed is False:
#             return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

#         return (
#             jsonify(
#                 {
#                     "ok": True,
#                     "data": models_to_dict_list(result),
#                 },
#             ),
#             200,
#         )
#     except Exception as err:
#         return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


@app.get("/api/v1/users/<int:telegram_id>/cart_items/")
def get_all_cart_items_v1(telegram_id: int):
    try:
        is_succeed, result = get_cart_items(
            session=Session(engine), telegram_id=telegram_id
        )

        if is_succeed is False:
            return jsonify({"ok": False, "message": f"unknown error: {result}"}), 500

        cart_items = list(
            map(
                lambda cart: {**model_to_dict(cart.item), "quantity": cart.quantity},
                result,
            )
        )

        return (
            jsonify(
                {
                    "ok": True,
                    "data": cart_items,
                },
            ),
            200,
        )
    except Exception as err:
        return jsonify({"ok": False, "message": f"server-side error: {err}"}), 500


# @app.delete("/api/v1/cart/<int:item_id>")
# def delete_cart_item_v1(item_id: int):
#     """
#     Reduces quantity of item in cart down to 0 (even if quantity is 10)
#     """
#     data = request.json if request.is_json else request.args

#     is_deleted, result = delete_cart_item(
#         Session(engine), item_id=item_id, telegram_id=data.get("telegram_id", None)
#     )

#     if is_deleted is False:
#         return (
#             jsonify({"ok": False, "message": f"unknown error when deleting: {result}"}),
#             500,
#         )

#     if is_deleted is None:
#         return (
#             jsonify({"ok": False, "message": result}),
#             404,
#         )

#     return jsonify({"ok": True, "data": {"item_id": result, "deleted": True}}), 200

# CART- END


# if __name__ == "__main__":
#     print(f"Running at http://127.0.0.1:8000")
#     app.run(host=HOST, port=PORT)
