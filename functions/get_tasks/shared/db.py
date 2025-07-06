import boto3
import os
import json
import pymysql

_cached_secret = None

def get_db_credentials():
    global _cached_secret
    if _cached_secret:
        return _cached_secret

    secret_name = os.environ["DB_SECRET_NAME"]
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    client = boto3.client("secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)

    _cached_secret = json.loads(response["SecretString"])
    return _cached_secret

def get_connection():
    creds = get_db_credentials()
    return pymysql.connect(
        host=creds["host"],
        port=int(creds.get("port", 3306)),
        user=creds["username"],
        password=creds["password"],
        database=creds["database"],
        cursorclass=pymysql.cursors.DictCursor
    )
