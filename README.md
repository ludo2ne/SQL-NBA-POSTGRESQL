# SQL-NBA-POSTGRESQL
Import nba database from kaggle, import into PostgreSQL and create dump file

## Setup

```
sudo apt update
sudo apt install pgloader
sudo apt install postgresql-client-17

pgloader sqlite://nba.sqlite postgresql://user-ludo2ne:iyw7imls8vqbslosgy6b@postgresql-727754.user-ludo2ne/defaultdb


sqlite3 nba.sqlite "SELECT name FROM sqlite_master WHERE type='table';"
sqlite3 nba.sqlite "PRAGMA table_info(player)"
```

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


```{.sql}
ALTER TABLE nba.team
ADD COLUMN conference VARCHAR(10);


UPDATE nba.team
SET conference = CASE nickname
    WHEN 'Hawks' THEN 'East'
    WHEN 'Celtics' THEN 'East'
    WHEN 'Cavaliers' THEN 'East'
    WHEN 'Bulls' THEN 'East'
    WHEN 'Heat' THEN 'East'
    WHEN 'Bucks' THEN 'East'
    WHEN 'Magic' THEN 'East'
    WHEN 'Pacers' THEN 'East'
    WHEN '76ers' THEN 'East'
    WHEN 'Nets' THEN 'East'
    WHEN 'Knicks' THEN 'East'
    WHEN 'Raptors' THEN 'East'
    WHEN 'Hornets' THEN 'East'
    WHEN 'Pistons' THEN 'East'
    WHEN 'Wizards' THEN 'East'
    WHEN 'Hawks' THEN 'East'
    WHEN 'Mavericks' THEN 'West'
    WHEN 'Nuggets' THEN 'West'
    WHEN 'Warriors' THEN 'West'
    WHEN 'Rockets' THEN 'West'
    WHEN 'Clippers' THEN 'West'
    WHEN 'Lakers' THEN 'West'
    WHEN 'Timberwolves' THEN 'West'
    WHEN 'Suns' THEN 'West'
    WHEN 'Trail Blazers' THEN 'West'
    WHEN 'Kings' THEN 'West'
    WHEN 'Spurs' THEN 'West'
    WHEN 'Thunder' THEN 'West'
    WHEN 'Jazz' THEN 'West'
    WHEN 'Grizzlies' THEN 'West'
    WHEN 'Pelicans' THEN 'West'
    ELSE NULL
END;
```