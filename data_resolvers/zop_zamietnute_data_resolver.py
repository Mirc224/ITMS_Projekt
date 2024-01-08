from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/zop/zamietnute?minId={minId}
class ZopZamietnuteDataResolver(DataResolverWithMinIdBase):
    def __init__(self, zopZamietnute_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/zop/zamietnute?minId={minId}'
        super().__init__(zopZamietnute_collection, url)

# 'https://opendata.itms2014.sk/v2/zop/zamietnute/{zopId}'
class ZopZamietnuteDetailDataResolver(DataDetailResolverBase):
    def __init__(self, zopZamietnuteDetail_collection: Collection, zopZamietnute_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/zop/zamietnute/{zopId}'
        super().__init__(zopZamietnuteDetail_collection, url, zopZamietnute_collection, "id", 'zopId')