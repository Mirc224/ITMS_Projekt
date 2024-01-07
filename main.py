import asyncio
from data_resolvers.mongo_db_connection import MongoDBConnection
from data_resolvers.ciselniky_data_resolver import CiselnikyDataResolver, CiselnikyDetailDataResolver
from data_resolvers.nezrovnalost_data_resolver import NezrovnalostDataResolver, NezrovnalostDetailDataResolver
from data_resolvers.pohladavkovyDoklad_data_reslover import PohladavkovyDokladDataResolver, PohladavkovyDokladDetailDataResolver
from data_resolvers.aktivita_data_reslover import AktivitaDataResolver, AktivitaDetailDataResolver
from time import perf_counter


async def main():
    connection = MongoDBConnection('./appsettings.json')
    client = connection.client
    itms_db_name = 'itmsDB'
    db = client.get_database(itms_db_name)
    ciselniky_col_name = 'ciselniky' 
    ciselnikyDetail_col_name = 'ciselnikyDetail' 
    nezrovnalost_col_name = 'nezrovnalost'
    nezrovnalostDetail_col_name = 'nezrovnalostDetail'
    pohladavkovyDoklad_col_name = 'pohladavkovyDoklad'
    pohladavkovyDokladDetail_col_name = 'pohladavkovyDokladDetail'
    aktivita_col_name = 'aktivita'
    aktivitaDetail_col_name = 'aktivitaDetail'

    ciselniky_collection = db.get_collection(ciselniky_col_name)
    ciselnikyDetail_collection = db.get_collection(ciselnikyDetail_col_name)
    nezrovnalost_collection = db.get_collection(nezrovnalost_col_name)
    nezrovnalostDetail_collection = db.get_collection(nezrovnalostDetail_col_name)
    pohladavkovyDoklad_collection = db.get_collection(pohladavkovyDoklad_col_name)
    pohladavkovyDokladDetail_collection = db.get_collection(pohladavkovyDokladDetail_col_name)
    aktivita_collection = db.get_collection(aktivita_col_name)
    aktivitaDetail_collection = db.get_collection(aktivitaDetail_col_name)

    # ciselniky_data_resolver = CiselnikyDataResolver(
    # ciselniky_collection, 'https://opendata.itms2014.sk/v2/ciselniky')
    # await ciselniky_data_resolver.resolve_data()

    ciselnikyDetail_data_resolver = CiselnikyDetailDataResolver(
        ciselnikyDetail_collection, 
        'https://opendata.itms2014.sk/v2/hodnotaCiselnika/{ciselnikKod}?minId={minId}',
        ciselniky_collection)
    await ciselnikyDetail_data_resolver.resolve_data()

    # nezrovnalost_data_resolver = NezrovnalostDataResolver(
    #     nezrovnalost_collection, 
    #     'https://opendata.itms2014.sk/v2/nezrovnalost?minId={minId}')
    # await nezrovnalost_data_resolver.resolve_data()

    # nezrovnalostDetail_data_resolver = NezrovnalostDetailDataResolver(
    #     nezrovnalostDetail_collection, 
    #     'https://opendata.itms2014.sk/v2/nezrovnalost/{nezrovnalostId}',
    #     nezrovnalost_collection,
    #     "id",
    #     'nezrovnalostId')
    # await nezrovnalostDetail_data_resolver.resolve_data()

    # pohladavkovyDoklad_data_resolver = PohladavkovyDokladDataResolver(
    #     pohladavkovyDoklad_collection, 
    #     'https://opendata.itms2014.sk/v2/pohladavkovyDoklad?minId={minId}')
    # await pohladavkovyDoklad_data_resolver.resolve_data()

    # pohladavkovyDokladDetail_data_resolver = PohladavkovyDokladDetailDataResolver(
    #     pohladavkovyDokladDetail_collection, 
    #     'https://opendata.itms2014.sk/v2/pohladavkovyDoklad/{dokladId}',
    #     pohladavkovyDoklad_collection,
    #     "id",
    #     'dokladId')
    # await pohladavkovyDokladDetail_data_resolver.resolve_data()

    # aktivita_data_resolver = AktivitaDataResolver(
    #     aktivita_collection, 
    #     'https://opendata.itms2014.sk/v2/aktivita?minId={minId}')
    # await aktivita_data_resolver.resolve_data()

    # aktivitaDetail_data_resolver = AktivitaDetailDataResolver(
    #     aktivitaDetail_collection,
    #     'https://opendata.itms2014.sk/v2/aktivita/{aktivitaId}',
    #     aktivita_collection,
    #     "id",
    #     'aktivitaId')
    # await aktivitaDetail_data_resolver.resolve_data()


if __name__ == '__main__':
    start = perf_counter()
    asyncio.run(main())
    stop = perf_counter()
    print("time taken:", stop - start)