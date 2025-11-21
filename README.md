# SQL-NBA-POSTGRESQL

Create nba database using nba_api

## Create env file

```
POSTGRESQL_HOST=
POSTGRESQL_PORT=5432
POSTGRESQL_DATABASE=
POSTGRESQL_USERNAME=
POSTGRESQL_PASSWORD=
POSTGRESQL_SCHEMA=nba
```

## Using api

run: `uvicorn 6_import_for_students_api:app --host 0.0.0.0 --port 8000`

call:

```
curl -X POST http://localhost:8000/restore \
  -H "Content-Type: application/json" \
  -d '{
    "PG_HOST": "postgresql-xxxxxx.user-yyyyy",
    "PG_PORT": 5432,
    "PG_DB": "defaultdb",
    "PG_USER": "admin",
    "PG_PASSWORD": "mypassword"
  }'
```