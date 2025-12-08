import logging
import os
import random
import time
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from nba_api.stats.endpoints import (
    BoxScoreTraditionalV3,
    CommonAllPlayers,
    LeagueDashPlayerStats,
    LeagueGameFinder,
)
from sqlalchemy import create_engine, text

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("nba_pipeline")

load_dotenv()

SLEEP_BETWEEN_REQUESTS = 1
SEASON = "2024-25"

PG_HOST = os.getenv("POSTGRESQL_HOST")
PG_PORT = os.getenv("POSTGRESQL_PORT", "5432")
PG_DATABASE = os.getenv("POSTGRESQL_DATABASE")
PG_USER = os.getenv("POSTGRESQL_USERNAME")
PG_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
PG_SCHEMA = os.getenv("POSTGRESQL_SCHEMA")

ENGINE = create_engine(
    f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:5432/{PG_DATABASE}"
)

with ENGINE.begin() as conn:
    conn.execute(text(f"DROP SCHEMA IF EXISTS {PG_SCHEMA} CASCADE;"))
    conn.execute(text(f"CREATE SCHEMA {PG_SCHEMA};"))


def fetch_endpoint(endpoint_class, **kwargs):
    """
    Appelle un endpoint nba_api et retourne directement un DataFrame
    avec les colonnes converties en minuscules.
    """
    try:
        endpoint = endpoint_class(**kwargs)
        time.sleep(SLEEP_BETWEEN_REQUESTS)  # pause pour éviter throttling
        dfs = endpoint.get_data_frames()
        if dfs:
            df = dfs[0].copy()
            df.columns = [c.lower() for c in df.columns]
            logger.info(
                f"{len(df)} lignes récupérées pour {endpoint_class.__name__}/{list(kwargs.values())}"
            )
            return df
        else:
            logger.warning(f"Aucun DataFrame retourné par {endpoint_class.__name__}")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Erreur fetch endpoint {endpoint_class.__name__}: {e}")
        return pd.DataFrame()


# ---------------------------------------------------------
# Import des joueurs
# ---------------------------------------------------------

players_df = fetch_endpoint(CommonAllPlayers, is_only_current_season=0)


# ---------------------------------------------------------
# Import des matchs et des stats par saison
# ---------------------------------------------------------

all_games = []
all_stats = []

current_year = datetime.now().year
seasons = [f"{y}-{str(y + 1)[-2:]}" for y in range(2000, current_year + 1)]

logger.info("-" * 50)
logger.info(f"Liste des saisons à récupérer : {seasons}")
logger.info("-" * 50)

for season in seasons:
    try:
        df_games = fetch_endpoint(
            LeagueGameFinder, season_nullable=season, season_type_nullable="Regular Season"
        )
        df_games["season_type"] = "Regular Season"
        current_regular_season_id = df_games["season_id"].iloc[0]
        all_games.append(df_games)

        df_games = fetch_endpoint(
            LeagueGameFinder, season_nullable=season, season_type_nullable="Playoffs"
        )
        df_games["season_type"] = "Playoffs"
        all_games.append(df_games)

        df_stats = fetch_endpoint(
            LeagueDashPlayerStats, season=season, season_type_all_star="Regular Season"
        )
        df_stats["season_id"] = current_regular_season_id
        cols = ["season_id"] + [c for c in df_stats.columns if c != "season_id"]
        df_stats = df_stats[cols]
        all_stats.append(df_stats)

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des matchs pour la saison {season}: {e}")

# Concaténation finale
valid_games = [df for df in all_games if not df.empty]
games_df = pd.concat(valid_games, ignore_index=True) if valid_games else pd.DataFrame()
regular_season_stats_df = pd.concat(all_stats, ignore_index=True)


# ---------------------------------------------------------
# Stats par match de la dernière saison
# ---------------------------------------------------------

latest_season = games_df["season_id"].max()

latest_season = games_df.loc[games_df["season_type"] == "Regular Season", "season_id"].max()
latest_season_games_id = games_df.loc[games_df["season_id"] == latest_season, "game_id"].unique()

logger.info("-" * 50)
logger.info(
    f"Stats par match de la dernière saison régulière : {latest_season} -> {len(latest_season_games_id)} games"
)
logger.info("-" * 50)

all_player_stats = []

for idx, game_id in enumerate(latest_season_games_id, start=1):
    try:
        logger.info(
            f"[{idx}/{len(latest_season_games_id)}] Récupération stats pour game_id={game_id}"
        )
        player_stats_df = fetch_endpoint(BoxScoreTraditionalV3, game_id=game_id)

        if not player_stats_df.empty:
            all_player_stats.append(player_stats_df)
        else:
            logger.warning(f"Aucune stat renvoyée pour game_id={game_id}")

    except Exception as e:
        logger.error(f"Erreur pour game_id={game_id}: {e}")

    # Pause aléatoire pour réduire les risques de throttling
    time.sleep(SLEEP_BETWEEN_REQUESTS + random.uniform(0, 0.5))

if all_player_stats:
    player_stats_df = pd.concat(all_player_stats, ignore_index=True)
    player_stats_df.columns = [c.lower() for c in player_stats_df.columns]
    logger.info(f"Total stats récupérées : {len(player_stats_df)} lignes")
else:
    player_stats_df = pd.DataFrame()
    logger.warning("Aucune stat joueur récupérée")


# ---------------------------------------------------------
# Création des tables
# ---------------------------------------------------------


def df_to_postgres_table(df, table_name):
    """
    Crée une table PostgreSQL à partir d'un DataFrame et insère les données.
    """
    if df.empty:
        logger.warning(
            f"Le DataFrame pour la table '{table_name}' est vide. Aucune insertion effectuée."
        )
        return

    try:
        # Conversion des colonnes
        df_copy = df.copy()
        for col in df_copy.columns:
            if pd.api.types.is_numeric_dtype(df_copy[col]):
                df_copy[col] = pd.to_numeric(df_copy[col], errors="coerce")
            else:
                df_copy[col] = df_copy[col].astype(str)

        df_copy.columns = [c.lower() for c in df_copy.columns]

        # Insertion dans PostgreSQL
        df_copy.to_sql(
            name=table_name, con=ENGINE, schema=PG_SCHEMA, if_exists="replace", index=False
        )

        logger.info(
            f"Insertion terminée pour la table '{table_name}' ({len(df_copy)} lignes insérées)."
        )

    except Exception as e:
        logger.error(f"Erreur lors de l'insertion dans la table '{table_name}': {e}")


logger.info("-" * 50)
logger.info("Création des tables")
logger.info("-" * 50)

df_to_postgres_table(players_df, "player")
df_to_postgres_table(games_df, "game")
df_to_postgres_table(regular_season_stats_df, "regular_season_stat")
df_to_postgres_table(player_stats_df, "player_stat_match")
