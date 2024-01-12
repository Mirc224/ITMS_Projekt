from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverWithAggregationsBase

# https://opendata.itms2014.sk/v2/prioritnaOs/{poId}/konkretneCiele?minId={minId}
class KonkretneCielePOsDataResolver(DataResolverWithMinIdBase):
    def __init__(self, 
                konkretneCielePOs_collection: Collection,
                prioritneOsiDetail_collection: Collection,
                **kwargs):
        url = 'https://opendata.itms2014.sk/v2/prioritnaOs/{poId}/konkretneCiele?minId={minId}'
        super().__init__(konkretneCielePOs_collection, url)
        self._poId_field_name = 'poId'
        self._prioritneOsi_collection = prioritneOsiDetail_collection
    
    def  get_all_keys(self) -> set:
        return self._prioritneOsi_collection.distinct("id")
    
    def get_params_based_on_key(self, key) -> dict:
        return {self._poId_field_name : key}

# https://opendata.itms2014.sk/v2/konkretnyCiel/{kcId}
class KonkretneCieleDetailDataResolver(DataDetailResolverWithAggregationsBase):
    def __init__(self, 
                 konkretneCieleDetail_collection: Collection,
                 konkretneCielePOs_collection: Collection,
                 nezrovnalostDetail_collection: Collection,
                 pohladavkovyDoklad_collection: Collection,
                 projektyUkonceneDetail_collection: Collection,
                 projektyVRealizaciiDetail_collection: Collection,
                 zonfpPrijateDetail_collection: Collection,
                 zonfpSchvaleneDetail_collection: Collection,
                 zonfpZamietnuteDetail_collection: Collection,
                 vyzvyPlanovane_collection: Collection,
                 vyzvyVyhlasene_collection: Collection,
                 **kwargs):
        url = 'https://opendata.itms2014.sk/v2/konkretnyCiel/{kcId}'
        super().__init__(konkretneCieleDetail_collection, url, "kcId")
        
        self._related_collections = [
            konkretneCielePOs_collection,
            nezrovnalostDetail_collection,
            pohladavkovyDoklad_collection,
            projektyUkonceneDetail_collection,
            projektyVRealizaciiDetail_collection,
            zonfpPrijateDetail_collection,
            zonfpSchvaleneDetail_collection,
            zonfpZamietnuteDetail_collection,
            vyzvyPlanovane_collection,
            vyzvyVyhlasene_collection,
        ]

        self._aggregations_by_collection_name = {
            konkretneCielePOs_collection.name: self.get_konkretneCielePOs_aggregation(),
            nezrovnalostDetail_collection.name: self.get_nezrovnalost_or_pohladavkovyDoklad_aggregation(),
            pohladavkovyDoklad_collection.name: self.get_nezrovnalost_or_pohladavkovyDoklad_aggregation(),
            projektyUkonceneDetail_collection.name: self.get_projekty_or_zonfp_aggregation(),
            projektyVRealizaciiDetail_collection.name: self.get_projekty_or_zonfp_aggregation(),
            zonfpPrijateDetail_collection.name: self.get_projekty_or_zonfp_aggregation(),
            zonfpSchvaleneDetail_collection.name: self.get_projekty_or_zonfp_aggregation(),
            zonfpZamietnuteDetail_collection.name: self.get_projekty_or_zonfp_aggregation(),
            vyzvyPlanovane_collection.name: self.get_vyzvy_aggregation(),
            vyzvyVyhlasene_collection.name: self.get_vyzvy_aggregation()
        }

    def get_konkretneCielePOs_aggregation(self) -> list[dict]:
        return [
            {
                '$project': {
                    '_id': 0, 
                    self._route_param_name: '$id'
                }
            }
        ] 
    
    def get_nezrovnalost_or_pohladavkovyDoklad_aggregation(self) -> list[dict]:
        return [
            {
                '$match': {
                    'konkretnyCiel': {
                        '$exists': True
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    self._route_param_name: '$konkretnyCiel.id'
                }
            }
        ]
    
    def get_projekty_or_zonfp_aggregation(self) -> list[dict]:
        return [
                {
                    '$addFields': {
                        'cieleArr': {
                            '$setUnion': [
                                {
                                    '$ifNull': [
                                        '$formyFinancovania', []
                                    ]
                                }, {
                                    '$ifNull': [
                                        '$hospodarskeCinnosti', []
                                    ]
                                }, {
                                    '$ifNull': [
                                        '$oblastiIntervencie', []
                                    ]
                                }, {
                                    '$ifNull': [
                                        '$sekundarnyTematickyOkruh', []
                                    ]
                                }, {
                                    '$ifNull': [
                                        '$typyUzemia', []
                                    ]
                                }, {
                                    '$ifNull': [
                                        '$uzemneMechanizmy', []
                                    ]
                                }
                            ]
                        }
                    }
                }, {
                    '$unwind': {
                        'path': '$cieleArr'
                    }
                }, {
                    '$project': {
                        '_id': 0, 
                        self._route_param_name: '$cieleArr.konkretnyCiel.id'
                    }
                }
            ]
    def get_vyzvy_aggregation(self) -> list[dict]:
        return [
            {
                '$addFields': {
                    'cieleArr': {
                        '$setUnion': [
                            {
                                '$ifNull': [
                                    '$konkretneCiele', []
                                ]
                            }
                        ]
                    }
                }
            }, {
                '$unwind': {
                    'path': '$cieleArr'
                }
            }, {
                '$project': {
                    '_id': 0, 
                    self._route_param_name: '$cieleArr.id'
                }
            }
        ]
