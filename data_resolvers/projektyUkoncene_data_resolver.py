from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/projekty/ukoncene?minId={minId}
class ProjektyUkonceneDataResolver(DataResolverWithMinIdBase):
    def __init__(self, projektyUkoncene_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/projekty/ukoncene?minId={minId}'
        super().__init__(projektyUkoncene_collection, url)

# https://opendata.itms2014.sk/v2/projekty/ukoncene/{projektId}
class ProjektyUkonceneDetailDataResolver(DataDetailResolverBase):
    def __init__(self, projektyUkonceneDetail_collection: Collection, projektyUkoncene_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/projekty/ukoncene/{projektId}'
        super().__init__(projektyUkonceneDetail_collection, url, projektyUkoncene_collection, "id", 'projektId')
