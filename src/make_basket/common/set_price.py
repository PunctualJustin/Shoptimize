def set_price(element: dict, message: str = None) -> bool:
    break_out = False
    while not break_out:
        new_price = input(f"{message} > " if message else f"What is the price? > ")
        if new_price.isdigit():
            element["price"] = float(new_price)
            break
        elif new_price == "r":
            break_out = True
        else:
            print("That is not a valid price")
    return break_out
