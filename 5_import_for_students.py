import os
import subprocess

import psycopg2
import s3fs
from dotenv import load_dotenv

load_dotenv()

AWS_ENDPOINT = os.environ["AWS_ENDPOINT_URL"]
DUMP_FILE = "nba.dump"
FILE_PATH = f"s3://ludo2ne/diffusion/ENSAI/SQL-TP/{DUMP_FILE}"

fs = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": AWS_ENDPOINT},
    key=os.environ["AWS_ACCESS_KEY_ID"],
    secret=os.environ["AWS_SECRET_ACCESS_KEY"],
    token=os.environ["AWS_SESSION_TOKEN"],
)

print("📥 Téléchargement du dump depuis S3...")
with fs.open(FILE_PATH, "rb") as f_in:
    with open(DUMP_FILE, "wb") as f_out:
        f_out.write(f_in.read())
print("✅ Dump téléchargé :")


PG_HOST = os.getenv("POSTGRESQL_HOST")
PG_PORT = os.getenv("POSTGRESQL_PORT", "5432")
PG_DB = os.getenv("POSTGRESQL_DATABASE")
PG_USER = os.getenv("POSTGRESQL_USERNAME")
PG_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
PG_SCHEMA = os.getenv("POSTGRESQL_SCHEMA")

os.environ["PGPASSWORD"] = PG_PASSWORD

conn = psycopg2.connect(
    dbname=PG_DB, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT
)
conn.autocommit = True
cur = conn.cursor()

sql_create_schema = f"CREATE SCHEMA IF NOT EXISTS {PG_SCHEMA};"
cur.execute(sql_create_schema)

cmd = [
    "pg_restore",
    "-n",
    "nba",
    "-d",
    PG_DB,
    "-h",
    PG_HOST,
    "-p",
    PG_PORT,
    "-U",
    PG_USER,
    "-n",
    PG_SCHEMA,
    DUMP_FILE,
]


print("⏳ Restauration PostgreSQL...")
subprocess.run(cmd, check=True)
print("🎉 Base NBA restaurée dans votre PostgreSQL")
