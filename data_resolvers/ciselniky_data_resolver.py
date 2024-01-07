from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverBase

class CiselnikyDataResolver(DataResolverBase):
    def __init__(self, main_collection: Collection, remote_url: str):
        super().__init__(main_collection, remote_url)

    async def get_all_remote_data_async(self):
        return await self.fetch_all_async([{}])
    
    def perform_next_fetch(self, fetched_data):
        return False

class CiselnikyDetailDataResolver(DataResolverBase):
    def __init__(self, main_collection: Collection, remote_url: str, ciselniky_collection: Collection):
        super().__init__(main_collection, remote_url)
        self._ciselniky_collection = ciselniky_collection

    async def get_all_remote_data_async(self):
        ciselnikKod_field_name = 'ciselnikKod'
        all_ciselnik_kod = self._ciselniky_collection.distinct(ciselnikKod_field_name)
        list_of_params = []
        for ciselnik_kod in all_ciselnik_kod:
            list_of_params.append({ciselnikKod_field_name: ciselnik_kod, 'minId':0})
        return await self.fetch_all_async(list_of_params)
    
    def transform_fetched_data(self, fetched_data, ciselnikKod:str, **params:dict):
        return [{'ciselnikKod': ciselnikKod} | item for item in fetched_data]
    
    def perform_next_fetch(self, fetched_data):
        return True if fetched_data else False
    
    def get_updated_params(self, fetched_data, params:dict)-> dict:
        min_id = max(fetched_data, key=lambda item: item["id"])['id']
        params['minId'] = min_id
        return params