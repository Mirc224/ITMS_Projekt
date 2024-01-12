from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataDetailResolverWithAggregationsBase

# https://opendata.itms2014.sk/v2/polozkaRozpoctu/{polozkaRozpoctuId}
class IntenzitaDetailDataResolver(DataDetailResolverWithAggregationsBase):
    def __init__(
            self, 
            intenzitaDetail_collection: Collection, 
            polozkaRozpoctuDetail_collection: Collection, 
            projektyVRealizaciiDetail_collection: Collection, 
            projektyUkonceneDetail_collection: Collection,
            **kwargs):
        url = 'https://opendata.itms2014.sk/v2/intenzita/{intenzitaId}'
        super().__init__(intenzitaDetail_collection, url, 'intenzitaId')

        self._related_collections = [
            polozkaRozpoctuDetail_collection,
            projektyVRealizaciiDetail_collection,
            projektyUkonceneDetail_collection
        ]

        self._aggregations_by_collection_name = {
            polozkaRozpoctuDetail_collection.name: self.get_polozkaRozpoctu_aggregation(),
            projektyVRealizaciiDetail_collection.name: self.get_projekt_aggregation(),
            projektyUkonceneDetail_collection.name: self.get_projekt_aggregation()
        }
        self._parallel_requests = 2500
    
    def get_projekt_aggregation(self) -> list[dict]:
        return [
                {
                    '$unwind': {
                        'path': '$intenzity', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$addFields': {
                        self._route_param_name: '$intenzity.id'
                    }
                }, {
                    '$project': {
                        '_id': 0, 
                        self._route_param_name: 1
                    }
                }
            ]
    
    def get_polozkaRozpoctu_aggregation(self) -> list[dict]:
        return [
                {
                    '$addFields': {
                        self._route_param_name: '$intenzita.id'
                    }
                }, {
                    '$project': {
                        '_id': 0, 
                        self._route_param_name: 1
                    }
                }
            ]
