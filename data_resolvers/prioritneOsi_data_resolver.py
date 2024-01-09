from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/operacneProgramy/{opId}/prioritneOsi?minId={minId}
class PrioritneOsiDataResolver(DataResolverWithMinIdBase):
    def __init__(self, prioritneOsi_collection: Collection, operacneProgramy_collection: Collection,**kwargs):
        url = 'https://opendata.itms2014.sk/v2/operacneProgramy/{opId}/prioritneOsi?minId={minId}'
        super().__init__(prioritneOsi_collection, url)
        self._operacneProgramy_collection = operacneProgramy_collection

    async def get_and_store_all_remote_data_async(self):
        opId_field_name = 'opId'
        all_opId = self._operacneProgramy_collection.distinct("id")
        list_of_params = []
        for opId in all_opId:
            list_of_params.append({opId_field_name: opId, 'minId':0})
        return await self.fetch_and_store_all_async(list_of_params)

# https://opendata.itms2014.sk/v2/prioritnaOs/{poId}
class PrioritneOsiDetailDataResolver(DataDetailResolverBase):
    def __init__(self, 
                 prioritneOsiDetail_collection: Collection, 
                 prioritneOsi_collection: Collection,
                 **kwargs):
        url = 'https://opendata.itms2014.sk/v2/prioritnaOs/{poId}'
        super().__init__(prioritneOsiDetail_collection, url, prioritneOsi_collection, "id", "poId")