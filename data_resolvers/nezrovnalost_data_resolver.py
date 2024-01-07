from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/nezrovnalost?minId={minId}
class NezrovnalostDataResolver(DataResolverWithMinIdBase):
    def __init__(self, main_collection: Collection, remote_url: str):
        super().__init__(main_collection, remote_url)

# https://opendata.itms2014.sk/v2/nezrovnalost/{nezrovnalostId}
class NezrovnalostDetailDataResolver(DataDetailResolverBase):
    def __init__(self, 
                 main_collection: Collection, 
                 remote_url: str, 
                 related_collection: Collection, 
                 related_col_key_name: str, 
                 route_param_name: str):
        super().__init__(main_collection, remote_url, related_collection, related_col_key_name, route_param_name)