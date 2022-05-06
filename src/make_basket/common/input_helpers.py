from typing import Callable

def set_price(element: dict, message: str = None) -> bool:
    message = f"{message} > " if message else f"What is the price? > "
    return get_float_input(element, "price", message, "That is not a valid price")


def get_float_input(
    element: dict,
    key: str,
    input_message: str,
    error_message: str,
    additional_validation: Callable = None,
) -> bool:
    break_out = False
    additional_validation = additional_validation or (lambda x: True)
    while not break_out:
        new_price = input(f"{input_message} > ")
        if new_price.isdigit() and additional_validation(new_price):
            element[key] = float(new_price)
            break
        elif new_price == "r":
            break_out = True
        else:
            print(error_message)
    return break_out
