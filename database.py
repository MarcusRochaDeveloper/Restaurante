import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

class Database:
    def __init__(self):
        self.engine = None
        self.Session = None
    
    def garantir_banco_existente(self, host, port, user, password, dbname):
        conn = pymysql.connect(host=host, port=int(port), user=user, password=password)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}`")
        conn.commit()
        conn.close()
    
    def conectar(self, host, port, user, password, dbname):
        try:
            self.garantir_banco_existente(host, port, user, password, dbname)

            url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
            self.engine = create_engine(url, echo=False, pool_pre_ping=True)

            Base.metadata.create_all(self.engine)

            self.Session = sessionmaker(bind=self.engine)

            return True

        except Exception as e:
            raise Exception("Erro ao conectar ao banco: " + str(e))
    
    def get_session(self):
        if not self.Session:
            return None
        return self.Session()

db = Database()
