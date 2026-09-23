import os
import urllib.parse

import pyodbc
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


# ============================================================
# ODBC DRIVER
# ============================================================

available_drivers = pyodbc.drivers()

if "ODBC Driver 18 for SQL Server" in available_drivers:
    DRIVER = "ODBC Driver 18 for SQL Server"

elif "ODBC Driver 17 for SQL Server" in available_drivers:
    DRIVER = "ODBC Driver 17 for SQL Server"

else:
    raise RuntimeError(
        "No supported SQL Server ODBC driver found. "
        f"Available drivers: {available_drivers}"
    )


# ============================================================
# CONNECTION
# ============================================================

connection_string = (
    f"DRIVER={{{DRIVER}}};"
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
    f"mssql+pyodbc:///?odbc_connect={params}",
    pool_pre_ping=True
)