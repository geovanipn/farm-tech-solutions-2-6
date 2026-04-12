import os
import oracledb
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    user = os.getenv("ORACLE_USER")
    password = os.getenv("ORACLE_PASSWORD")
    dsn = os.getenv("ORACLE_DSN")

    try:
        return oracledb.connect(user=user, password=password, dsn=dsn)
    except oracledb.DatabaseError as e:
        print(f"Erro ao conectar ao banco de dados Oracle: {e}")
        raise
