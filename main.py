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
from data_resolvers.zop_zamietnute_data_resolver import ZopZamietnuteDataResolver, ZopZamietnuteDetailDataResolver
from data_resolvers.zonfp_prijate_data_resolver import ZonfpPrijateDataResolver, ZonfpPrijateDetailDataResolver
from data_resolvers.zonfp_schvalene_data_resolver import ZonfpSchvaleneDataResolver, ZonfpSchvaleneDetailDataResolver
from data_resolvers.zonfp_zamietnute_data_resolver import ZonfpZamietnuteDataResolver, ZonfpZamietnuteDetailDataResolver
from data_resolvers.vyzvy_planovane_data_resolver import VyzvyPlanovaneDataResolver, VyzvyPlanovaneDetailDataResolver
from data_resolvers.vyzvy_vyhlasene_data_resolver import VyzvyVyhlaseneDataResolver, VyzvyVyhlaseneDetailDataResolver
from data_resolvers.verejneObstaravania_data_resolver import VerejneObstaravaniaDataResolver, VerejneObstaravaniaDetailDataResolver
from data_resolvers.zmluvyVo_data_resolver import ZmluvyVODataResolver, ZmluvyVODetailDataResolver
from data_resolvers.projektovyUkazovatel_data_resolver import ProjektovyUkazovatelDataResolver, ProjektovyUkazovatelDetailDataResolver
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
        'zopUhradeneDetail_collection',
        'zopZamietnute_collection',
        'zopZamietnuteDetail_collection',
        'zonfpPrijate_collection',
        'zonfpPrijateDetail_collection',
        'zonfpSchvalene_collection',
        'zonfpSchvaleneDetail_collection',
        'zonfpZamietnute_collection',
        'zonfpZamietnuteDetail_collection',
        'vyzvyPlanovane_collection',
        'vyzvyPlanovaneDetail_collection',
        'vyzvyVyhlasene_collection',
        'vyzvyVyhlaseneDetail_collection',
        'verejneObstaravania_collection',
        'verejneObstaravaniaDetail_collection',
        'zmluvyVO_collection',
        'zmluvyVODetail_collection',
        'projektovyUkazovatel_collection',
        'projektovyUkazovatelDetail_collection',
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
        # # AktivitaDetailDataResolver(**db_collections), # pada to na chybach a trvá to dlho, neobsahuje iné informácie ako aktivitadata
        ProjektyVRealizaciiDataResolver(**db_collections),
        ProjektyVRealizaciiDetailDataResolver(**db_collections),
        ProjektyUkonceneDataResolver(**db_collections),
        ProjektyUkonceneDetailDataResolver(**db_collections),
        ZopPredlozeneDataResolver(**db_collections),
        ZopPredlozeneDetailDataResolver(**db_collections),
        ZopUhradeneDataResolver(**db_collections),
        # ZopUhradeneDetailDataResolver(**db_collections), # trvá 70 minút
        ZopZamietnuteDataResolver(**db_collections),
        ZopZamietnuteDetailDataResolver(**db_collections),
        ZonfpPrijateDataResolver(**db_collections),
        ZonfpPrijateDetailDataResolver(**db_collections),
        ZonfpSchvaleneDataResolver(**db_collections),
        ZonfpSchvaleneDetailDataResolver(**db_collections),
        ZonfpZamietnuteDataResolver(**db_collections),
        ZonfpZamietnuteDetailDataResolver(**db_collections),
        VyzvyPlanovaneDataResolver(**db_collections),
        VyzvyPlanovaneDetailDataResolver(**db_collections),
        VyzvyVyhlaseneDataResolver(**db_collections),
        VyzvyVyhlaseneDetailDataResolver(**db_collections),
        VerejneObstaravaniaDataResolver(**db_collections),
        VerejneObstaravaniaDetailDataResolver(**db_collections),
        ZmluvyVODataResolver(**db_collections),
        ZmluvyVODetailDataResolver(**db_collections),
        ProjektovyUkazovatelDataResolver(**db_collections),
        # ProjektovyUkazovatelDetailDataResolver(**db_collections), # zbyotčné, nepridáva nové fieldy
        
    ]

    await data_resolving_pipeline[-1].resolve_data()

if __name__ == '__main__':
    # start = perf_counter()
    asyncio.run(main())
    # stop = perf_counter()
    # print("time taken:", stop - start)