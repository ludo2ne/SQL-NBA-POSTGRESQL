import os
import subprocess

import psycopg2
import s3fs
from dotenv import load_dotenv

load_dotenv()

AWS_ENDPOINT = os.environ["AWS_ENDPOINT_URL"]
DUMP_FILE = "nba.dump"
FILE_PATH = f"s3://ludo2ne/diffusion/ENSAI/SQL-TP/{DUMP_FILE}"

os.environ["AWS_ACCESS_KEY_ID"] = "95IEK0JBR89OHWUGFBQ5"
os.environ["AWS_SECRET_ACCESS_KEY"] = "zEsK4aMKqvG7hIdEEzKxTggM3eoLdRB++2CJqrlV"
os.environ["AWS_SESSION_TOKEN"] = (
    "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiI5NUlFSzBKQlI4OU9IV1VHRkJRNSIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sImF1ZCI6WyJtaW5pby1kYXRhbm9kZSIsIm9ueXhpYSIsImFjY291bnQiXSwiYXV0aF90aW1lIjoxNzYzMzcwMzM5LCJhenAiOiJvbnl4aWEiLCJlbWFpbCI6Imx1ZG92aWMuZGVuZXV2aWxsZUBlbnNhaS5mciIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJleHAiOjE3NjQzNDEzNDQsImZhbWlseV9uYW1lIjoiRGVuZXV2aWxsZSIsImdpdmVuX25hbWUiOiJMdWRvdmljIiwiZ3JvdXBzIjpbIlVTRVJfT05ZWElBIl0sImlhdCI6MTc2MzczNjU0NCwiaXNzIjoiaHR0cHM6Ly9hdXRoLmxhYi5zc3BjbG91ZC5mci9hdXRoL3JlYWxtcy9zc3BjbG91ZCIsImp0aSI6Im9ucnRydDowNjAyZTBkZC0yNjgyLTQ1NGQtZjFkNC1hMDhiNDJmNjRmZDAiLCJuYW1lIjoiTHVkb3ZpYyBEZW5ldXZpbGxlIiwicG9saWN5Ijoic3Rzb25seSIsInByZWZlcnJlZF91c2VybmFtZSI6Imx1ZG8ybmUiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3NwY2xvdWQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiZGVmYXVsdC1yb2xlcy1zc3BjbG91ZCJdLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGdyb3VwcyBlbWFpbCIsInNpZCI6IjJmMTkxYTJiLWM4NzEtNDI5MS04M2E4LTQxZGQ0MGI2MDQwMSIsInN1YiI6ImEwZWVmMTNkLTNjZDMtNDA3ZS1iMWEwLTNiNWM1MjIwNjM0OSIsInR5cCI6IkJlYXJlciJ9.WYizYqtDtj58sQiVuYyrBK_UfzyZrNdj2U1Ou5_l5r1e6qvFm7vKjgXEofq2FUTmL9NTWQPghDS1eaUVUUy0Rw"
)
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

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
