from connectors.csv_connector import CSVConnector
from connectors.json_connector import JSONConnector
from core.store import Store



def add_stores(input_file_path):
    stores = {}
    obj = JSONConnector(input_file_path, 'stores')
    for store in obj:
        stores[store["name"]] = Store(**store)
    return stores
