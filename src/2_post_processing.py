import logging
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql

# ---------------------------------------------------------
# Logger configuration
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("nba_pipeline")

# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------
load_dotenv()

PG_HOST = os.getenv("POSTGRESQL_HOST")
PG_PORT = os.getenv("POSTGRESQL_PORT", "5432")
PG_DATABASE = os.getenv("POSTGRESQL_DATABASE")
PG_USER = os.getenv("POSTGRESQL_USERNAME")
PG_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
PG_SCHEMA = os.getenv("POSTGRESQL_SCHEMA")

# ---------------------------------------------------------
# Locate SQL script
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # project root
SQL_FILE = BASE_DIR / "data" / "cleaning_tables.sql"

logger.info(f"Fichier SQL détecté : {SQL_FILE}")

if not SQL_FILE.exists():
    logger.error(f"Le fichier SQL n'existe pas : {SQL_FILE}")
    raise FileNotFoundError(f"Fichier introuvable : {SQL_FILE}")

# ---------------------------------------------------------
# Read SQL file
# ---------------------------------------------------------
try:
    sql_commands = SQL_FILE.read_text(encoding="utf-8")
    logger.info("Script SQL chargé avec succès.")
except Exception as e:
    logger.error(f"Erreur lecture fichier SQL : {e}")
    raise

# ---------------------------------------------------------
# Connect to PostgreSQL
# ---------------------------------------------------------
logger.info("Connexion à PostgreSQL...")

try:
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
    )
    cur = conn.cursor()
    logger.info("Connexion PostgreSQL établie.")
except Exception as e:
    logger.error(f"Impossible de se connecter à PostgreSQL : {e}")
    raise

# ---------------------------------------------------------
# Execute SQL script
# ---------------------------------------------------------
logger.info("Exécution du script SQL...")

try:
    cur.execute(sql.SQL(sql_commands))
    conn.commit()
    logger.info("Script SQL exécuté avec succès.")
except Exception as e:
    conn.rollback()
    logger.error(f"Erreur lors de l'exécution du SQL : {e}")
    raise
finally:
    cur.close()
    conn.close()
    logger.info("Connexion PostgreSQL fermée.")
