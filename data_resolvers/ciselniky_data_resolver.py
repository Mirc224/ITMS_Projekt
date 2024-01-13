from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverBase, DataResolverWithMinIdBase
import logging

# https://opendata.itms2014.sk/v2/ciselniky
class CiselnikyDataResolver(DataResolverBase):
    def __init__(self, ciselniky_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/ciselniky'
        super().__init__(ciselniky_collection, url)
    
    def perform_next_fetch(self, fetched_data):
        return False

# https://opendata.itms2014.sk/v2/hodnotaCiselnika/{ciselnikKod}?minId={minId}
class CiselnikyDetailDataResolver(DataResolverWithMinIdBase):
    def __init__(self, ciselnikyDetail_collection: Collection, ciselniky_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/hodnotaCiselnika/{ciselnikKod}?minId={minId}'
        super().__init__(ciselnikyDetail_collection, url)
        self._ciselniky_collection = ciselniky_collection
        self._cislenikKod_field_name = 'ciselnikKod'

    def get_all_keys(self) -> set:
        return self._ciselniky_collection.distinct(self._cislenikKod_field_name)
    
    def get_params_based_on_key(self, key) -> dict:
        return { self._cislenikKod_field_name : key}
    
    def transform_fetched_data(self, fetched_data, ciselnikKod:str, **params:dict):
        return [{self._cislenikKod_field_name: ciselnikKod} | item for item in fetched_data]
    
    def check_related_collections(self):
        self._check_if_collection_is_empty(self._ciselniky_collection)