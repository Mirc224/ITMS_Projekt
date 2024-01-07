from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataDetailResolverBase, DataResolverBase, DataResolverWithMinIdBase

# https://opendata.itms2014.sk/v2/pohladavkovyDoklad?minId={minId}
class PohladavkovyDokladDataResolver(DataResolverWithMinIdBase):
    def __init__(self, pohladavkovyDoklad_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/pohladavkovyDoklad?minId={minId}'
        super().__init__(pohladavkovyDoklad_collection, url)

# https://opendata.itms2014.sk/v2/pohladavkovyDoklad/{pohladavkaId}
class PohladavkovyDokladDetailDataResolver(DataDetailResolverBase):
    def __init__(self, pohladavkovyDokladDetail_collection: Collection, pohladavkovyDoklad_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/pohladavkovyDoklad/{pohladavkaId}'
        super().__init__(pohladavkovyDokladDetail_collection, url, pohladavkovyDoklad_collection, 'id', 'pohladavkaId')
