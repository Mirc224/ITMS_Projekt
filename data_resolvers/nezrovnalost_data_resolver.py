from data_resolvers.mongo_db_connection import MongoDBConnection
import requests

class NezrovnalostDataResolver:
    def __init__(self, connection:MongoDBConnection, db_name:str, nezrovnalost_col_name:str):
        mongo_client = connection.client
        itms_db = mongo_client.get_database(db_name)
        self._nezrovnalost_collection = itms_db.get_collection(nezrovnalost_col_name)
        self._remote_url_template = 'https://opendata.itms2014.sk/v2/nezrovnalost?minId={minId}'

    def fetch_remote_data(self):
        remote_data = self.get_all_remote_data()
        self._nezrovnalost_collection.delete_many({})
        self._nezrovnalost_collection.insert_many(remote_data)

    def get_all_remote_data(self) -> list[dict]:
        min_id = 0
        all_data = []
        while True:
            current_url = self._remote_url_template.format(minId=min_id)
            current_data_batch = requests.get(current_url).json()
            if not current_data_batch:
                break
            all_data.extend(current_data_batch)
            min_id = max(current_data_batch, key=lambda item: item["id"])['id']
        return all_data