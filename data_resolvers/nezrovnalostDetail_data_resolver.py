from data_resolvers.mongo_db_connection import MongoDBConnection
from bson.objectid import ObjectId
import asyncio
import aiohttp
from aiohttp import ClientSession

class NezrovnalostDetailDataResolver:
    def __init__(
            self, 
            connection:MongoDBConnection, 
            db_name:str, 
            nezrovnalosti_col_name:str, 
            nezrovnalostDetail_col_name:str):
        mongo_client = connection.client
        itms_db = mongo_client.get_database(db_name)
        self._nezrovnalost_collection = itms_db.get_collection(nezrovnalosti_col_name)
        self._nezrovnalostDetail_collection = itms_db.get_collection(nezrovnalostDetail_col_name)
        self._uri_template = 'https://opendata.itms2014.sk/v2/nezrovnalost/{nezrovnalostId}'
        

    async def fetch_remote_data_async(self):
        remote_data = await self.get_all_remote_data_async()
        self._nezrovnalostDetail_collection.delete_many({})
        self._nezrovnalostDetail_collection.insert_many(remote_data)

    async def fetch_async(self, s:ClientSession, nezrovnalost_id:int):
        async with s.get(self._uri_template.format(nezrovnalostId=nezrovnalost_id)) as r:
            if r.status != 200:
                r.raise_for_status()
            return await r.json()

    async def fetch_all_async(self, nezrovnalost_id_list:list[int]):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for nezrovnalost_id in nezrovnalost_id_list:
                task = asyncio.create_task(self.fetch_async(session, nezrovnalost_id))
                tasks.append(task)
            return await asyncio.gather(*tasks)
        
    async def get_all_remote_data_async(self):
        all_ids = self._nezrovnalost_collection.distinct("id")
        return await self.fetch_all_async(all_ids)
    