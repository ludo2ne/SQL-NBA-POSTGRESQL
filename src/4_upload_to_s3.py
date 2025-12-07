import os

import s3fs

AWS_ENDPOINT = os.environ["AWS_ENDPOINT_URL"]
AWS_KEY = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_TOKEN = os.environ.get("AWS_SESSION_TOKEN")

USERNAME = "ludo2ne"
DUMP_FILE = "nba.dump"


print("Upload vers S3...")

fs = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": AWS_ENDPOINT}, key=AWS_KEY, secret=AWS_SECRET, token=AWS_TOKEN
)

destination = f"s3://{USERNAME}/diffusion/ENSAI/SQL-TP/{DUMP_FILE}"

with fs.open(destination, mode="wb") as f_out:
    with open(f"data/{DUMP_FILE}", "rb") as f_in:
        f_out.write(f_in.read())


print("Dump uploadé sur S3")
