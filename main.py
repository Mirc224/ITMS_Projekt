import asyncio
from data_resolvers.mongo_db_connection import MongoDBConnection
from data_resolvers.ciselniky_data_resolver import CiselnikyDataResolver, CiselnikyDetailDataResolver
from data_resolvers.nezrovnalost_data_resolver import NezrovnalostDataResolver, NezrovnalostDetailDataResolver
from data_resolvers.pohladavkovyDoklad_data_reslover import PohladavkovyDokladDataResolver, PohladavkovyDokladDetailDataResolver
from data_resolvers.aktivita_data_reslover import AktivitaDataResolver, AktivitaDetailDataResolver
from data_resolvers.projektyVRealizacii_data_resolver import ProjektyVRealizaciiDataResolver, ProjektyVRealizaciiDetailDataResolver
from data_resolvers.projektyUkoncene_data_resolver import ProjektyUkonceneDataResolver, ProjektyUkonceneDetailDataResolver
from data_resolvers.zop_predlozene_data_resolver import ZopPredlozeneDataResolver, ZopPredlozeneDetailDataResolver
from data_resolvers.zop_uhradene_data_resolver import ZopUhradeneDataResolver, ZopUhradeneDetailDataResolver
from time import perf_counter


async def main():
    connection = MongoDBConnection('./appsettings.json')
    client = connection.client
    itms_db_name = 'itmsDB'
    db = client.get_database(itms_db_name)
    collection_names = [
        'ciselniky_collection',
        'ciselnikyDetail_collection',
        'aktivita_collection',
        'aktivitaDetail_collection',
        'nezrovnalost_collection',
        'nezrovnalostDetail_collection',
        'pohladavkovyDoklad_collection',
        'pohladavkovyDokladDetail_collection',
        'projektyUkoncene_collection',
        'projektyUkonceneDetail_collection',
        'projektyVRealizacii_collection',
        'projektyVRealizaciiDetail_collection',
        'zopPredlozene_collection',
        'zopPredlozeneDetail_collection',
        'zopUhradene_collection',
        'zopUhradeneDetail_collection'
    ]

    db_collections = {col_name:db.get_collection(col_name) for col_name in collection_names}

    data_resolving_pipeline = [
        CiselnikyDataResolver(**db_collections),
        CiselnikyDetailDataResolver(**db_collections),
        NezrovnalostDataResolver(**db_collections),
        NezrovnalostDetailDataResolver(**db_collections),
        PohladavkovyDokladDataResolver(**db_collections),
        PohladavkovyDokladDetailDataResolver(**db_collections),
        AktivitaDataResolver(**db_collections),
        # # AktivitaDetailDataResolver(**db_collections),
        ProjektyVRealizaciiDataResolver(**db_collections),
        ProjektyVRealizaciiDetailDataResolver(**db_collections),
        ProjektyUkonceneDataResolver(**db_collections),
        ProjektyUkonceneDetailDataResolver(**db_collections),
        ZopPredlozeneDataResolver(**db_collections),
        ZopPredlozeneDetailDataResolver(**db_collections),
        ZopUhradeneDataResolver(**db_collections),
        # ZopUhradeneDetailDataResolver(**db_collections) # trvá 70 minút
    ]

    await data_resolving_pipeline[-1].resolve_data()

    # projektyUkoncene_data_resolver = ProjektyUkonceneDataResolver(
    #     projektyUkoncene_collection, 
    #     'https://opendata.itms2014.sk/v2/projekty/ukoncene?minId={minId}')
    # await projektyUkoncene_data_resolver.resolve_data()

    # projektyUkonceneDetail_data_resolver = ProjektyUkonceneDetailDataResolver(
    #     projektyUkonceneDetail_collection, 
    #     'https://opendata.itms2014.sk/v2/projekty/ukoncene/{projektId}',
    #     projektyUkoncene_collection,
    #     "id",
    #     'projektId')
    # await projektyUkonceneDetail_data_resolver.resolve_data()

if __name__ == '__main__':
    start = perf_counter()
    asyncio.run(main())
    stop = perf_counter()
    print("time taken:", stop - start)