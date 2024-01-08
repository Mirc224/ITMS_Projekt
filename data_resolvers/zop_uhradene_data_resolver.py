from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/zop/uhradene?minId={minId}
class ZopUhradeneDataResolver(DataResolverWithMinIdBase):
    def __init__(self, zopUhradene_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/zop/uhradene?minId={minId}'
        super().__init__(zopUhradene_collection, url)

# 'https://opendata.itms2014.sk/v2/zop/uhradene/{zopId}'
class ZopUhradeneDetailDataResolver(DataDetailResolverBase):
    def __init__(self, zopUhradeneDetail_collection: Collection, zopUhradene_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/zop/uhradene/{zopId}'
        super().__init__(zopUhradeneDetail_collection, url, zopUhradene_collection, "id", 'zopId')
        self._parallel_requests = 2000