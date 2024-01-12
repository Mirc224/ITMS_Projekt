from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverWithAggregationsBase

# https://opendata.itms2014.sk/v2/operacneProgramy/{opId}/prioritneOsi?minId={minId}
class PrioritneOsiOPDataResolver(DataResolverWithMinIdBase):
    def __init__(self, prioritneOsiOP_collection: Collection, operacneProgramy_collection: Collection,**kwargs):
        url = 'https://opendata.itms2014.sk/v2/operacneProgramy/{opId}/prioritneOsi?minId={minId}'
        super().__init__(prioritneOsiOP_collection, url)
        self._operacneProgramy_collection = operacneProgramy_collection
        self._opId_field_name = 'opId'
    
    def get_all_keys(self) -> set:
        return self._operacneProgramy_collection.distinct("id")
    
    def get_params_based_on_key(self, key) -> dict:
        return { self._opId_field_name : key }

# https://opendata.itms2014.sk/v2/prioritnaOs/{poId}
class PrioritneOsiDetailDataResolver(DataDetailResolverWithAggregationsBase):
    def __init__(self, 
                 prioritneOsiDetail_collection: Collection, 
                 prioritneOsiOP_collection: Collection,
                 nezrovnalostDetail_collection: Collection,
                 pohladavkovyDoklad_collection: Collection,
                 intenzitaDetail_collection: Collection,
                 **kwargs):
        url = 'https://opendata.itms2014.sk/v2/prioritnaOs/{poId}'
        super().__init__(prioritneOsiDetail_collection, url, "poId")

        self._related_collections = [
            prioritneOsiOP_collection,
            nezrovnalostDetail_collection,
            pohladavkovyDoklad_collection,
            intenzitaDetail_collection,
        ]

        self._aggregations_by_collection_name  = {
            prioritneOsiOP_collection.name : self.get_most_collection_aggregation(),
            nezrovnalostDetail_collection.name : self.get_most_collection_aggregation(),
            pohladavkovyDoklad_collection.name : self.get_most_collection_aggregation(),
            intenzitaDetail_collection.name : self.get_most_collection_aggregation(),
        }

    def get_most_collection_aggregation(self) -> list[dict]:
        return [
            {
                '$match': {
                    'prioritnaOs': {
                        '$exists': True
                    }
                }
            }, {
                '$project': {
                    self._route_param_name: '$prioritnaOs.id', 
                    '_id': 0
                }
            }
        ]
    
    def get_poId_from_prioritneOsi_aggregation(self) -> list[dict]:
        return [
            {
                '$project': {
                    '_id': 0, 
                    self._route_param_name: '$id'
                }
            }
        ]