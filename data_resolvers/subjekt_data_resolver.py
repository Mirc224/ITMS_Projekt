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
        # url = 'https://opendata.itms2014.sk/v2/dodavatelia/{dodavatelId}'
        # super().__init__(dodavatelia_collection, url, "dodavatelId")
        
        # self._related_collections = [
        #     uctovneDoklady_collection,
        #     verejneObstaravania_collection,
        #     zmluvyVODetail_collection
        # ]

        # self._aggregations_by_collection_name = {
        #     uctovneDoklady_collection.name: self.get_uctovneDoklady_aggregation(),
        #     verejneObstaravania_collection.name: self.get_verejneObstaravania_aggregation(),
        #     zmluvyVODetail_collection.name: self.get_zmluvyVO_aggregation()
        # }
        self._parallel_requests = 1000