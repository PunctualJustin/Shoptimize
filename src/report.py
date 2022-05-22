from make_basket.common.list_printer import list_printer, ColumnWidths


def get_item_headers(store):
    headers = {
        "ITEM": ColumnWidths.NAME,
        "PRICE": ColumnWidths.PRICE,
    }
    if (
        store.shipping.type_ == "free above"
        and store.lp_variables.get(shipping_type="free above").varValue == 0
    ):
        shipping_type = store.shipping.other_type
    else:
        shipping_type = store.shipping
    if shipping_type.type_ == "distinct":
        headers["SHIPPING"] = ColumnWidths.PRICE
    headers["QTY"] = ColumnWidths.INDEX
    headers["ITEM COST"] = ColumnWidths.PRICE
    return headers


def format_rows(headers, store):
    rows = []
    total = 0

    for item, price in store.items.items():
        row = []
        for header in headers:
            if header == "ITEM":
                row.append(item)
            elif header == "PRICE":
                row.append("${:.2f}".format(price))
            elif header == "SHIPPING":
                row.append("${:.2f}".format(store.shipping_prices[item]))
            elif header == "QTY":
                row.append(
                    f"{0 if store.lp_variables.get(item=item).varValue == 0 else 1}"
                )
            elif header == "ITEM COST":
                shipping_val = (
                    store.shipping_prices.get(item)
                    if store.shipping_prices.get(item) is not None
                    else 0
                )
                cost = (price + shipping_val) * store.lp_variables.get(
                    item=item
                ).varValue
                row.append("${:.2f}".format(cost))
                total += cost
        rows.append(row)
    return rows, total


def get_shipping_cost(store, shipping):
    if shipping.type_ in ["free above", "free"]:
        return 0
    elif shipping.type_ == "flat":
        if any(store.lp_variables.get(item=item).varValue for item in store.items):
            return shipping.price
        else:
            return 0
    elif shipping.type_ == "fixed":
        num_selected = sum(
            store.lp_variables.get(item=item).varValue for item in store.items
        )
        return num_selected * shipping.price
    elif shipping.type_ == "dynamic":
        selected_items = [
            item
            for item in store.items
            if store.lp_variables.get(item=item).varValue > 0
        ]
        return shipping.combinations[selected_items] if len(selected_items) > 0 else 0


def get_totals(headers, store, total_cost):
    totals_headers = [width for width in headers.values()]
    rows = [["" for i in enumerate(totals_headers)]]
    additionals = 0
    if (
        store.shipping.type_ == "free above"
        and store.lp_variables.get(shipping_type="free above").varValue == 0
    ):
        shipping_type = store.shipping.other_type
    else:
        shipping_type = store.shipping

    if shipping_type.type_ != "distinct":
        row = ["" for i in enumerate(totals_headers)]
        row[-3] = "SHIPPING"
        shipping = get_shipping_cost(store, shipping_type)
        additionals += shipping
        row[-1] = "${:.2f}".format(shipping)
        rows.append(row)
    if store.exchange != 1:
        row = ["" for i in enumerate(totals_headers)]
        row[-3] = "EXCHANGE"
        row[-2] = f"{round(store.exchange*100)}%"
        exchange = (store.exchange - 1) * total_cost
        additionals += exchange
        row[-1] = "${:.2f}".format(exchange)
        rows.append(row)
    if store.tax != 0:
        row = ["" for i in enumerate(totals_headers)]
        row[-3] = "TAX"
        row[-2] = f"{round((store.tax - 1)*100)}%"
        tax = (store.tax - 1) * total_cost
        additionals += tax
        row[-1] = "${:.2f}".format(tax)
        rows.append(row)
    row = ["" for i in enumerate(totals_headers)]
    row[-3] = "TOTAL"
    total = total_cost + additionals
    row[-1] = "${:.2f}".format(total)
    rows.append(row)
    return {"headers": totals_headers, "contents": rows}, total


def report(stores, problem):
    summed_total = 0
    for store in stores.values():
        print(f" {store.name} ".upper().center(72, "="))
        headers = get_item_headers(store)
        contents, total_cost = format_rows(headers, store)
        list_printer(headers, contents, False)
        totals_list, total = get_totals(headers, store, total_cost)
        summed_total += total
        list_printer(totals_list["headers"], totals_list["contents"], False, True)
        print("\n")

    if (problem.objective.value() - summed_total) ** 2 > 0.01:
        print(
            f"ERROR! Objective value {problem.objective.value()} does not match summed total {summed_total}"
        )
    else:
        print("GRAND TOTAL = ${:.2f}".format(summed_total))
