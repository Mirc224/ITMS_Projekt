from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataDetailResolverWithAggregationsBase

class SubjektyDataResolver(DataDetailResolverWithAggregationsBase):
    def __init__(
            self, 
            subjekty_collection: Collection,
            nezrovnalostDetail_collection: Collection,
            pohladavkovyDokladDetail_collection: Collection,
            aktivita_collection: Collection,
            intenzitaDetail_collection: Collection,
            polozkaRozpoctuDetail_collection: Collection,
            projektyUkonceneDetail_collection: Collection,
            projektyVRealizaciiDetail_collection: Collection,
            operacneProgramy_collection: Collection,
            uctovneDoklady_collection: Collection,
            verejneObstaravaniaDetail_collection: Collection,
            zmluvyVODetail_collection: Collection,
            vyzvyPlanovaneDetail_collection: Collection,
            vyzvyVyhlaseneDetail_collection: Collection,
            zonfpPrijateDetail_collection: Collection,
            zonfpSchvaleneDetail_collection: Collection,
            zonfpZamietnuteDetail_collection: Collection,
            zopPredlozeneDetail_collection: Collection,
            zopUhradeneDetail_collection: Collection,
            zopZamietnuteDetail_collection: Collection,
            **kwargs):
        url = 'https://opendata.itms2014.sk/v2/subjekty/{subjektId}'
        super().__init__(subjekty_collection, url, "subjektId")
        
        self._related_collections = [
            nezrovnalostDetail_collection,
            pohladavkovyDokladDetail_collection,
            aktivita_collection,
            intenzitaDetail_collection,
            polozkaRozpoctuDetail_collection,
            projektyUkonceneDetail_collection,
            projektyVRealizaciiDetail_collection,
            operacneProgramy_collection,
            uctovneDoklady_collection,
            verejneObstaravaniaDetail_collection,
            zmluvyVODetail_collection,
            vyzvyPlanovaneDetail_collection,
            vyzvyVyhlaseneDetail_collection,
            zonfpPrijateDetail_collection,
            zonfpSchvaleneDetail_collection,
            zonfpZamietnuteDetail_collection,
            zopPredlozeneDetail_collection,
            zopUhradeneDetail_collection,
            zopZamietnuteDetail_collection,
        ]
        zopZamietnuteDetail_collection
        self._aggregations_by_collection_name = {
            nezrovnalostDetail_collection.name : self.get_nezrovnalost_aggregation(),
            pohladavkovyDokladDetail_collection.name : self.get_pohladavkovyDoklad_aggregation(),
            aktivita_collection.name : self.get_simple_subjektId_aggregation(),
            intenzitaDetail_collection.name : self.get_simple_subjektId_aggregation(),
            polozkaRozpoctuDetail_collection.name : self.get_simple_subjektId_aggregation(),
            operacneProgramy_collection.name : self.get_simple_subjektId_aggregation(),
            projektyUkonceneDetail_collection.name : self.get_projekty_aggregation(),
            projektyVRealizaciiDetail_collection.name : self.get_projekty_aggregation(),
            uctovneDoklady_collection.name : self.get_uctovneDoklady_aggregation(),
            verejneObstaravaniaDetail_collection.name : self.get_verejneObstaravania_aggregation(),
            zmluvyVODetail_collection.name : self.get_zmluvyVO_aggregation(),
            vyzvyPlanovaneDetail_collection.name : self.get_vyzvy_aggregation(),
            vyzvyVyhlaseneDetail_collection.name : self.get_vyzvy_aggregation(),
            zonfpPrijateDetail_collection.name : self.get_zonfp_aggregation(),
            zonfpSchvaleneDetail_collection.name : self.get_zonfp_aggregation(),
            zonfpZamietnuteDetail_collection.name : self.get_zonfp_aggregation(),
            zopPredlozeneDetail_collection.name : self.get_zop_aggregation(),
            zopUhradeneDetail_collection.name : self.get_zop_aggregation(),
            zopZamietnuteDetail_collection.name : self.get_zop_aggregation(),
        }
        self._parallel_requests = 1000

    def get_nezrovnalost_aggregation(self) -> list[dict]:
        return [{
                    '$addFields': {
                        'subjektyArr': {
                            '$setUnion': [
                                {
                                    '$ifNull': [
                                        '$subjektyKtoreSposobiliNezrovnalost', []
                                    ]
                                }, {
                                    '$ifNull': [
                                        '$subjektyKtoreZistiliNezrovnalost', []
                                    ]
                                }, {
                                    '$ifNull': [
                                        '$subjektyZodpovedneZaNasledneKonanie', []
                                    ]
                                }, {
                                    '$filter': {
                                        'input': [
                                            '$dlznik'
                                        ], 
                                        'cond': '$$this'
                                    }
                                }
                            ]
                        }
                    }
                }, {
                    '$unwind': {
                        'path': '$subjektyArr'
                    }
                }, {
                    '$project': {
                        '_id': 0, 
                        self._route_param_name: '$subjektyArr.id'
                    }
                }
            ]
    def get_pohladavkovyDoklad_aggregation(self):
        return [
                {
                    '$match': {
                        'subjektZodpovednyZaVymahanie': {
                            '$exists': 0
                        }
                    }
                }, {
                    '$addFields': {
                        'subjektyArr': {
                            '$setUnion': [
                                {
                                    '$filter': {
                                        'input': [
                                            '$dlznik'
                                        ], 
                                        'cond': '$$this'
                                    }
                                }, {
                                    '$filter': {
                                        'input': [
                                            '$subjektZodpovednyZaVymahanie'
                                        ], 
                                        'cond': '$$this'
                                    }
                                }
                            ]
                        }
                    }
                }, {
                    '$unwind': {
                        'path': '$subjektyArr'
                    }
                }, {
                    '$project': {
                        '_id': 0, 
                        self._route_param_name: '$subjektyArr.id'
                    }
                }
            ]
    
    def get_simple_subjektId_aggregation(self) -> list[dict]:
        return [
                {
                    '$match': {
                        'subjekt': {
                            '$exists': 1
                        }
                    }
                }, {
                    '$project': {
                        '_id': 0, 
                        self._route_param_name: '$subjekt.id'
                    }
                }
            ]
    
    def get_projekty_aggregation(self) -> list[dict]:
        return [
                {
                    '$addFields': {
                        'subjektyArr': {
                            '$setUnion': [
                                {
                                    '$ifNull': [
                                        '$partneri', []
                                    ]
                                }, {
                                    '$ifNull': [
                                        {
                                            '$reduce': {
                                                'input': '$partneri.predchodcovia', 
                                                'initialValue': [], 
                                                'in': {
                                                    '$concatArrays': [
                                                        '$$value', '$$this'
                                                    ]
                                                }
                                            }
                                        }, []
                                    ]
                                }, {
                                    '$filter': {
                                        'input': [
                                            '$prijimatel'
                                        ], 
                                        'cond': '$$this'
                                    }
                                }, {
                                    '$ifNull': [
                                        '$prijimatel.predchodcovia', []
                                    ]
                                }
                            ]
                        }
                    }
                }, {
                    '$unwind': {
                        'path': '$subjektyArr'
                    }
                }, {
                    '$project': {
                        '_id': 0, 
                        self._route_param_name: '$subjektyArr.subjekt.id'
                    }
                }
            ]
    def get_uctovneDoklady_aggregation(self) -> list[dict]:
        return [
                {
                    '$addFields': {
                        'subjektyArr': {
                            '$setUnion': [
                                {
                                    '$filter': {
                                        'input': [
                                            '$dodavatelSubjekt'
                                        ], 
                                        'cond': '$$this'
                                    }
                                }, {
                                    '$filter': {
                                        'input': [
                                            '$vlastnikDokladu'
                                        ], 
                                        'cond': '$$this'
                                    }
                                }
                            ]
                        }
                    }
                }, {
                    '$unwind': {
                        'path': '$subjektyArr'
                    }
                }, {
                    '$project': {
                        '_id': 0, 
                        self._route_param_name: '$subjektyArr.id'
                    }
                }
            ]
    
    def get_verejneObstaravania_aggregation(self) -> list[dict]:
        return [
                {
                    '$addFields': {
                        'subjektyArr': {
                            '$setUnion': [
                                {
                                    '$filter': {
                                        'input': [
                                            '$obstaravatelSubjekt'
                                        ], 
                                        'cond': '$$this'
                                    }
                                }, {
                                    '$filter': {
                                        'input': [
                                            '$zadavatel'
                                        ], 
                                        'cond': '$$this'
                                    }
                                }
                            ]
                        }
                    }
                }, {
                    '$unwind': {
                        'path': '$subjektyArr'
                    }
                }, {
                    '$project': {
                        '_id': 0, 
                        self._route_param_name: '$subjektyArr.subjekt.id'
                    }
                }
            ]
    def get_zmluvyVO_aggregation(self) -> list[dict]:
        return [
                {
                    '$addFields': {
                        'subjektyArr': {
                            '$filter': {
                                'input': {
                                    '$setUnion': [
                                        [
                                            '$hlavnyDodavatelSubjekt'
                                        ], {
                                            '$map': {
                                                'input': {
                                                    '$ifNull': [
                                                        '$dodavatelia', []
                                                    ]
                                                }, 
                                                'in': '$$this.dodavatelSubjekt'
                                            }
                                        }, [
                                            '$verejneObstaravanie.obstaravatelSubjekt'
                                        ], [
                                            '$verejneObstaravanie.zadavatel.id'
                                        ]
                                    ]
                                }, 
                                'cond': '$$this'
                            }
                        }
                    }
                }, {
                    '$unwind': {
                        'path': '$subjektyArr'
                    }
                }, {
                    '$project': {
                        '_id': 0, 
                        self._route_param_name: '$subjektyArr.id'
                    }
                }
            ]
    
    def get_vyzvy_aggregation(self) -> list[dict]:
        return [
                {
                    '$addFields': {
                        'subjektyArr': {
                            '$filter': {
                                'input': {
                                    '$setUnion': [
                                        {
                                            '$ifNull': [
                                                '$poskytovatelia', []
                                            ]
                                        }, [
                                            '$vyhlasovatel'
                                        ]
                                    ]
                                }, 
                                'cond': '$$this'
                            }
                        }
                    }
                }, {
                    '$unwind': {
                        'path': '$subjektyArr'
                    }
                }, {
                    '$project': {
                        '_id': 0, 
                        self._route_param_name: '$subjektyArr.id'
                    }
                }
            ]
    
    def get_zonfp_aggregation(self) -> list[dict]:
        return [
                {
                    '$addFields': {
                        'subjektyArr': {
                            '$filter': {
                                'input': {
                                    '$setUnion': [
                                        {
                                            '$ifNull': [
                                                '$partneri', []
                                            ]
                                        }, {
                                            '$ifNull': [
                                                {
                                                    '$reduce': {
                                                        'input': '$partneri.predchodcovia', 
                                                        'initialValue': [], 
                                                        'in': {
                                                            '$concatArrays': [
                                                                '$$value', '$$this'
                                                            ]
                                                        }
                                                    }
                                                }, []
                                            ]
                                        }, [
                                            '$ziadatel'
                                        ], {
                                            '$ifNull': [
                                                '$ziadatel.predchodcovia', []
                                            ]
                                        }, {
                                            '$ifNull': [
                                                '$aktivityProjekt', []
                                            ]
                                        }
                                    ]
                                }, 
                                'cond': '$$this'
                            }
                        }
                    }
                }, {
                    '$unwind': {
                        'path': '$subjektyArr'
                    }
                }, {
                    '$project': {
                        '_id': 0, 
                        self._route_param_name: '$subjektyArr.subjekt.id'
                    }
                }
            ]
    
    def get_zop_aggregation(self) -> list[dict]:
        return [
                {
                    '$match': {
                        'predkladanaZa': {
                            '$exists': 0
                        }
                    }
                }, {
                    '$addFields': {
                        'subjektyArr': {
                            '$filter': {
                                'input': {
                                    '$setUnion': [
                                        {
                                            '$map': {
                                                'input': {
                                                    '$ifNull': [
                                                        '$predkladanaZaSubjekty', []
                                                    ]
                                                }, 
                                                'in': '$$this.subjekt'
                                            }
                                        }, [
                                            '$predkladanaZa'
                                        ], [
                                            '$prijimatel'
                                        ], [
                                            '$hlavnyCehranicnyPartner'
                                        ]
                                    ]
                                }, 
                                'cond': '$$this'
                            }
                        }
                    }
                }, {
                    '$unwind': {
                        'path': '$subjektyArr'
                    }
                }, {
                    '$project': {
                        '_id': 0, 
                        self._route_param_name: '$subjektyArr.id'
                    }
                }
            ]
