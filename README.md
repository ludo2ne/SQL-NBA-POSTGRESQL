# SQL-NBA-POSTGRESQL
Import nba database from kaggle, import into PostgreSQL and create dump file


## Download nba database 

https://www.kaggle.com/datasets/wyattowalsh/basketball/data

Download file nba.sqllite

Todo : automate

## Create env file

```
POSTGRESQL_HOST=
POSTGRESQL_PORT=5432
POSTGRESQL_DATABASE=
POSTGRESQL_USERNAME=
POSTGRESQL_PASSWORD=
POSTGRESQL_SCHEMA=nba
```

## Run programs

- After step 2, drop large table *play_to_play* (2.5Go)
