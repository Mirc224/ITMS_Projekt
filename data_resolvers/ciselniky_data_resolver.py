from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverBase, DataResolverWithMinIdBase

# https://opendata.itms2014.sk/v2/ciselniky
class CiselnikyDataResolver(DataResolverBase):
    def __init__(self, ciselniky_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/ciselniky'
        super().__init__(ciselniky_collection, url)

    async def get_and_store_all_remote_data_async(self):
        return await self.fetch_and_store_all_async([{}])
    
    def perform_next_fetch(self, fetched_data):
        return False

# https://opendata.itms2014.sk/v2/hodnotaCiselnika/{ciselnikKod}?minId={minId}
class CiselnikyDetailDataResolver(DataResolverWithMinIdBase):
    def __init__(self, ciselnikyDetail_collection: Collection, ciselniky_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/hodnotaCiselnika/{ciselnikKod}?minId={minId}'
        super().__init__(ciselnikyDetail_collection, url)
        self._ciselniky_collection = ciselniky_collection

    async def get_and_store_all_remote_data_async(self):
        ciselnikKod_field_name = 'ciselnikKod'
        all_ciselnik_kod = self._ciselniky_collection.distinct(ciselnikKod_field_name)
        list_of_params = []
        for ciselnik_kod in all_ciselnik_kod:
            list_of_params.append({ciselnikKod_field_name: ciselnik_kod, 'minId':0})
        return await self.fetch_and_store_all_async(list_of_params)
    
    def transform_fetched_data(self, fetched_data, ciselnikKod:str, **params:dict):
        return [{'ciselnikKod': ciselnikKod} | item for item in fetched_data]