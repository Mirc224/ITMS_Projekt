from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/prioritnaOs/{poId}/konkretneCiele?minId={minId}
class KonkretneCieleDataResolver(DataResolverWithMinIdBase):
    def __init__(self, 
                konkretneCiele_collection: Collection,
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
        url = 'https://opendata.itms2014.sk/v2/prioritnaOs/{poId}/konkretneCiele?minId={minId}'
        super().__init__(konkretneCiele_collection, url)
        self._nezrovnalostDetail_collection = nezrovnalostDetail_collection
        self._pohladavkovyDoklad_collection = pohladavkovyDoklad_collection
        self._projektyUkonceneDetail_collection = projektyUkonceneDetail_collection
        self._projektyVRealizaciiDetail_collection = projektyVRealizaciiDetail_collection
        self._zonfpPrijateDetail_collection = zonfpPrijateDetail_collection
        self._zonfpSchvaleneDetail_collection = zonfpSchvaleneDetail_collection
        self._zonfpZamietnuteDetail_collection = zonfpZamietnuteDetail_collection
        self._vyzvyPlanovane_collection = vyzvyPlanovane_collection
        self._vyzvyVyhlasene_collection = vyzvyVyhlasene_collection


    async def get_and_store_all_remote_data_async(self):
        poId_field_name = 'poId'
        all_poId = self._prioritneOsi_collection.distinct("id")
        list_of_params = []
        for poId in all_poId:
            list_of_params.append({poId_field_name: poId, 'minId':0})
        return await self.fetch_and_store_all_async(list_of_params)

# https://opendata.itms2014.sk/v2/konkretnyCiel/{kcId}
class KonkretneCieleDetailDataResolver(DataDetailResolverBase):
    def __init__(self, 
                 konkretneCieleDetail_collection: Collection, 
                 konkretneCiele_collection: Collection,
                 **kwargs):
        url = 'https://opendata.itms2014.sk/v2/konkretnyCiel/{kcId}'
        super().__init__(konkretneCieleDetail_collection, url, konkretneCiele_collection, "id", "kcId")
