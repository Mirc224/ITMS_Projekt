from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataDetailResolverBase

# https://opendata.itms2014.sk/v2/polozkaRozpoctu/{polozkaRozpoctuId}
class PolozkaRozpoctuDetailDataResolver(DataDetailResolverBase):
    def __init__(
            self, 
            polozkaRozpoctuDetail_collection: Collection, 
            zopPredlozeneDetail_collection: Collection, 
            zopUhradeneDetail_collection: Collection,
            zopZamietnuteDetail_collection: Collection,
            **kwargs):
        url = 'https://opendata.itms2014.sk/v2/polozkaRozpoctu/{polozkaRozpoctuId}'
        super().__init__(polozkaRozpoctuDetail_collection, url, None, None, 'polozkaRozpoctuId')
        self._zopPredlozeneDetail_collection = zopPredlozeneDetail_collection
        self._zopUhradeneDetail_collection = zopUhradeneDetail_collection
        self._zopZamietnuteDetail_collection = zopZamietnuteDetail_collection
        self._parallel_requests = 100

    async def get_and_store_all_remote_data_async(self):
        all_polozkaRozpoctuId = self.get_polozky_rozpoctu(self._zopPredlozeneDetail_collection)
        all_polozkaRozpoctuId |= self.get_polozky_rozpoctu(self._zopUhradeneDetail_collection)
        all_polozkaRozpoctuId |= self.get_polozky_rozpoctu(self._zopZamietnuteDetail_collection)
        list_of_params = []
        for key in all_polozkaRozpoctuId:
            list_of_params.append(
                {
                    self._route_param_name: key
                })
        return await self.fetch_and_store_all_async(list_of_params)

    
    def get_polozky_rozpoctu(self, collection:Collection) -> set[dict]:
        all_polozkyRozpoctuId_in_collection = collection.aggregate([
            {
                '$unwind': {
                    'path': '$predlozeneDeklarovaneVydavky', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$addFields': {
                    self._route_param_name: '$predlozeneDeklarovaneVydavky.polozkaRozpoctu.id'
                }
            }, {
                '$project': {
                    '_id': 0, 
                    self._route_param_name : 1
                }
            }
        ])
        return set([item[self._route_param_name] for item in all_polozkyRozpoctuId_in_collection])
