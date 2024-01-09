from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/vyzvy/planovane?minId={minId}
class VyzvyPlanovaneDataResolver(DataResolverWithMinIdBase):
    def __init__(self, vyzvyPlanovane_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/vyzvy/planovane?minId={minId}'
        super().__init__(vyzvyPlanovane_collection, url)

# https://opendata.itms2014.sk/v2/vyzvy/planovane/{vyzvaId}
class VyzvyPlanovaneDetailDataResolver(DataDetailResolverBase):
    def __init__(self, vyzvyPlanovaneDetail_collection: Collection, vyzvyPlanovane_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/vyzvy/planovane/{vyzvaId}'
        super().__init__(vyzvyPlanovaneDetail_collection, url, vyzvyPlanovane_collection, "id", 'vyzvaId')