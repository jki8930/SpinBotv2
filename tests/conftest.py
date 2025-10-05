import pytest
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def terminate_database_connections(db_name):
    conn = psycopg2.connect(user="postgres", password="postgres", host="localhost", port="5432", dbname="postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{db_name}'
              AND pid <> pg_backend_pid();
        """)
    finally:
        cursor.close()
        conn.close()

@pytest.fixture(scope="session")
def test_db_name():
    db_name = "tgspin_test"
    
    conn = psycopg2.connect(user="postgres", password="postgres", host="localhost", port="5432")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    try:
        terminate_database_connections(db_name)
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name}")
    finally:
        cursor.close()
        conn.close()

    yield db_name

    terminate_database_connections(db_name)
    conn = psycopg2.connect(user="postgres", password="postgres", host="localhost", port="5432")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    try:
        cursor.execute(f"DROP DATABASE {db_name}")
    finally:
        cursor.close()
        conn.close()