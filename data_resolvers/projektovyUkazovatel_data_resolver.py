from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/projektovyUkazovatel?minId={minId}
class ProjektovyUkazovatelDataResolver(DataResolverWithMinIdBase):
    def __init__(self, projektovyUkazovatel_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/projektovyUkazovatel?minId={minId}'
        super().__init__(projektovyUkazovatel_collection, url)

# https://opendata.itms2014.sk/v2/projektovyUkazovatel/{ukazovatelId}
class ProjektovyUkazovatelDetailDataResolver(DataDetailResolverBase):
    def __init__(self, projektovyUkazovatelDetail_collection: Collection, projektovyUkazovatel_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/projektovyUkazovatel/{ukazovatelId}'
        super().__init__(projektovyUkazovatelDetail_collection, url, projektovyUkazovatel_collection, "id", 'ukazovatelId')