from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/zonfp/schvalene?minId={minId}
class ZonfpSchvaleneDataResolver(DataResolverWithMinIdBase):
    def __init__(self, zonfpSchvalene_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/zonfp/schvalene?minId={minId}'
        super().__init__(zonfpSchvalene_collection, url)

# 'https://opendata.itms2014.sk/v2/zonfp/schvalene/{zonfpId}'
class ZonfpSchvaleneDetailDataResolver(DataDetailResolverBase):
    def __init__(self, zonfpSchvaleneDetail_collection: Collection, zonfpSchvalene_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/zonfp/prijate/{zonfpId}'
        super().__init__(zonfpSchvaleneDetail_collection, url, zonfpSchvalene_collection, "id", 'zonfpId')