import keys
import pymysql
from sqlalchemy import create_engine


def get_connection():
    sqlEngine = create_engine(
    f'mysql+pymysql://{keys.mysql_username}:{keys.mysql_password}@{keys.mysql_host}:{keys.mysql_port}/{keys.mysql_db}?charset=utf8mb4',
        pool_recycle=3600)

    db_connection = sqlEngine.connect()
    print('connected to db...', db_connection)
    return db_connection


