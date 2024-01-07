import asyncio
import aiohttp
from aiohttp import ClientSession
from pymongo.collection import Collection
from abc import ABC, abstractmethod
from itertools import batched


class DataResolverBase(ABC):
    def __init__(self, main_collection: Collection, remote_url:str):
        self._main_collection = main_collection
        self._remote_url_template = remote_url
    
    async def resolve_data(self):
        remote_data = await self.get_all_remote_data_async()
        self._main_collection.delete_many({})
        data_to_insert = self.transform_data_to_insert(remote_data)
        self._main_collection.insert_many(data_to_insert)

    async def fetch_all_async(self, list_of_params:list[dict], batch_size:int=0):
        if not batch_size > 0:
            batch_size = len(list_of_params)
        
        results = []
        for batch_of_params in batched(list_of_params, batch_size):
            tasks = []
            async with aiohttp.ClientSession() as session:
                for params in batch_of_params:
                    task = asyncio.create_task(self.fetch_async(session, params))
                    tasks.append(task)
                results.extend(await asyncio.gather(*tasks))
        return results

    async def fetch_async(self, s:ClientSession, params:dict):
        results = []
        while True:
            async with s.get(self._remote_url_template.format(**params)) as r:
                if r.status != 200:
                    r.raise_for_status()
                fetched_data =  await r.json()
                fetched_data = self.transform_fetched_data(fetched_data, **params)
                results.extend(fetched_data)
                if not self.perform_next_fetch(fetched_data):
                    break
                params = self.get_updated_params(fetched_data, params)
        return results
    
    @abstractmethod
    async def get_all_remote_data_async(self):
        pass
    
    def transform_data_to_insert(self, all_data)-> list[dict]:
        result = []
        for data in all_data:
            result.extend(data)
        return result

    def transform_fetched_data(self, fetched_data, **params:dict):
        return fetched_data
    
    @abstractmethod
    def perform_next_fetch(self, fetched_data)->bool:
        pass

    def get_updated_params(self, fetched_data, params:dict)-> dict:
        return params
    

class DataResolverWithMinIdBase(DataResolverBase):
    def __init__(self, main_collection: Collection, remote_url: str):
        assert 'minId={minId}' in remote_url, f"Missing minId query param in route {remote_url}!"
        super().__init__(main_collection, remote_url)

    def perform_next_fetch(self, fetched_data):
        return True if fetched_data else False
    
    def get_updated_params(self, fetched_data, params:dict)-> dict:
        min_id = max(fetched_data, key=lambda item: item["id"])['id']
        params['minId'] = min_id
        return params
    
    async def get_all_remote_data_async(self):
        return await self.fetch_all_async([{ "minId": 0 }])
    

class DataDetailResolverBase(DataResolverBase):
    def __init__(
            self, 
            main_collection: Collection, 
            remote_url: str, 
            related_collection: Collection,
            related_col_key_name: str,
            route_param_name: str):
        assert f"{{{route_param_name}}}" in remote_url, f"Missing {{{route_param_name}}} in route {remote_url}!"
        super().__init__(main_collection, remote_url)
        self._related_collection = related_collection
        self._related_col_key_name = related_col_key_name
        self._route_param_name = route_param_name

    async def get_all_remote_data_async(self):
        list_of_params = self.get_list_of_params()
        return await self.fetch_all_async(list_of_params)
    
    def get_list_of_params(self):
        all_keys = self._related_collection.distinct(self._related_col_key_name)
        list_of_params = []
        for key in all_keys:
            list_of_params.append(
                {
                    self._route_param_name: key
                })
        return list_of_params
    
    def perform_next_fetch(self, fetched_data):
        return False
    
    def transform_fetched_data(self, fetched_data, **params:dict):
        return [fetched_data]