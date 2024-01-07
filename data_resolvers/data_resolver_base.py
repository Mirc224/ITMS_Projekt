import asyncio
import aiohttp
from aiohttp import ClientSession
from pymongo.collection import Collection
from data_resolvers.mongo_db_connection import MongoDBConnection
from abc import ABC, abstractmethod

class DataResolverBase:
    def __init__(self, main_collection: Collection, remote_url:str):
        self._main_collection = main_collection
        self._remote_url_template = remote_url
    
    async def resolve_data(self):
        remote_data = await self.get_all_remote_data_async()
        self._main_collection.delete_many({})
        data_to_insert = self.transform_data_to_insert(remote_data)
        self._main_collection.insert_many(data_to_insert)

    async def fetch_all_async(self, list_of_params:list[dict]):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for params in list_of_params:
                task = asyncio.create_task(self.fetch_async(session, params))
                tasks.append(task)
            return await asyncio.gather(*tasks)

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