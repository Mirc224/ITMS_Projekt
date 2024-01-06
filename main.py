# from data_resolvers.mongo_db_connection import MongoDBConnection
# import time
# connection = MongoDBConnection('./appsettings.json')

# client = connection.client

# print(client.list_database_names())

# db = client.get_database("itmsDB")

# collection = db.get_collection("users")

# collection.insert_one({"name":"Jakub", "age":20, "email":"jakub123@email.com", "address":"Hlavna 1, Bratislava", "orders":[], "subscription": True})

url = 'asd{minId}'

print(url.format(**{"minId":1}))