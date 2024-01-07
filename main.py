import asyncio
from data_resolvers.mongo_db_connection import MongoDBConnection
from data_resolvers.ciselniky_data_resolver import CiselnikyDataResolver, CiselnikyDetailDataResolver
from data_resolvers.nezrovnalost_data_resolver import NezrovnalostDataResolver, NezrovnalostDetailDataResolver
from time import perf_counter

connection = MongoDBConnection('./appsettings.json')
client = connection.client
itms_db_name = 'itmsDB'
db = client.get_database(itms_db_name)
ciselniky_col_name = 'ciselniky' 
ciselnikyDetail_col_name = 'ciselnikyDetail' 
nezrovnalost_col_name = 'nezrovnalost'
nezrovnalostDetail_col_name = 'nezrovnalostDetail'

ciselniky_collection = db.get_collection(ciselniky_col_name)
ciselnikyDetail_collection = db.get_collection(ciselnikyDetail_col_name)
nezrovnalost_collection = db.get_collection(nezrovnalost_col_name)
nezrovnalostDetail_collection = db.get_collection(nezrovnalostDetail_col_name)


start = perf_counter()
# ciselniky_data_resolver = CiselnikyDataResolver(ciselniky_collection, 'https://opendata.itms2014.sk/v2/ciselniky')
# asyncio.run(ciselniky_data_resolver.resolve_data())

# ciselnikyDetail_data_resolver = CiselnikyDetailDataResolver(
#     ciselnikyDetail_collection, 
#     'https://opendata.itms2014.sk/v2/hodnotaCiselnika/{ciselnikKod}?minId={minId}',
#     ciselniky_collection)
# asyncio.run(ciselnikyDetail_data_resolver.resolve_data())

# nezrovnalost_data_resolver = NezrovnalostDataResolver(
#     nezrovnalost_collection, 
#     'https://opendata.itms2014.sk/v2/nezrovnalost?minId={minId}')
# asyncio.run(nezrovnalost_data_resolver.resolve_data())

# nezrovnalostDetail_data_resolver = NezrovnalostDetailDataResolver(
#     nezrovnalostDetail_collection, 
#     'https://opendata.itms2014.sk/v2/nezrovnalost/{nezrovnalostId}',
#     nezrovnalost_collection)
# asyncio.run(nezrovnalostDetail_data_resolver.resolve_data())

stop = perf_counter()
print("time taken:", stop - start)