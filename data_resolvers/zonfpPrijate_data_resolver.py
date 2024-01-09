from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/zonfp/prijate?minId={minId}
class ZonfpPrijateDataResolver(DataResolverWithMinIdBase):
    def __init__(self, zonfpPrijate_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/zonfp/prijate?minId={minId}'
        super().__init__(zonfpPrijate_collection, url)

# 'https://opendata.itms2014.sk/v2/zonfp/prijate/{zonfpId}'
class ZonfpPrijateDetailDataResolver(DataDetailResolverBase):
    def __init__(self, zonfpPrijateDetail_collection: Collection, zonfpPrijate_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/zonfp/prijate/{zonfpId}'
        super().__init__(zonfpPrijateDetail_collection, url, zonfpPrijate_collection, "id", 'zonfpId')
        self._parallel_requests = 450