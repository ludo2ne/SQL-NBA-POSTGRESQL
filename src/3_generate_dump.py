import os
import subprocess

from dotenv import load_dotenv

load_dotenv()

PG_HOST = os.getenv("POSTGRESQL_HOST")
PG_PORT = os.getenv("POSTGRESQL_PORT", "5432")
PG_DB = os.getenv("POSTGRESQL_DATABASE")
PG_USER = os.getenv("POSTGRESQL_USERNAME")
PG_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
PG_SCHEMA = os.getenv("POSTGRESQL_SCHEMA")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

DUMP_FILE = os.path.join(DATA_DIR, "nba.dump")

print("Création du dump PostgreSQL...")

cmd = [
    "pg_dump",
    "-h",
    PG_HOST,
    "-p",
    PG_PORT,
    "-U",
    PG_USER,
    "-d",
    PG_DB,
    "-n",
    PG_SCHEMA,
    "--no-owner",
    "--no-privileges",
    "-F",
    "c",
    "-f",
    DUMP_FILE,
]

subprocess.run(cmd, check=True)

print("Dump créé :", DUMP_FILE)
