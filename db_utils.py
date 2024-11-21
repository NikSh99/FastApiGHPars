import psycopg2
from psycopg2.extensions import connection as PSQLConnection
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)
load_dotenv()


def get_db_connection() -> PSQLConnection:
    """Connecting with PSQL.

    out: Connection object.
    """
    try:
        '''
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            sslmode=os.getenv('DB_SSLMODE'),
            sslrootcert=os.getenv('DB_CERT_PATH'),
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            target_session_attrs=os.getenv('DB_TSA')
        )
        '''
        conn = psycopg2.connect("""
                host=rc1b-5p9g4g147bxm77o2.mdb.yandexcloud.net
                port=6432
                sslmode=verify-full
                dbname=ghpsql
                user=user
                password=1qaz2wsx
                target_session_attrs=read-write
            """)
        logger.info("Successful connection to the database.")
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"Exeption connect with PSQL: {e}")
        raise


def execute_query(query: str, params=None) -> list:
    """Executes an SQL query and returns the result."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if cur.description:
                result = cur.fetchall()
            else:
                result = []
            conn.commit()
            return result
    except Exception as e:
        logger.error(f"Request execution error: {e}")
        raise
    finally:
        conn.close()
