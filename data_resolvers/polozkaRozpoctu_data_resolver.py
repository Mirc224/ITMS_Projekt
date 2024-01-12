from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataDetailResolverWithAggregationsBase

# https://opendata.itms2014.sk/v2/polozkaRozpoctu/{polozkaRozpoctuId}
class PolozkaRozpoctuDetailDataResolver(DataDetailResolverWithAggregationsBase):
    def __init__(
            self, 
            polozkaRozpoctuDetail_collection: Collection, 
            projektyUkonceneDetail_collection: Collection,
            projektyVRealizaciiDetail_collection: Collection,
            zopPredlozeneDetail_collection: Collection,
            zopUhradeneDetail_collection: Collection,
            zopZamietnuteDetail_collection: Collection,
            **kwargs):
        url = 'https://opendata.itms2014.sk/v2/polozkaRozpoctu/{polozkaRozpoctuId}'
        super().__init__(polozkaRozpoctuDetail_collection, url, 'polozkaRozpoctuId')
        
        self._related_collections = [
            projektyUkonceneDetail_collection,
            projektyVRealizaciiDetail_collection,
            zopPredlozeneDetail_collection,
            zopUhradeneDetail_collection,
            zopZamietnuteDetail_collection
        ]

        self._aggregations_by_collection_name  = {
            projektyUkonceneDetail_collection.name: self.get_polozkaRozpoctuId_from_projekt_agg(),
            projektyVRealizaciiDetail_collection.name: self.get_polozkaRozpoctuId_from_projekt_agg(),
            zopPredlozeneDetail_collection.name: self.get_polozkaRozpoctuId_from_zop_agg(),
            zopUhradeneDetail_collection.name: self.get_polozkaRozpoctuId_from_zop_agg(),
            zopZamietnuteDetail_collection.name: self.get_polozkaRozpoctuId_from_zop_agg()
        }
        self._parallel_requests = 100
    
    def get_polozkaRozpoctuId_from_projekt_agg(self)->list[dict]:
        return [
            {
                '$unwind': {
                    'path': '$polozkyRozpoctu'
                }
            }, {
                '$project': {
                    '_id': 0, 
                    self._route_param_name: '$polozkyRozpoctu.id'
                }
            }
        ]
    
    def get_polozkaRozpoctuId_from_zop_agg(self)->list[dict]:
        return [
            {
                '$unwind': {
                    'path': '$predlozeneDeklarovaneVydavky'
                }
            }, {
                '$project': {
                    '_id': 0, 
                    self._route_param_name: '$predlozeneDeklarovaneVydavky.polozkaRozpoctu.id'
                }
            }
        ]

