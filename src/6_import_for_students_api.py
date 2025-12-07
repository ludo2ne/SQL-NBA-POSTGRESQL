import os
import subprocess
import traceback

import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="NBA Restore API")


# -----------------------------
# Body du POST
# -----------------------------
class PGConfig(BaseModel):
    PG_HOST: str
    PG_PORT: int = 5432
    PG_DB: str
    PG_USER: str
    PG_PASSWORD: str
    PG_SCHEMA: str = "nba"  # optionnel


@app.post("/restore")
def restore_database(cfg: PGConfig):
    try:
        # ======================================================
        # 1) Download depuis S3
        # ======================================================
        DUMP_FILE = "nba.dump"
        os.environ["PGPASSWORD"] = cfg.PG_PASSWORD

        conn = psycopg2.connect(
            dbname=cfg.PG_DB,
            user=cfg.PG_USER,
            password=cfg.PG_PASSWORD,
            host=cfg.PG_HOST,
            port=cfg.PG_PORT,
        )
        conn.autocommit = True
        cur = conn.cursor()

        sql_create_schema = f"CREATE SCHEMA IF NOT EXISTS {cfg.PG_SCHEMA};"
        cur.execute(sql_create_schema)
        cur.close()
        conn.close()

        # ======================================================
        # 3) pg_restore
        # ======================================================
        print("Restauration PostgreSQL...")

        cmd = [
            "pg_restore",
            "-d",
            cfg.PG_DB,
            "-h",
            cfg.PG_HOST,
            "-p",
            str(cfg.PG_PORT),
            "-U",
            cfg.PG_USER,
            "-n",
            cfg.PG_SCHEMA,
            DUMP_FILE,
        ]

        subprocess.run(cmd, check=True)

        print("Base NBA restaurée dans PostgreSQL")

        return JSONResponse({"status": "success", "message": "NBA restored successfully"})

    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(
            {
                "status": "error",
                "error_type": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc(),
            },
            status_code=500,
        )
