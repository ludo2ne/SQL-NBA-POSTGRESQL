import logging
import os
import subprocess

import psycopg2
import s3fs
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("nba_pipeline")

AWS_ENDPOINT = os.environ["AWS_ENDPOINT_URL"]
DUMP_FILE = "nba.dump"
DUMP_FILEPATH = f"data/{DUMP_FILE}"

FILE_PATH = f"s3://ludo2ne/diffusion/ENSAI/SQL-TP/{DUMP_FILE}"

PG_HOST = os.getenv("POSTGRESQL_HOST")
PG_PORT = os.getenv("POSTGRESQL_PORT", "5432")
PG_DB = os.getenv("POSTGRESQL_DATABASE")
PG_USER = os.getenv("POSTGRESQL_USERNAME")
PG_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
PG_SCHEMA = os.getenv("POSTGRESQL_SCHEMA")

os.environ["PGPASSWORD"] = PG_PASSWORD

# --- Télécharger le dump depuis S3
fs = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": AWS_ENDPOINT},
    key=os.environ["AWS_ACCESS_KEY_ID"],
    secret=os.environ["AWS_SECRET_ACCESS_KEY"],
    token=os.environ["AWS_SESSION_TOKEN"],
)

logger.info("Téléchargement du dump depuis S3...")
with fs.open(FILE_PATH, "rb") as f_in:
    with open(DUMP_FILEPATH, "wb") as f_out:
        f_out.write(f_in.read())
logger.info(f"Dump téléchargé : {DUMP_FILEPATH}")

# --- Créer le schema si besoin
conn = psycopg2.connect(
    dbname=PG_DB, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT
)
conn.autocommit = True
cur = conn.cursor()
cur.execute(f"DROP SCHEMA IF EXISTS {PG_SCHEMA} CASCADE;")
cur.execute(f"CREATE SCHEMA {PG_SCHEMA};")
cur.close()
conn.close()

# --- Restaurer le dump
cmd = [
    "pg_restore",
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
    DUMP_FILEPATH,
]

logger.info("Restauration PostgreSQL...")
logger.info(str.join(" ", cmd))
subprocess.run(cmd, check=True)
logger.info("Base NBA restaurée dans PostgreSQL")
