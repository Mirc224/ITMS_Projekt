from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/operacneProgramy?minId={minId}
class OperacneProgramyDataResolver(DataResolverWithMinIdBase):
    def __init__(self, operacneProgramy_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/operacneProgramy?minId={minId}'
        super().__init__(operacneProgramy_collection, url)

# https://opendata.itms2014.sk/v2/operacneProgramy/{opId}
class OperacneProgramyDetailDataResolver(DataDetailResolverBase):
    def __init__(self, 
                 operacneProgramyDetail_collection: Collection, 
                 operacneProgramy_collection: Collection,
                 **kwargs):
        url = 'https://opendata.itms2014.sk/v2/operacneProgramy/{opId}'
        super().__init__(operacneProgramyDetail_collection, url, operacneProgramy_collection, "id", "opId")