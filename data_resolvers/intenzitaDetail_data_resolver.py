from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataDetailResolverBase

# https://opendata.itms2014.sk/v2/polozkaRozpoctu/{polozkaRozpoctuId}
class IntenzitaDetailDataResolver(DataDetailResolverBase):
    def __init__(
            self, 
            intenzitaDetail_collection: Collection, 
            polozkaRozpoctuDetail_collection: Collection, 
            projektyVRealizaciiDetail_collection: Collection, 
            projektyUkonceneDetail_collection: Collection,
            **kwargs):
        url = 'https://opendata.itms2014.sk/v2/intenzita/{intenzitaId}'
        super().__init__(intenzitaDetail_collection, url, None, None, 'intenzitaId')
        self._projektyUkonceneDetail_collection = projektyUkonceneDetail_collection
        self._projektyVRealizaciiDetail_collection = projektyVRealizaciiDetail_collection
        self._polozkaRozpoctuDetail_collection = polozkaRozpoctuDetail_collection
        self._parallel_requests = 3000
    
    def get_all_keys(self) -> set:
        all_intenzitaId = self.get_intenzitaId_from_projekt(self._projektyVRealizaciiDetail_collection)
        all_intenzitaId |= self.get_intenzitaId_from_projekt(self._projektyUkonceneDetail_collection)
        all_intenzitaId |= self.get_intenzitaId_from_polozkaRozpoctu(self._polozkaRozpoctuDetail_collection)
        return all_intenzitaId
    
    def get_intenzitaId_from_projekt(self, collection:Collection) -> set[dict]:
        all_polozkyRozpoctuId_in_collection = collection.aggregate([
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
            ])
        return set([item[self._route_param_name] for item in all_polozkyRozpoctuId_in_collection])
    
    def get_intenzitaId_from_polozkaRozpoctu(self, collection:Collection) -> set[dict]:
        all_intenzitaId_in_collection = collection.aggregate([
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
            ])
        return set([item[self._route_param_name] for item in all_intenzitaId_in_collection])

