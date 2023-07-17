import psycopg2
from typing import Dict
from utils import read_json


class SqlConnector:
    def __init__(self, config: str) -> None:
        self.conf: Dict[str, str] = read_json(config)
        self.db = psycopg2.connect(
                database=self.conf['database'],
                user=self.conf['user'],
                password=self.conf['password'],
                host=self.conf['host'],
                port=self.conf['port']
            )
        self.cursor = self.db.cursor()

    def execute(self, query) -> object:
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result



if __name__ == '__main__':    
    db = SqlConnector('./conf.json')
    query = 'SELECT * FROM actor limit 5'
    result = db.execute(query)
    print(result)
