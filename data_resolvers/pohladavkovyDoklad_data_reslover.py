from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataDetailResolverBase, DataResolverBase, DataResolverWithMinIdBase

# https://opendata.itms2014.sk/v2/pohladavkovyDoklad?minId={minId}
class PohladavkovyDokladDataResolver(DataResolverWithMinIdBase):
    def __init__(self, main_collection: Collection, remote_url: str):
        super().__init__(main_collection, remote_url)

# https://opendata.itms2014.sk/v2/pohladavkovyDoklad/{pohladavkaId}
class PohladavkovyDokladDetailDataResolver(DataDetailResolverBase):
    def __init__(self, main_collection: Collection, remote_url: str, related_collection: Collection, related_col_key_name: str, route_param_name: str):
        super().__init__(main_collection, remote_url, related_collection, related_col_key_name, route_param_name)
