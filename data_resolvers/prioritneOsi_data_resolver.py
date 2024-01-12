from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/operacneProgramy/{opId}/prioritneOsi?minId={minId}
class PrioritneOsiDataResolver(DataResolverWithMinIdBase):
    def __init__(self, prioritneOsi_collection: Collection, operacneProgramy_collection: Collection,**kwargs):
        url = 'https://opendata.itms2014.sk/v2/operacneProgramy/{opId}/prioritneOsi?minId={minId}'
        super().__init__(prioritneOsi_collection, url)
        self._operacneProgramy_collection = operacneProgramy_collection
        self._opId_field_name = 'opId'
    
    def get_all_keys(self) -> set:
        return self._operacneProgramy_collection.distinct("id")
    
    def get_params_based_on_key(self, key) -> dict:
        return { self._opId_field_name : key }

# https://opendata.itms2014.sk/v2/prioritnaOs/{poId}
class PrioritneOsiDetailDataResolver(DataDetailResolverBase):
    def __init__(self, 
                 prioritneOsiDetail_collection: Collection, 
                 prioritneOsi_collection: Collection,
                 **kwargs):
        url = 'https://opendata.itms2014.sk/v2/prioritnaOs/{poId}'
        super().__init__(prioritneOsiDetail_collection, url, prioritneOsi_collection, "id", "poId")