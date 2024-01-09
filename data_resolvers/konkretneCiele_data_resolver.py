from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/prioritnaOs/{poId}/konkretneCiele?minId={minId}
class KonkretneCieleDataResolver(DataResolverWithMinIdBase):
    def __init__(self, konkretneCiele_collection: Collection, prioritneOsi_collection: Collection,**kwargs):
        url = 'https://opendata.itms2014.sk/v2/prioritnaOs/{poId}/konkretneCiele?minId={minId}'
        super().__init__(konkretneCiele_collection, url)
        self._prioritneOsi_collection = prioritneOsi_collection

    async def get_and_store_all_remote_data_async(self):
        poId_field_name = 'poId'
        all_poId = self._prioritneOsi_collection.distinct("id")
        list_of_params = []
        for poId in all_poId:
            list_of_params.append({poId_field_name: poId, 'minId':0})
        return await self.fetch_and_store_all_async(list_of_params)

# https://opendata.itms2014.sk/v2/konkretnyCiel/{kcId}
class KonkretneCieleDetailDataResolver(DataDetailResolverBase):
    def __init__(self, 
                 konkretneCieleDetail_collection: Collection, 
                 konkretneCiele_collection: Collection,
                 **kwargs):
        url = 'https://opendata.itms2014.sk/v2/konkretnyCiel/{kcId}'
        super().__init__(konkretneCieleDetail_collection, url, konkretneCiele_collection, "id", "kcId")