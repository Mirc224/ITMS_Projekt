import asyncio
from data_resolvers.mongo_db_connection import MongoDBConnection
from data_resolvers.ciselniky_data_resolver import CiselnikyDataResolver, CiselnikyDetailDataResolver
from data_resolvers.nezrovnalost_data_resolver import NezrovnalostDataResolver, NezrovnalostDetailDataResolver
from data_resolvers.pohladavkovyDoklad_data_reslover import PohladavkovyDokladDataResolver, PohladavkovyDokladDetailDataResolver
from data_resolvers.aktivita_data_reslover import AktivitaDataResolver, AktivitaDetailDataResolver
from data_resolvers.projektyVRealizacii_data_resolver import ProjektyVRealizaciiDataResolver, ProjektyVRealizaciiDetailDataResolver
from data_resolvers.projektyUkoncene_data_resolver import ProjektyUkonceneDataResolver, ProjektyUkonceneDetailDataResolver
from data_resolvers.zopPredlozene_data_resolver import ZopPredlozeneDataResolver, ZopPredlozeneDetailDataResolver
from data_resolvers.zopUhradene_data_resolver import ZopUhradeneDataResolver, ZopUhradeneDetailDataResolver
from data_resolvers.zopZamietnute_data_resolver import ZopZamietnuteDataResolver, ZopZamietnuteDetailDataResolver
from data_resolvers.zonfpPrijate_data_resolver import ZonfpPrijateDataResolver, ZonfpPrijateDetailDataResolver
from data_resolvers.zonfpSchvalene_data_resolver import ZonfpSchvaleneDataResolver, ZonfpSchvaleneDetailDataResolver
from data_resolvers.zonfpZamietnute_data_resolver import ZonfpZamietnuteDataResolver, ZonfpZamietnuteDetailDataResolver
from data_resolvers.vyzvyPlanovane_data_resolver import VyzvyPlanovaneDataResolver, VyzvyPlanovaneDetailDataResolver
from data_resolvers.vyzvyVyhlasene_data_resolver import VyzvyVyhlaseneDataResolver, VyzvyVyhlaseneDetailDataResolver
from data_resolvers.verejneObstaravania_data_resolver import VerejneObstaravaniaDataResolver, VerejneObstaravaniaDetailDataResolver
from data_resolvers.zmluvyVo_data_resolver import ZmluvyVODataResolver, ZmluvyVODetailDataResolver
from data_resolvers.projektovyUkazovatel_data_resolver import ProjektovyUkazovatelDataResolver, ProjektovyUkazovatelDetailDataResolver
from data_resolvers.polozkaRozpoctu_data_resolver import PolozkaRozpoctuDetailDataResolver
from data_resolvers.intenzitaDetail_data_resolver import IntenzitaDetailDataResolver
from data_resolvers.uctovneDoklady_data_resolver import UctovneDokladyDataResolver, UctovneDokladyDetailDataResolver
from data_resolvers.operacneProgramy_data_resolver import OperacneProgramyDataResolver, OperacneProgramyDetailDataResolver
from data_resolvers.typyAktivit_data_resolver import TypyAktivitDataResolver, TypyAktivitDetailDataResolver
from data_resolvers.prioritneOsi_data_resolver import PrioritneOsiDataResolver, PrioritneOsiDetailDataResolver
from data_resolvers.konkretneCiele_data_resolver import KonkretneCieleDataResolver, KonkretneCieleDetailDataResolver
import logging


async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
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
        'polozkaRozpoctuDetail_collection',
        'intenzitaDetail_collection',
        'uctovneDoklady_collection',
        'uctovneDokladyDetail_collection',
        'operacneProgramy_collection',
        'operacneProgramyDetail_collection',
        'typyAktivit_collection',
        'typyAktivitDetail_collection',
        'prioritneOsi_collection',
        'prioritneOsiDetail_collection',
        'konkretneCiele_collection',
        'konkretneCieleDetail_collection',
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
        ZopUhradeneDetailDataResolver(**db_collections), # trvá 70 minút
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
        PolozkaRozpoctuDetailDataResolver(**db_collections),
        IntenzitaDetailDataResolver(**db_collections),
        UctovneDokladyDataResolver(**db_collections),
        UctovneDokladyDetailDataResolver(**db_collections),
        OperacneProgramyDataResolver(**db_collections),
        OperacneProgramyDetailDataResolver(**db_collections),
        TypyAktivitDataResolver(**db_collections),
        TypyAktivitDetailDataResolver(**db_collections),
        PrioritneOsiDataResolver(**db_collections),
        PrioritneOsiDetailDataResolver(**db_collections),
        KonkretneCieleDataResolver(**db_collections),
        KonkretneCieleDetailDataResolver(**db_collections)
    ]

    await data_resolving_pipeline[-1].resolve_data()
    # for data_resolver in data_resolving_pipeline[-3:]:
    #     await data_resolver.resolve_data()

if __name__ == '__main__':
    # start = perf_counter()
    asyncio.run(main())
    # stop = perf_counter()
    # print("time taken:", stop - start)