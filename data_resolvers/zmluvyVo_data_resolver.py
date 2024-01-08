from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataDetailResolverBase

# https://opendata.itms2014.sk/v2/verejneObstaravania/{verejneObstaravanieId}/zmluvyVerejneObstaravanie?minId={minId}
# minId na tento endpoint nefunguje, vzdy vrati []
class ZmluvyVODataResolver(DataDetailResolverBase):
    def __init__(self, zmluvyVO_collection: Collection, verejneObstaravania_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/verejneObstaravania/{verejneObstaravanieId}/zmluvyVerejneObstaravanie'
        self._voId_field_name = 'verejneObstaravanieId'
        super().__init__(zmluvyVO_collection, url, verejneObstaravania_collection, "id", self._voId_field_name)
        self._verejneObstravania_collection = verejneObstaravania_collection
        self._parallel_requests = 2500
    
    def transform_fetched_data(self, fetched_data, verejneObstaravanieId:int, **params:dict):
        return [{self._voId_field_name : verejneObstaravanieId} | item for item in fetched_data]
    
# 'https://opendata.itms2014.sk/v2/zmluvaVerejneObstaravanie/{zmluvaId}'
class ZmluvyVODetailDataResolver(DataDetailResolverBase):
    def __init__(self, zmluvyVODetail_collection: Collection, zmluvyVO_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/zmluvaVerejneObstaravanie/{zmluvaId}'
        super().__init__(zmluvyVODetail_collection, url, zmluvyVO_collection, "id", 'zmluvaId')
        self._parallel_requests = 250