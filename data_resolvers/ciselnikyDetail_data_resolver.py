from data_resolvers.mongo_db_connection import MongoDBConnection
from bson.objectid import ObjectId
import asyncio
import aiohttp
from aiohttp import ClientSession

class CiselnikyDetailDataResolver:
    def __init__(
            self, 
            connection:MongoDBConnection, 
            db_name:str, 
            ciselniky_col_name:str, 
            ciselnikyDetail_col_name:str):
        mongo_client = connection.client
        itms_db = mongo_client.get_database(db_name)
        self._ciselniky_collection = itms_db.get_collection(ciselniky_col_name)
        self._ciselnikyDetail_collection = itms_db.get_collection(ciselnikyDetail_col_name)
        self._remote_uri_template = 'https://opendata.itms2014.sk/v2/hodnotaCiselnika/{ciselnikKod}?minId={minId}'
        
    
    async def fetch_remote_data_async(self):
        remote_data = await self.get_all_remote_data_async()
        self._ciselnikyDetail_collection.delete_many({})
        self._ciselnikyDetail_collection.insert_many(remote_data)
        # remote_data_dict = await self.get_all_remote_data_async()
        # local_data_dict = self.get_all_local_data()

        # remote_dict_key_set = set(remote_data_dict.keys())
        # local_dict_key_set = set(local_data_dict.keys())

        # remote_dict_key_to_add = remote_dict_key_set - local_dict_key_set
        # local_dict_key_to_remove = local_dict_key_set - remote_dict_key_set

        # items_to_update = self.get_items_to_update(remote_data_dict, local_data_dict)
        # if local_dict_key_to_remove:
        #     ids_to_delete = [local_data_dict[dict_key]['_id'] for dict_key in local_dict_key_to_remove]
        #     self._ciselnikyDetail_collection.delete_many({"_id": {"$in" : ids_to_delete}})

        # if items_to_update:
        #     for item_for_update in items_to_update:
        #         self._ciselnikyDetail_collection.replace_one({"_id": item_for_update["_id"]}, item_for_update["new_record"])

        # if remote_dict_key_to_add:
        #     items_to_add = [remote_data_dict[dict_key].copy() for dict_key in remote_dict_key_to_add]
        #     self._ciselnikyDetail_collection.insert_many(items_to_add)

    def get_all_local_data(self):
        local_ciselnikDetail = self._ciselnikyDetail_collection.aggregate([
            {
                '$addFields': {
                    'origin': '$$CURRENT', 
                    'dict_key': {
                        '$concat': [
                            {
                                '$toString': '$ciselnikKod'
                            }, '_', {
                                '$toString': '$id'
                            }
                        ]
                    }
                }
            }, {
                '$project': {
                    'origin._id': 0
                }
            }, {
                '$project': {
                    '_id': 1, 
                    'origin': 1, 
                    'dict_key': 1
                }
            }
        ])
        return {item['dict_key']:item for item in local_ciselnikDetail}
    
    async def fetch_async(self, s:ClientSession, ciselnik_kod):
        min_id = 0
        all_ciselnikDetail_data = []
        remote_url_template = 'https://opendata.itms2014.sk/v2/hodnotaCiselnika/{ciselnikKod}?minId={minId}'
        while True:
            async with s.get(remote_url_template.format(ciselnikKod=ciselnik_kod, minId=min_id)) as r:
                if r.status != 200:
                    r.raise_for_status()
                current_data_batch = await r.json()
                if len(current_data_batch) == 0:
                    break
                all_ciselnikDetail_data.extend(current_data_batch)
                min_id = max(current_data_batch, key=lambda item: item["id"])['id']
            return [{"ciselnikKod":ciselnik_kod} | item for item in all_ciselnikDetail_data]

    async def fetch_all_async(self, ciselnik_kod_list:list[int]):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for ciselnik_kod in ciselnik_kod_list:
                task = asyncio.create_task(self.fetch_async(session, ciselnik_kod))
                tasks.append(task)
            res = await asyncio.gather(*tasks)
        final_list = []
        for res_list in res:
            if not res_list:
                continue
            final_list.extend(res_list)
        return final_list

    async def get_all_remote_data_async(self):
        ciselnikKod_field = 'ciselnikKod'
        ciselnik_kod_list = self._ciselniky_collection.distinct(ciselnikKod_field)
        # result = await self.fetch_all_async(ciselnik_kod_list)
        # return {f'{item['ciselnikKod']}_{item['id']}':item for item in result}
        return await self.fetch_all_async(ciselnik_kod_list)
    
    def get_items_to_update(self, remote_data:dict, local_data:dict):
        remote_dict_key_set = set(remote_data.keys())
        local_dict_key_set = set(local_data.keys())
        common_dict_key_to_check = remote_dict_key_set.intersection(local_dict_key_set)

        items_to_update = []
        for dict_key in common_dict_key_to_check:
                remote_item = remote_data[dict_key]
                local_item =  local_data[dict_key]['origin']
                object_id = local_data[dict_key]['_id']
                if remote_item != local_item:
                    items_to_update.append({"_id": object_id, "new_record": remote_item.copy() })
        return items_to_update
                