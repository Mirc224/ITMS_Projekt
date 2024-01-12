import asyncio
import aiohttp
from aiohttp import ClientSession
from pymongo.collection import Collection
from abc import ABC, abstractmethod
from itertools import batched
from time import perf_counter
from pymongo.command_cursor import CommandCursor
import logging

class DataResolverBase(ABC):
    def __init__(self, main_collection: Collection, remote_url:str):
        self._main_collection = main_collection
        self._remote_url_template = remote_url
        self._parallel_requests = -1

    def delete_local_data(self):
        self._main_collection.delete_many({})
    
    def insert_data(self, data:list[dict]):
        if not data:
            return
        self._main_collection.insert_many(data)
    
    async def resolve_data(self):
        self.delete_local_data()
        await self.get_and_store_all_remote_data_async()

    async def fetch_and_store_all_async(self, list_of_params:list[dict]):
        logging.info(f"{self._main_collection.name} - Získavanie dát...")
        start = perf_counter()
        batch_size = self._parallel_requests if self._parallel_requests > 0 else len(list_of_params)
        
        completed_requests = 0
        total_requests = len(list_of_params)
        for batch_of_params in batched(list_of_params, batch_size):
            tasks = []
            async with aiohttp.ClientSession() as session:
                for params in batch_of_params:
                    task = asyncio.create_task(self.fetch_async(session, params))
                    tasks.append(task)
                batch_data = await asyncio.gather(*tasks)
            data_to_insert = self.transform_data_to_insert(batch_data)
            self.insert_data(data_to_insert)

            completed_requests += len(batch_of_params)
            logging.info(f"{self._main_collection.name} - Spracovaných je {((completed_requests / total_requests)*100):.2f}%")
        stop = perf_counter()
        logging.info(f'{self._main_collection.name} - Ziskavanie dát trvalo: {stop - start}')

    async def fetch_async(self, s:ClientSession, params:dict):
        results = []
        while True:
            async with s.get(self._remote_url_template.format(**params)) as r:
                if r.status == 404:
                    logging.warning(f'NOT_FOUND: {r.url}' )
                    return results
                if r.status != 200:
                    r.raise_for_status()
                fetched_data =  await r.json()
                fetched_data = self.transform_fetched_data(fetched_data, **params)
                results.extend(fetched_data)
                if not self.perform_next_fetch(fetched_data):
                    break
                params = self.get_updated_params(fetched_data, params)
        return results
    
    async def get_and_store_all_remote_data_async(self):
        list_of_params = self.get_list_of_params()
        return await self.fetch_and_store_all_async(list_of_params)
    
    def get_list_of_params(self):
        all_keys = self.get_all_keys()
        list_of_params = []
        base_params_dict = self.get_base_params_dict()
        for key in all_keys:
            list_of_params.append(
                base_params_dict | self.get_params_based_on_key(key))
        return list_of_params
    
    def get_all_keys(self) -> set:
        return set([None])
    
    def get_params_based_on_key(self, key) -> dict:
        return {}
    
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

    def get_updated_params(self, fetched_data, params:dict) -> dict:
        return params
    
    def get_base_params_dict(self) -> dict:
        return {}

class DataResolverWithMinIdBase(DataResolverBase):
    def __init__(self, main_collection: Collection, remote_url: str):
        assert 'minId={minId}' in remote_url, f"Missing minId query param in route {remote_url}!"
        super().__init__(main_collection, remote_url)
        self._min_id_field_name = "id"

    def perform_next_fetch(self, fetched_data):
        return True if fetched_data else False
    
    def get_updated_params(self, fetched_data, params:dict)-> dict:
        min_id = max(fetched_data, key=lambda item: item[self._min_id_field_name])[self._min_id_field_name]
        params['minId'] = min_id
        return params
    
    def get_base_params_dict(self) -> dict:
        return  {"minId": 0 }

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

    async def get_and_store_all_remote_data_async(self):
        list_of_params = self.get_list_of_params()
        return await self.fetch_and_store_all_async(list_of_params)
    
    def get_all_keys(self)->set:
        return self._related_collection.distinct(self._related_col_key_name)
    
    def perform_next_fetch(self, fetched_data):
        return False
    
    def transform_fetched_data(self, fetched_data, **params:dict):
        return [fetched_data]
    
    def get_params_based_on_key(self, key) -> dict:
        return { self._route_param_name: key }
    
class DataDetailResolverWithAggregationsBase(DataDetailResolverBase):
    def __init__(self, 
                 main_collection: Collection, 
                 remote_url: str, 
                 route_param_name: str,
                 related_collections: list[Collection]=None,
                 aggregations_by_collection_name: dict[str, list]=None):
        super().__init__(main_collection, remote_url, None, None, route_param_name)
        self._related_collections = related_collections
        self._aggregations_by_collection_name = aggregations_by_collection_name

    def get_all_keys(self):
        all_ids = set()
        for collection in self._related_collections:
            all_ids |= self.get_key_from_collection(collection)
        return all_ids
    
    def get_key_from_collection(self, collection:Collection) -> set[dict]:
        aggregation = self._aggregations_by_collection_name[collection.name]
        result = collection.aggregate(aggregation)
        return self.get_route_param_set_from_aggregation_result(result)

    def get_route_param_set_from_aggregation_result(self, result: CommandCursor)->set:
        return set([item[self._route_param_name] for item in result if item])