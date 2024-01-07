from pymongo.collection import Collection
from data_resolvers.data_resolver_base import DataResolverWithMinIdBase, DataDetailResolverBase

# https://opendata.itms2014.sk/v2/aktivita
class AktivitaDataResolver(DataResolverWithMinIdBase):
    def __init__(self, main_collection: Collection, remote_url: str):
        super().__init__(main_collection, remote_url)


# Robí problémy, ale vyzerá to tak, že nie je potrebne, lebo aktivita, ziska vsetky a detail nema dodatocne info
# https://opendata.itms2014.sk/v2/aktivita/{aktivitaId}
class AktivitaDetailDataResolver(DataDetailResolverBase):
    def __init__(self, main_collection: Collection, remote_url: str, related_collection: Collection, related_col_key_name: str, route_param_name: str):
        super().__init__(main_collection, remote_url, related_collection, related_col_key_name, route_param_name)

    async def get_all_remote_data_async(self):
        all_keys = self._related_collection.distinct(self._related_col_key_name)
        list_of_params = []
        for key in all_keys:
            list_of_params.append(
                {
                    self._route_param_name: key
                })
        return await self.fetch_all_async(list_of_params)