from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/financnyPlan/{prioritnaOsId}?minId={minId}
class FinancnePlanyDataResolver(DataResolverWithMinIdBase):
    def __init__(self, financnePlany_collection: Collection, prioritneOsi_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/financnyPlan/{prioritnaOsId}?minId={minId}'
        super().__init__(financnePlany_collection, url)
        self._prioritneOsi_collection = prioritneOsi_collection
        self._min_id_field_name = 'ID'

    async def get_and_store_all_remote_data_async(self):
        prioritnaOsId_field_name = 'prioritnaOsId'
        all_opId = self._prioritneOsi_collection.distinct("id")
        list_of_params = []
        for prioritnaOsId in all_opId:
            list_of_params.append({prioritnaOsId_field_name: prioritnaOsId, 'minId':0})
        return await self.fetch_and_store_all_async(list_of_params)