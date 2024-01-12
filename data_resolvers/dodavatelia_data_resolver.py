from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataDetailResolverBase
from pymongo.command_cursor import CommandCursor

class DodavateliaDataResolver(DataDetailResolverBase):
    def __init__(
            self, 
            dodavatelia_collection: Collection,
            uctovneDoklady_collection: Collection,
            verejneObstaravania_collection: Collection,
            zmluvyVODetail_collection: Collection,
            **kwargs):
        url = 'https://opendata.itms2014.sk/v2/dodavatelia/{dodavatelId}'
        super().__init__(dodavatelia_collection, url, None, None, 'dodavatelId')

        self._related_collections = [
            uctovneDoklady_collection,
            verejneObstaravania_collection,
            zmluvyVODetail_collection
        ]

        self._aggregations_by_type_name = {
            uctovneDoklady_collection.name: self.get_uctovneDoklady_aggregation(),
            verejneObstaravania_collection.name: self.get_verejneObstaravania_aggregation(),
            zmluvyVODetail_collection.name: self.get_zmluvyVO_aggregation()
        }
        self._parallel_requests = 1000

    def get_all_keys(self):
        all_ids = set()
        for collection in self._related_collections:
            all_ids |= self.get_key_from_collection(collection)
        return all_ids
    
    def get_key_from_collection(self, collection:Collection) -> set[dict]:
        aggregation = self._aggregations_by_type_name[collection.name]
        result = collection.aggregate(aggregation)
        return set([item[self._route_param_name] for item in result if item])
    
    def get_uctovneDoklady_aggregation(self):
        return [
                {
                    '$match': {
                        'dodavatelDodavatelObstaravatel': {
                            '$exists': True
                        }
                    }
                }, {
                    '$addFields': {
                        self._route_param_name: '$dodavatelDodavatelObstaravatel.id'
                    }
                }, {
                    '$project': {
                        '_id': 0, 
                        self._route_param_name: 1
                    }
                }
            ]
    
    def get_zmluvyVO_aggregation(self):
        return [
            {
                '$addFields': {
                    'dodavatelArr': {
                        '$setUnion': [
                            {
                                '$ifNull': [
                                    {
                                        '$map': {
                                            'input': '$dodavatelia', 
                                            'in': '$$this.dodavatelDodavatelObstaravatel'
                                        }
                                    }, []
                                ]
                            }, {
                                '$filter': {
                                    'input': [
                                        '$hlavnyDodavatelDodavatelObstaravatel'
                                    ], 
                                    'cond': '$$this'
                                }
                            }, {
                                '$filter': {
                                    'input': [
                                        '$verejneObstaravanie.obstaravatelDodavatelObstaravatel'
                                    ], 
                                    'cond': '$$this'
                                }
                            }
                        ]
                    }
                }
            }, {
                '$unwind': {
                    'path': '$dodavatelArr', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$project': {
                    self._route_param_name: '$dodavatelArr.id', 
                    '_id': 0
                }
            }
        ]
    
    def get_verejneObstaravania_aggregation(self):
        return [
            {
                '$match': {
                    'obstaravatelDodavatelObstaravatel': {
                        '$exists': True
                    }
                }
            },
            {
                '$project': {
                    '_id': 0, 
                    self._route_param_name: '$obstaravatelDodavatelObstaravatel.id'
                }
            }
        ]

    

