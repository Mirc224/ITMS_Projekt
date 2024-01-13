import asyncio
from data_resolvers.data_resolver_base import DataResolverBase
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
from data_resolvers.prioritneOsi_data_resolver import PrioritneOsiOPDataResolver, PrioritneOsiDetailDataResolver
from data_resolvers.konkretneCiele_data_resolver import KonkretneCielePOsDataResolver, KonkretneCieleDetailDataResolver
from data_resolvers.financnePlany_data_reslover import FinancnePlanyDataResolver
from data_resolvers.dodavatelia_data_resolver import DodavateliaDataResolver
from data_resolvers.subjekt_data_resolver import SubjektyDataResolver
import logging
import graphlib
import inspect
import json
from pymongo.collection import Collection


class DataResolversRunner:
    def __init__(self, appsettings_path:str) -> None:
        self._config = self.__read_config_file(appsettings_path)
        
        connection = MongoDBConnection(self._config['database'])
        self._db = connection.client.get_database("itmsDB")
        
        self._collection_data_resolver_dict = self.__get_collection_data_resolver_dict()

    def __get_collection_data_resolver_list(self) -> list[DataResolverBase]:
        db_collections = self.__get_db_collections()
        return [
            CiselnikyDataResolver(**db_collections),
            CiselnikyDetailDataResolver(**db_collections),
            NezrovnalostDataResolver(**db_collections),
            NezrovnalostDetailDataResolver(**db_collections),
            PohladavkovyDokladDataResolver(**db_collections),
            PohladavkovyDokladDetailDataResolver(**db_collections),
            ZopPredlozeneDataResolver(**db_collections),
            ZopPredlozeneDetailDataResolver(**db_collections),
            ZopUhradeneDataResolver(**db_collections),
            ZopUhradeneDetailDataResolver(**db_collections),
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
            UctovneDokladyDataResolver(**db_collections),
            UctovneDokladyDetailDataResolver(**db_collections),
            DodavateliaDataResolver(**db_collections),
            SubjektyDataResolver(**db_collections),
            FinancnePlanyDataResolver(**db_collections),
            KonkretneCieleDetailDataResolver(**db_collections),
            OperacneProgramyDataResolver(**db_collections),
            OperacneProgramyDetailDataResolver(**db_collections),
            PrioritneOsiOPDataResolver(**db_collections),
            PrioritneOsiDetailDataResolver(**db_collections),
            KonkretneCielePOsDataResolver(**db_collections),
            TypyAktivitDataResolver(**db_collections),
            TypyAktivitDetailDataResolver(**db_collections),
            ProjektovyUkazovatelDataResolver(**db_collections),
            ProjektovyUkazovatelDetailDataResolver(**db_collections),
            AktivitaDataResolver(**db_collections),
            AktivitaDetailDataResolver(**db_collections),
            ProjektyVRealizaciiDataResolver(**db_collections),
            ProjektyVRealizaciiDetailDataResolver(**db_collections),
            ProjektyUkonceneDataResolver(**db_collections),
            ProjektyUkonceneDetailDataResolver(**db_collections),
            PolozkaRozpoctuDetailDataResolver(**db_collections),
            PolozkaRozpoctuDetailDataResolver(**db_collections),
            IntenzitaDetailDataResolver(**db_collections),
        ]   

    def __get_collection_data_resolver_dict(self) -> dict[str, DataResolverBase]:
        all_resolvers = self.__get_collection_data_resolver_list()
        collection_resolver_dict = {}
        for resolver in all_resolvers:
            resolver_parameters = list(inspect.signature(resolver.__init__).parameters.keys())
            resolver_main_collection_name = resolver_parameters[0]
            collection_resolver_dict[resolver_main_collection_name] = resolver
        
        return collection_resolver_dict

    def __get_db_collections(self) -> dict[Collection]:
        all_resolvers = [
            CiselnikyDataResolver,
            CiselnikyDetailDataResolver,
            NezrovnalostDataResolver,
            NezrovnalostDetailDataResolver,
            PohladavkovyDokladDataResolver,
            PohladavkovyDokladDetailDataResolver,
            ZopPredlozeneDataResolver,
            ZopPredlozeneDetailDataResolver,
            ZopUhradeneDataResolver,
            ZopUhradeneDetailDataResolver,
            ZopZamietnuteDataResolver,
            ZopZamietnuteDetailDataResolver,
            ZonfpPrijateDataResolver,
            ZonfpPrijateDetailDataResolver,
            ZonfpSchvaleneDataResolver,
            ZonfpSchvaleneDetailDataResolver,
            ZonfpZamietnuteDataResolver,
            ZonfpZamietnuteDetailDataResolver,
            VyzvyPlanovaneDataResolver,
            VyzvyPlanovaneDetailDataResolver,
            VyzvyVyhlaseneDataResolver,
            VyzvyVyhlaseneDetailDataResolver,
            VerejneObstaravaniaDataResolver,
            VerejneObstaravaniaDetailDataResolver,
            ZmluvyVODataResolver,
            ZmluvyVODetailDataResolver,
            UctovneDokladyDataResolver,
            UctovneDokladyDetailDataResolver,
            DodavateliaDataResolver,
            SubjektyDataResolver,
            FinancnePlanyDataResolver,
            KonkretneCieleDetailDataResolver,
            OperacneProgramyDataResolver,
            OperacneProgramyDetailDataResolver,
            PrioritneOsiOPDataResolver,
            PrioritneOsiDetailDataResolver,
            KonkretneCielePOsDataResolver,
            TypyAktivitDataResolver,
            TypyAktivitDetailDataResolver,
            ProjektovyUkazovatelDataResolver,
            ProjektovyUkazovatelDetailDataResolver,
            AktivitaDataResolver,
            AktivitaDetailDataResolver,
            ProjektyVRealizaciiDataResolver,
            ProjektyVRealizaciiDetailDataResolver,
            ProjektyUkonceneDataResolver,
            ProjektyUkonceneDetailDataResolver,
            PolozkaRozpoctuDetailDataResolver,
            PolozkaRozpoctuDetailDataResolver,
            IntenzitaDetailDataResolver,
            ]
        list_of_collections_names = []
        for resolver in all_resolvers:
            resolver_parameters = list(inspect.signature(resolver.__init__).parameters.keys())
            list_of_collections_names.extend(resolver_parameters[1:-1])
        
        set_of_collection_names = set(list_of_collections_names)
        return {col_name:self._db.get_collection(col_name) for col_name in set_of_collection_names}

    def __read_config_file(self, config_path:str) -> dict:
        config = {}
        with open(config_path, "r", encoding="utf8") as f:
            config = json.load(f)
        return config
    
    def __get_ordered_resolvers_to_run(self) -> list[DataResolverBase]:
        collections_to_resolve_set = set(self._config['collections_to_resolve'])
        precedence_graph = {}
        for collection_resolver_name in collections_to_resolve_set:
            resolver = self._collection_data_resolver_dict[collection_resolver_name]

            resolver_parameters = list(inspect.signature(resolver.__init__).parameters.keys())
            resolver_main_collection_name = resolver_parameters[0]
            resolver_prerquisit_collections = set(resolver_parameters[1:-1])

            precedence_graph[resolver_main_collection_name] = resolver_prerquisit_collections.intersection(collections_to_resolve_set)
        
        topological_sorter = graphlib.TopologicalSorter(precedence_graph)
        ordered_collections_to_get = list(topological_sorter.static_order())
        return [self._collection_data_resolver_dict[collection_resolver_name] for collection_resolver_name in ordered_collections_to_get]

    async def resolve_data_async(self):
        resolvers_to_run = self.__get_ordered_resolvers_to_run()
        for resolver in resolvers_to_run:
            await resolver.resolve_data()