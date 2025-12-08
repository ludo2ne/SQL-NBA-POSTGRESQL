# SQL-NBA-POSTGRESQL

Create nba database using nba_api

## Packages

All needed packages are in file called *requirements.txt*. Use the following command to install:

`pip install -r requirements.txt`

## Create .env file

Create a file called `.env` at the project root. Paste and fill these variables:

```
POSTGRESQL_HOST=
POSTGRESQL_PORT=5432
POSTGRESQL_DATABASE=
POSTGRESQL_USERNAME=
POSTGRESQL_PASSWORD=
POSTGRESQL_SCHEMA=nba
```

## Students : import nba data

- [ ] Open a *Vscode-python* service
- [ ] Open a terminal
  - CTRL + ù
- [ ] Clone this repository using *https*
- [ ] Open Folder of the repository
  - `code-server SQL-NBA-POSTGRESQL`
- [ ] Install needed packages
- [ ] Create `.env` file
- [ ] Update *pg_restore* version
  - actual version is 16 on VScode-python, needed : 17
  - `sudo apt update`
  - `sudo apt install postgresql-client-17`
- [ ] Run script `5_import_for_students.py`
- [ ] Check using cloudBeaver that the nba schema has been created in your database 


## Teacher

1. Call nba_api to obtain the data, convert it to df, then insert it into the database.
2. Post processing to fix some issues
3. Generate a dump file
4. Upload this dump file to S3


### :construction: Using api

Objective : 

- Create and launch an api
- Students can use the `restore` endpoint with a body containing the database connection information 


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