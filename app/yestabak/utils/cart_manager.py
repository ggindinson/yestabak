from typing import List, Literal, Dict, Any


def check_item_in_list(item_id, items_list: List[Dict[int, int]]):
    for item in items_list:
        if item["id"] == item_id:
            return True
    return False


def decrease_item(item_id, items_list: List[Dict[int, int]]):
    if not check_item_in_list(item_id, items_list):
        cart = list(filter(lambda item: item["id"] != item_id, items_list))
        return cart

    for item in items_list:
        if item["id"] == item_id:
            if item["quantity"] == 1:
                return list(filter(lambda item: item["id"] != item_id, items_list))
            item["quantity"] -= 1
            return items_list


def increase_item(item_id, items_list: List[Dict[int, int]]):
    if not check_item_in_list(item_id, items_list):
        items_list.append({"id": item_id, "quantity": 1})
    else:
        for item in items_list:
            if item["id"] == item_id:
                item["quantity"] += 1
    return items_list


def cart_dispatch(
    item_id: int,
    action: Literal["increase", "decrease", "delete"],
    cart: Dict[int, Any],
):
    """
    :param cart: list of dictionary items. E.g:
    [
        {
            item_id: 1,
            quantity: 1
        }
    ]
    :param action: action type. E.g: "increase" | "decrease" | "delete"
    """
    match (action, item_id):
        case ("increase", item_id):
            cart = increase_item(item_id, cart)
            return cart

        case ("decrease", item_id):
            cart = decrease_item(item_id, cart)
            return cart

        case ("delete", item_id):
            cart = list(filter(lambda item: item["id"] != item_id, cart))

            return cart

        case _:
            raise TypeError(
                f"Wrong action type. \nYou passed: {action} \nPass one of ['increase', 'decrease', 'delete']"
            )
