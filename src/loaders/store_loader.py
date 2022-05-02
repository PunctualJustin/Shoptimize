from connectors.csv_connector import CSVConnector
from core.store import Store


stores_csv_file = "inputs/stores.csv"


def add_stores():
    stores = {}
    csv = CSVConnector(stores_csv_file)
    for item in csv:
        stores[item["ID"]] = Store(**item)
    return stores
