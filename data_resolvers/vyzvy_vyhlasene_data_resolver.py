from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/vyzvy/vyhlasene?minId={minId}
class VyzvyVyhlaseneDataResolver(DataResolverWithMinIdBase):
    def __init__(self, vyzvyVyhlasene_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/vyzvy/vyhlasene?minId={minId}'
        super().__init__(vyzvyVyhlasene_collection, url)

# https://opendata.itms2014.sk/v2/vyzvy/vyhlasene/{vyzvaId}
class VyzvyVyhlaseneDetailDataResolver(DataDetailResolverBase):
    def __init__(self, vyzvyVyhlaseneDetail_collection: Collection, vyzvyVyhlasene_collection: Collection, **kwargs):
        url = 'https://opendata.itms2014.sk/v2/vyzvy/vyhlasene/{vyzvaId}'
        super().__init__(vyzvyVyhlaseneDetail_collection, url, vyzvyVyhlasene_collection, "id", 'vyzvaId')