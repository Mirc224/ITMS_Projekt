import asyncio
import aiohttp
from time import perf_counter
from aiohttp import ClientSession
from data_resolvers.mongo_db_connection import MongoDBConnection
from data_resolvers.nezrovnalostDetail_data_resolver import NezrovnalostDetailDataResolver


# min_id = 0
# remote_url_template = 'https://opendata.itms2014.sk/v2/hodnotaCiselnika/{ciselnikKod}?minId={minId}'
# url = remote_url_template.format(ciselnikKod=ciselnik_kod, minId=min_id)
# print(cislenik_kod_list[:2])

# async def fetch(s, base_url:str, cislenik_kod):

# async def fetch_all(session, ciselnik_kod_list:list[int]):

# async def fetch_async(s:ClientSession, nezrovnalost_id:int):
#     remote_url_template = 'https://opendata.itms2014.sk/v2/nezrovnalost/{nezrovnalostId}'
#     async with s.get(remote_url_template.format(nezrovnalostId=nezrovnalost_id)) as r:
#         if r.status != 200:
#             r.raise_for_status()
#         return await r.text()

# async def fetch_all_async(nezrovnalost_id_list:list[int]):
#     tasks = []
#     async with aiohttp.ClientSession() as session:
#         for nezrovnalost_id in nezrovnalost_id_list:
#             task = asyncio.create_task(fetch_async(session, nezrovnalost_id))
#             tasks.append(task)
#         return await asyncio.gather(*tasks)
    # final_list = []
    # for res_list in res:
    #     if not res_list:
    #         continue
    #     final_list.extend(res_list)
    # return final_list


async def main():
    connection = MongoDBConnection('./appsettings.json')
    client = connection.client
    itms_db_name = 'itmsDB'
    nezrovnalost_col_name = 'nezrovnalosti'
    nezrovnalostDetail_col_name = 'nezrovnalostiDetail'
    nezrovnalostDetail_data_res = NezrovnalostDetailDataResolver(
        connection, 
        itms_db_name,
        nezrovnalost_col_name,
        nezrovnalostDetail_col_name)
    await nezrovnalostDetail_data_res.fetch_remote_data_async()


if __name__ == '__main__':
    start = perf_counter()
    asyncio.run(main())
    # main()
    stop = perf_counter()
    print("time taken:", stop - start)

# async def fetch(s:ClientSession, nezrovnalost_id):
#     async with s.get(f'https://opendata.itms2014.sk/v2/nezrovnalost/{nezrovnalost_id}') as r:
#         if r.status != 200:
#             r.raise_for_status()
#         return await r.json()


# async def fetch_all(all_ids:list[int]):
#     async with aiohttp.ClientSession() as s:
#         tasks = []
#         for id in all_ids:
#             task = asyncio.create_task(fetch(s, id))
#             tasks.append(task)
#         res = await asyncio.gather(*tasks)
#     return res


# def main():
#     connection = MongoDBConnection('./appsettings.json')
#     client = connection.client
#     nezrovnalost_col = client.get_database('itmsDB').get_collection('nezrovnalosti')
#     all_ids = nezrovnalost_col.distinct("id")
#     jsons = asyncio.run(fetch_all(all_ids[:5]))
#     print(jsons)


# if __name__ == '__main__':
#     start = perf_counter()
#     main()
#     stop = perf_counter()
#     print("time taken:", stop - start)
