from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/financnyPlan/{prioritnaOsId}?minId={minId}
class FinancnePlanyDataResolver(DataResolverWithMinIdBase):
    def __init__(self, financnePlany_collection: Collection, prioritneOsiDetail_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/financnyPlan/{prioritnaOsId}?minId={minId}'
        super().__init__(financnePlany_collection, url)
        self._prioritneOsiDetail_collection = prioritneOsiDetail_collection
        self._min_id_field_name = 'ID'
        self._prioritnaOs_field_name = 'prioritnaOsId'
    
    def get_all_keys(self) -> set:
        return self._prioritneOsiDetail_collection.distinct("id")
    
    def get_params_based_on_key(self, key) -> dict:
        return {self._prioritnaOs_field_name: key }