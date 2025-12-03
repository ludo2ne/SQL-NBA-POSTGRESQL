import os
import subprocess

import psycopg2
import s3fs
from dotenv import load_dotenv

#---------------------------------------------------------------------
# Chargement des variables d environnement
#---------------------------------------------------------------------

os.environ["AWS_ACCESS_KEY_ID"] = 'OZHRXI98VQWP2S2OU250'
os.environ["AWS_SECRET_ACCESS_KEY"] = '35pTciJJ3SC2XNXX+LsdCSW2rXVkK+BFWpEgZxPk'
os.environ["AWS_SESSION_TOKEN"] = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJPWkhSWEk5OFZRV1AyUzJPVTI1MCIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sImF1ZCI6WyJtaW5pby1kYXRhbm9kZSIsIm9ueXhpYSIsImFjY291bnQiXSwiYXV0aF90aW1lIjoxNzY0NzY1MTU5LCJhenAiOiJvbnl4aWEiLCJlbWFpbCI6Imx1ZG92aWMuZGVuZXV2aWxsZUBlbnNhaS5mciIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJleHAiOjE3NjUzNzAzNjUsImZhbWlseV9uYW1lIjoiRGVuZXV2aWxsZSIsImdpdmVuX25hbWUiOiJMdWRvdmljIiwiZ3JvdXBzIjpbIlVTRVJfT05ZWElBIl0sImlhdCI6MTc2NDc2NTU2NSwiaXNzIjoiaHR0cHM6Ly9hdXRoLmxhYi5zc3BjbG91ZC5mci9hdXRoL3JlYWxtcy9zc3BjbG91ZCIsImp0aSI6Im9ucnRydDo3Yzk2NTBiNy1mZGNmLWI0MzAtOWMyZC05YTQ1Y2UyODFhMzYiLCJuYW1lIjoiTHVkb3ZpYyBEZW5ldXZpbGxlIiwicG9saWN5Ijoic3Rzb25seSIsInByZWZlcnJlZF91c2VybmFtZSI6Imx1ZG8ybmUiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3NwY2xvdWQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiZGVmYXVsdC1yb2xlcy1zc3BjbG91ZCJdLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGdyb3VwcyBlbWFpbCIsInNpZCI6IjdmMjVmZTg3LTIwOGItNGM0Yi05MzhhLTRkOTAzYzI5ZjY3NiIsInN1YiI6ImEwZWVmMTNkLTNjZDMtNDA3ZS1iMWEwLTNiNWM1MjIwNjM0OSIsInR5cCI6IkJlYXJlciJ9.jHzLyzCc9idhYefbIvzVrMbmKgpZVLG1HcMd6UaVSMtziFquqnTWWrTMjmajuXS-NFNu51QjUTkRnQslF9BTsA'
os.environ["AWS_DEFAULT_REGION"] = 'us-east-1'

load_dotenv()

AWS_ENDPOINT = os.environ["AWS_ENDPOINT_URL"]
DUMP_FILE = "nba.dump"
FILE_PATH = f"s3://ludo2ne/diffusion/ENSAI/SQL-TP/{DUMP_FILE}"

PG_HOST = os.getenv("POSTGRESQL_HOST")
PG_PORT = os.getenv("POSTGRESQL_PORT", "5432")
PG_DB = os.getenv("POSTGRESQL_DATABASE")
PG_USER = os.getenv("POSTGRESQL_USERNAME")
PG_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
PG_SCHEMA = os.getenv("POSTGRESQL_SCHEMA")

os.environ["PGPASSWORD"] = PG_PASSWORD         # utilisee par pg_restore


#---------------------------------------------------------------------
# Connexion au stockage S3 et Import du fichier dump
#---------------------------------------------------------------------

fs = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": AWS_ENDPOINT},
    key=os.environ["AWS_ACCESS_KEY_ID"],
    secret=os.environ["AWS_SECRET_ACCESS_KEY"],
    token=os.environ["AWS_SESSION_TOKEN"],
)

print("Téléchargement du dump depuis S3...")
with fs.open(FILE_PATH, "rb") as f_in:
    with open(DUMP_FILE, "wb") as f_out:
        f_out.write(f_in.read())
print("Dump téléchargé")


#---------------------------------------------------------------------
# Connexion a la base de donnees et restauration du dump
#---------------------------------------------------------------------

conn = psycopg2.connect(
    dbname=PG_DB, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT
)
conn.autocommit = True
cur = conn.cursor()

sql_create_schema = f"CREATE SCHEMA IF NOT EXISTS {PG_SCHEMA};"
cur.execute(sql_create_schema)

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
    DUMP_FILE,
]


print("Restauration PostgreSQL...")
subprocess.run(cmd, check=True)
print("Base NBA restaurée dans votre PostgreSQL")
