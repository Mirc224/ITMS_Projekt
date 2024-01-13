from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/uctovneDoklady?minId={minId}
class UctovneDokladyDataResolver(DataResolverWithMinIdBase):
    def __init__(self, uctovneDoklady_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/uctovneDoklady?minId={minId}'
        super().__init__(uctovneDoklady_collection, url)

# 'https://opendata.itms2014.sk/v2/uctovneDoklady/{dokladId}'
class UctovneDokladyDetailDataResolver(DataDetailResolverBase):
    def __init__(self, uctovneDokladyDetail_collection: Collection, uctovneDoklady_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/uctovneDoklady/{dokladId}'
        super().__init__(uctovneDokladyDetail_collection, url, uctovneDoklady_collection, "id", 'dokladId')