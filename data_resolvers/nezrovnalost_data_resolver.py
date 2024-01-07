from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverBase

class NezrovnalostDataResolver(DataResolverBase):
    def __init__(self, main_collection: Collection, remote_url: str):
        super().__init__(main_collection, remote_url)

    async def get_all_remote_data_async(self):
        return await self.fetch_all_async([{ "minId": 0 }])
    
    def perform_next_fetch(self, fetched_data):
        return True if fetched_data else False
    
    def get_updated_params(self, fetched_data, params:dict)-> dict:
        min_id = max(fetched_data, key=lambda item: item["id"])['id']
        params['minId'] = min_id
        return params

# 'https://opendata.itms2014.sk/v2/nezrovnalost/{nezrovnalostId}'
class NezrovnalostDetailDataResolver(DataResolverBase):
    def __init__(self, main_collection: Collection, remote_url: str, nezrovnalosti_collection:Collection):
        super().__init__(main_collection, remote_url)
        self._nezrovnalosti_collection = nezrovnalosti_collection

    async def get_all_remote_data_async(self):
        all_nezrovnalosti_ids = self._nezrovnalosti_collection.distinct("id")
        list_of_params = []
        for nezrovnalost_id in all_nezrovnalosti_ids:
            list_of_params.append(
                {
                    'nezrovnalostId': nezrovnalost_id
                })
        return await self.fetch_all_async(list_of_params)
    
    def perform_next_fetch(self, fetched_data):
        return False
    
    def transform_fetched_data(self, fetched_data, **params:dict):
        return [fetched_data]