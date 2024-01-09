from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/zop/predlozene?minId={minId}
class ZopPredlozeneDataResolver(DataResolverWithMinIdBase):
    def __init__(self, zopPredlozene_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/zop/predlozene?minId={minId}'
        super().__init__(zopPredlozene_collection, url)

# 'https://opendata.itms2014.sk/v2/zop/predlozene/{zopId}'
class ZopPredlozeneDetailDataResolver(DataDetailResolverBase):
    def __init__(self, zopPredlozeneDetail_collection: Collection, zopPredlozene_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/zop/predlozene/{zopId}'
        super().__init__(zopPredlozeneDetail_collection, url, zopPredlozene_collection, "id", 'zopId')