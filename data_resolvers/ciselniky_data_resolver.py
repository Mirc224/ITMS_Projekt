from data_resolvers.mongo_db_connection import MongoDBConnection
import requests
from bson.objectid import ObjectId
'''
Remote data example:
[
  {
    "ciselnikKod": 951945807983695100,
    "nazov": "Nihil architecto distinctio dicta.",
    "popis": "Et reiciendis officia."
  },
  {
    "ciselnikKod": 951945807983695100,
    "nazov": "Nihil architecto distinctio dicta.",
    "popis": "Et reiciendis officia."
  }
]
'''
class CiselnikyDataResolver:
    def __init__(self, connection:MongoDBConnection, db_name:str, collection_name):
        mongo_client = connection.client
        itms_db = mongo_client.get_database(db_name)
        self._ciselniky_collection = itms_db.get_collection(collection_name)
        self._remote_uri = 'https://opendata.itms2014.sk/v2/ciselniky'
        self._ciselnikKod_field = 'ciselnikKod'
        
    
    def fetch_remote_data(self):
        # remote_ciselniky_dict = self.get_all_remote_data()
        remote_data = self.get_all_remote_data()
        self._ciselniky_collection.delete_many({})
        self._ciselniky_collection.insert_many(remote_data)
        # local_ciselniky_dict = self.get_all_local_data()

        # remote_ciselnikKod_set = set(remote_ciselniky_dict.keys())
        # local_ciselnikKod_set = set(local_ciselniky_dict.keys())
        # ciselnikKod_items_to_add = remote_ciselnikKod_set - local_ciselnikKod_set
        # ciselnikKod_items_to_remove = local_ciselnikKod_set - remote_ciselnikKod_set

        # items_to_update = self.get_items_to_update(remote_ciselniky_dict, local_ciselniky_dict)

        # if ciselnikKod_items_to_remove:
        #     self._ciselniky_collection.delete_many({self._ciselnikKod_field : {"$in": list(ciselnikKod_items_to_remove)}})

        # if items_to_update:
        #     for data_for_replace in items_to_update:
        #          self._ciselniky_collection.replace_one({"_id": ObjectId(data_for_replace["_id"])}, data_for_replace["new_record"])

        # if ciselnikKod_items_to_add:
        #     items_to_add = [remote_ciselniky_dict[ciselnikKod].copy() for ciselnikKod in ciselnikKod_items_to_add]
        #     self._ciselniky_collection.insert_many(items_to_add)


    '''
    Returns:
    [
        {
            "_id": "1234",
            "new_record": {
                "ciselnikKod": 1001,
                "nazov": "Nihil architecto distinctio dicta.",
                "popis": "Et reiciendis officia."
            }
        }
    ]
    '''
    def get_items_to_update(
            self,
            remote_data_dict:dict, 
            local_data_dict:dict) -> dict:
        remote_ciselnikKod_set = set(remote_data_dict.keys())
        local_ciselnikKod_set = set(local_data_dict.keys())
        common_ciselnikKod_to_check = remote_ciselnikKod_set.intersection(local_ciselnikKod_set)

        items_to_update = []
        for ciselnikKod in common_ciselnikKod_to_check:
            remote_item = remote_data_dict[ciselnikKod]
            local_item =  local_data_dict[ciselnikKod]['origin']
            object_id = local_data_dict[ciselnikKod]['_id']
            if remote_item != local_item:
                items_to_update.append({"_id": object_id, "new_record": remote_item })

        return items_to_update

    '''
    Returns:
    {
        1001: {
        
            "_id": ObjectId(1234),
            "origin" {
                "ciselnikKod": 1001,
                "nazov": "Nihil architecto distinctio dicta.",
                "popis": "Et reiciendis officia."
            }
        },
        1002: {
        
            "_id": ObjectId(1235),
            "origin" {
                "ciselnikKod": 1002,
                "nazov": "Nihil architecto distinctio dicta.",
                "popis": "Et reiciendis officia."
            }
        }
    }
    '''
    def get_all_local_data(self) -> dict:
        local_ciselniky = self._ciselniky_collection.aggregate([
            {
                '$addFields': {
                    'origin': '$$CURRENT', 
                    'dict_key': '$ciselnikKod'
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

        return {val['dict_key']:val for val in local_ciselniky}


    '''
    Returns:
    {
        1001: {
            "ciselnikKod": 1001,
            "nazov": "Nihil architecto distinctio dicta.",
            "popis": "Et reiciendis officia."
        },
        1002: {
            "ciselnikKod": 1002,
            "nazov": "Nihil architecto distinctio dicta.",
            "popis": "Et reiciendis officia."
        }
    }
    '''
    def get_all_remote_data(self) -> dict:
        response = requests.get(self._remote_uri)
        # return {item[self._ciselnikKod_field]:item for item in response.json()}
        return response.json()
        