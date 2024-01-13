from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/zonfp/zamietnute?minId={minId}
class ZonfpZamietnuteDataResolver(DataResolverWithMinIdBase):
    def __init__(self, zonfpZamietnute_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/zonfp/zamietnute?minId={minId}'
        super().__init__(zonfpZamietnute_collection, url)

# 'https://opendata.itms2014.sk/v2/zonfp/zamietnute/{zonfpId}'
class ZonfpZamietnuteDetailDataResolver(DataDetailResolverBase):
    def __init__(self, zonfpZamietnuteDetail_collection: Collection, zonfpZamietnute_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/zonfp/zamietnute/{zonfpId}'
        super().__init__(zonfpZamietnuteDetail_collection, url, zonfpZamietnute_collection, "id", 'zonfpId')