import json
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
REQUIRED_FIELDS = [
        "DB_USER",
        "DB_PASSWORD",
        "HOST",
        "PORT",
        "AUTH_SOURCE",
        "DATABASE",
        "SERVER_SELECTION_TIMEOUT_MS"]

class MongoDBConnection:
    def __init__(self, config_path:str="./appsettings.json"):
        self._config = self.__read_config_file(config_path)
        self.__check_config_values(self._config, REQUIRED_FIELDS)
        self._client = self.__make_connection()
    
    def __check_config_values(self, config:dict, required_fields:list[str]):
        for field in required_fields:
            assert field in config.keys() and config[field] is not None, f"Chýba konfiguračná hodnota {field}"

    def __read_config_file(self, config_path:str) -> dict:
        config = {}
        with open(config_path, "r", encoding="utf8") as f:
            config = json.load(f)
        return config['database']
    
    def __make_connection(self) -> MongoClient:
        db_user = self._config["DB_USER"]
        db_password = self._config["DB_PASSWORD"]
        host = self._config["HOST"]
        port = self._config["PORT"]
        auth_source = self._config["AUTH_SOURCE"]
        database = self._config["DATABASE"]
        server_connection_timeout = self._config["SERVER_SELECTION_TIMEOUT_MS"]
        user_credentials = ""

        if db_user and  db_password:
            user_credentials = f"{db_user}:{db_password}@"


        # db_uri=f"mongodb://{db_user}:{db_password}@{host}:{port}/{database}?authSource={auth_source}&serverSelectionTimeoutMS={server_connection_timeout}"
        db_uri=f"mongodb://{user_credentials}{host}:{port}/{database}?authSource={auth_source}&serverSelectionTimeoutMS={server_connection_timeout}"
        client = MongoClient(db_uri)
        print("Pripájanie k databáze...")
        msg = None
        try:
            client.list_database_names()
        except ServerSelectionTimeoutError as e:
            print("Nepodarilo sa pripojiť k databáze, skontrolujte HOST a PORT!")
            msg=e
        except OperationFailure as e:
            print("Nepodarilo sa autentifikovať voči databáze, skontrolujte USERNAME a PASSWORD!")
            msg=e
        except Exception as e:
            print("Nepodarilo sa pripojiť k databáze!")
            msg=e
        finally:
            if msg is not None:
                print(msg)
                print("Ukončujem vykonávanie!")
                exit()
            print("Pripojenie k databáze prebehlo úspešne!")
        return client
    
    @property
    def client(self) -> MongoClient:
        return self._client
