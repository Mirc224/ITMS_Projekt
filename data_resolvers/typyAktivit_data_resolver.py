from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/typyAktivit?minId={minId}
class TypyAktivitDataResolver(DataResolverWithMinIdBase):
    def __init__(self, typyAktivit_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/typyAktivit?minId={minId}'
        super().__init__(typyAktivit_collection, url)

# https://opendata.itms2014.sk/v2/typyAktivit/{opId}
class TypyAktivitDetailDataResolver(DataDetailResolverBase):
    def __init__(self, 
                 typyAktivitDetail_collection: Collection, 
                 typyAktivit_collection: Collection,
                 **kwargs):
        url = 'https://opendata.itms2014.sk/v2/typyAktivit/{typAktivityId}'
        super().__init__(typyAktivitDetail_collection, url, typyAktivit_collection, "id", "typAktivityId")