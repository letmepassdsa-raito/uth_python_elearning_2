import os
import psycopg2
from configparser import ConfigParser

class DatabaseConnection:
    @staticmethod
    def get_connection():
        config = ConfigParser()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, 'config.ini')
        
        if not os.path.exists(config_path):
            print(f"[SYSTEM ERROR]: Configuration file not found at {config_path}")
            return None
        
        config.read(config_path)
        try:
            return psycopg2.connect(
                host=config.get('postgresql', 'host'),
                database=config.get('postgresql', 'database'),
                user=config.get('postgresql', 'user'),
                password=config.get('postgresql', 'password'),
                port=config.get('postgresql', 'port')
            )
        except Exception as error:
            print(f"\n[DATABASE CONNECTION ERROR]: {error}")
            return None
