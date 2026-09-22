import os
import urllib.parse

from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

SERVER = os.getenv("DB_SERVER")
DATABASE = os.getenv("DB_NAME")
USERNAME = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")


if not all([
    SERVER,
    DATABASE,
    USERNAME,
    PASSWORD
]):
    raise ValueError(
        "Database environment variables are missing."
    )


connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

params = urllib.parse.quote_plus(
    connection_string
)

engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params}"
)