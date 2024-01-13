from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/projekty/vrealizacii?minId={minId}
class ProjektyVRealizaciiDataResolver(DataResolverWithMinIdBase):
    def __init__(self, projektyVRealizacii_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/projekty/vrealizacii?minId={minId}'
        super().__init__(projektyVRealizacii_collection, url)

# https://opendata.itms2014.sk/v2/projekty/vrealizacii/{projektId}
class ProjektyVRealizaciiDetailDataResolver(DataDetailResolverBase):
    def __init__(self, projektyVRealizaciiDetail_collection: Collection, projektyVRealizacii_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/projekty/vrealizacii/{projektId}'
        super().__init__(projektyVRealizaciiDetail_collection, url, projektyVRealizacii_collection, "id", 'projektId')