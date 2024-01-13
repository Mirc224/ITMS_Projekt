from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/verejneObstaravania?minId={minId}
class VerejneObstaravaniaDataResolver(DataResolverWithMinIdBase):
    def __init__(self, verejneObstaravania_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/verejneObstaravania?minId={minId}'
        super().__init__(verejneObstaravania_collection, url)

# https://opendata.itms2014.sk/v2/verejneObstaravania/{obstaravanieId}
class VerejneObstaravaniaDetailDataResolver(DataDetailResolverBase):
    def __init__(self, verejneObstaravaniaDetail_collection: Collection, verejneObstaravania_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/verejneObstaravania/{obstaravanieId}'
        super().__init__(verejneObstaravaniaDetail_collection, url, verejneObstaravania_collection, "id", 'obstaravanieId')