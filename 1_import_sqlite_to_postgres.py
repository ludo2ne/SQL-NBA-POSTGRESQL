import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv

# Charger les variables d'environnement du .env
load_dotenv()

PG_HOST = os.getenv("POSTGRESQL_HOST")
PG_PORT = os.getenv("POSTGRESQL_PORT", "5432")
PG_DB = os.getenv("POSTGRESQL_DATABASE")
PG_USER = os.getenv("POSTGRESQL_USERNAME")
PG_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")

SQLITE_FILE = "nba.sqlite"

if not Path(SQLITE_FILE).exists():
    raise FileNotFoundError(f"Fichier SQLite introuvable : {SQLITE_FILE}")

cmd = [
    "pgloader",
    f"sqlite://{SQLITE_FILE}",
    f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}",
]

print("⏳ Import SQLite → PostgreSQL via pgloader...")
subprocess.run("ls", check=True)
subprocess.run("pwd", check=True)
subprocess.run(cmd, check=True)
print("✅ Import terminé.")
