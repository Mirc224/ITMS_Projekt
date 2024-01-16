# ITMS2014+
This project provides the ability to retrieve data from ITMS2014+ OpenAPI and store it in the MongoDB database.

## Usage
Pri použití je potrebné v **appsettings.json** súbore, v sekcii **collections_to_resolve** špecifikovať zoznam kolekcii, ktoré sa majú stiahnuť. Celý zoznam dostupných kolekcií je vylistovaný v **README.md -> Available Collections**. Ak zadáte viacero kolekcií, ktoré medzi sebou závisia, program sa postará o to, aby boli sťahované v správnom poradí.

## Resolver Settings
V súbore **appsettings.json** v sekcii **resolvers_settings** je možné pre každý data resolver definovať nasledujúce vlastnosti:
- "batchSize" - keďže niektoré kolekcie obsahujú veľa URL adries, na ktoré treba pristupovať, je vhodné z hľadiska rýchlosti a pamäťovej efektivity, rozdeliť tieto URL na menšie dávky, ktoré sa budú postupne sťahovať. (default 500)
- "parallelRequests" - na zabezpečenie rýchleho získavania dát je vhodné zasielať paralelne viacero requestov. Je však potrebné dbať na to, aby tento počet nepreťažoval server, inak sa budú objavovať chyba. Tento parameter určuje, koľko paralelných requestov sa bude v rámci jednej dávky spracovať. (default 50)
- "sleepTime" - pri príliš vysokom počte paralelných requestov môže dôjsť k zastaveniu prenosu zo strany serevera. Vtedy nastane chyba a na určitý čas, nie je možné zasielať ďalšie requesty. Vykonávanie sa v rámci paralelného "vlákna" uspí na stanovený počet sekúnd, určený hodnotou "sleepTime". Po uplynutí času sa opätovne pokúsi získať dáta. Hoci by mal byť tento spôsob spoľahlivý a zabezpečiť získanie dát, je z hľadiska rýchlosti a solidarity vhodnejšie znížiť počet requestov pre daný resolver tak, aby nepreťažoval server, čím sa vyhneme chybám a zbytočnému čakaniu. (default 300) 
- "numberOfRetries" - v prípade, že pri získavaní nastane chyba, program sa po uplynutí "sleepTime" pokúsi opätovne pristúpiť k dátam. Ak sa ani po *numberOfRetires* pokusoch nepodarí získať dáta, program ukončí získavanie danej adresy. (default 3)

Všetky tieto je možné (ale nie povinné) uviesť v appsettings súbore pre jednotlivé resolvery. Zoznam všetký resolverov je dostupný v sekcii **README.md -> Available Data Resolvers**.

## Database
Pripojenie k MongoDB je potrebné nadefinovať v súbore **appsettings.json** v sekcii **database**. Konfiguračná časť pre databázu by mala obsahovať všetky potrebné údaje pre pripojenie k lokálnej ako aj vzdialenej inštancii MongoDB databázy.

## Expanding Functionality
V prípade, že sa na ITMS OpenAPI pridá nový endpoint, bude potrebné vytvoriť data resolver, ktorý sa postará o získavanie dát z daného endpointu. Pri implementácii je v závislosti od typu endpointu, odporúčané použiť základné triedy, ktoré sa nachádzajú v súbore **./data_resolvers/data_resolver_base.py**. Nový data resolver by mal dediť od niektoré z tried **DataResolverWithMinIdBase**, **DataDetailResolverBase** alebo **DataDetailResolverWithAggregationsBase**, v závislosti od typu endpointu. V triede nového resolvera je potom potrebné určiť URL adresu, na ktorú sa má pristupovať a aj kolekcie s ktorými sa pracuje. Pre jednoduchosť je potrebné dodržiavať názvy vo formate *novaKolekcia_collection* a tento názov parametra používať aj naprieč ostatnými triedami, ktoré budú s touto kolekciou pracovať. Vďaka jednotnosti názvov kolekcií je potom program schopný určovať závislosti a vďaka tomu aj presné poradie získavania dát v rámci kolekcií.

Po implementácii nového data resolvera je potrebné tento data resolver pridať do **DataResolversRunner**, konkrétne do polí v metódach **__get_db_collections** a **__get_collection_data_resolver_list**. Pri pridávní nového data resolvera do týchto metód dodržte formát po vzore predchádzajúcich data resolverov.

Ak ste postupovali podľa návodu a odporúčaní, program by sa mal vedieť vysporiadať s novou kolekciou. Ak ste dodržali jednotnosť názvov parametrov, bude program schopný zistiť závislosti a vyriešiť poradie, v ktorom sa majú kolekcie napĺňať.

## Available Collections
"operacneProgramyDetail_collection",
"zmluvyVODetail_collection",
"financnePlany_collection",
"zonfpSchvaleneDetail_collection",
"verejneObstaravaniaDetail_collection",
"projektyVRealizaciiDetail_collection",
"nezrovnalostDetail_collection",
"aktivitaDetail_collection",
"zopZamietnute_collection",
"zopUhradene_collection",
"pohladavkovyDokladDetail_collection",
"vyzvyPlanovane_collection",
"prioritneOsiOP_collection",
"zopPredlozene_collection",
"zonfpZamietnute_collection",
"intenzitaDetail_collection",
"nezrovnalost_collection",
"zopUhradeneDetail_collection",
"typyAktivit_collection",
"polozkaRozpoctuDetail_collection",
"projektyUkoncene_collection",
"zonfpPrijateDetail_collection",
"typyAktivitDetail_collection",
"projektovyUkazovatelDetail_collection",
"vyzvyVyhlaseneDetail_collection",
"projektovyUkazovatel_collection",
"konkretneCieleDetail_collection",
"uctovneDoklady_collection",
"subjekty_collection",
"aktivita_collection",
"projektyVRealizacii_collection",
"konkretneCielePOs_collection",
"zonfpZamietnuteDetail_collection",
"vyzvyPlanovaneDetail_collection",
"prioritneOsiDetail_collection",
"pohladavkovyDoklad_collection",
"ciselnikyDetail_collection",
"operacneProgramy_collection",
"vyzvyVyhlasene_collection",
"zopPredlozeneDetail_collection",
"zonfpPrijate_collection",
"ciselniky_collection",
"zmluvyVO_collection",
"zopZamietnuteDetail_collection",
"dodavatelia_collection",
"projektyUkonceneDetail_collection",
"verejneObstaravania_collection",
"zonfpSchvalene_collection",
"uctovneDokladyDetail_collection"

## Available Data Resolvers
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
IntenzitaDetailDataResolver