from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/nezrovnalost?minId={minId}
class NezrovnalostDataResolver(DataResolverWithMinIdBase):
    def __init__(self, nezrovnalost_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/nezrovnalost?minId={minId}'
        super().__init__(nezrovnalost_collection, url)

# https://opendata.itms2014.sk/v2/nezrovnalost/{nezrovnalostId}
class NezrovnalostDetailDataResolver(DataDetailResolverBase):
    def __init__(self, 
                 nezrovnalostDetail_collection: Collection, 
                 nezrovnalost_collection: Collection,
                 **kwargs):
        url = 'https://opendata.itms2014.sk/v2/nezrovnalost/{nezrovnalostId}'
        super().__init__(nezrovnalostDetail_collection, url, nezrovnalost_collection, "id", "nezrovnalostId")