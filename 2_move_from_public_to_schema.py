import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

PG_HOST = os.getenv("POSTGRESQL_HOST")
PG_PORT = os.getenv("POSTGRESQL_PORT", "5432")
PG_DB = os.getenv("POSTGRESQL_DATABASE")
PG_USER = os.getenv("POSTGRESQL_USERNAME")
PG_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
PG_SCHEMA = os.getenv("POSTGRESQL_SCHEMA")


print(f"🚚 Déplacement des tables vers le schéma {PG_SCHEMA}...")

conn = psycopg2.connect(
    dbname=PG_DB, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT
)
conn.autocommit = True
cur = conn.cursor()

sql_create_schema = f"CREATE SCHEMA IF NOT EXISTS {PG_SCHEMA};"
cur.execute(sql_create_schema)

sql_move_tables = f"""
DO $$
DECLARE 
    r RECORD;
BEGIN
    FOR r IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    LOOP
        EXECUTE format('ALTER TABLE public.%I SET SCHEMA {PG_SCHEMA};', r.tablename);
    END LOOP;
END $$;
"""

sql_move_sequences = f"""
DO $$
DECLARE 
    r RECORD;
BEGIN
    FOR r IN
        SELECT sequence_name
        FROM information_schema.sequences
        WHERE sequence_schema = 'public'
    LOOP
        EXECUTE format('ALTER SEQUENCE public.%I SET SCHEMA {PG_SCHEMA};', r.sequence_name);
    END LOOP;
END $$;
"""

cur.execute(sql_move_tables)
cur.execute(sql_move_sequences)

cur.execute(
    f"GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA {os.getenv('POSTGRESQL_SCHEMA')} TO PUBLIC;"
)

cur.execute(
    f"ALTER DEFAULT PRIVILEGES IN SCHEMA {os.getenv('POSTGRESQL_SCHEMA')} GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO PUBLIC;"
)


cur.close()
conn.close()

print("✔️ Déplacement terminé")
