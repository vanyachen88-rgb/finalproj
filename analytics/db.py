from sqlalchemy import text
from etl.db import engine


def read_sql(query: str):
    """
    Execute SQL query and return a Pandas DataFrame.
    """
    import pandas as pd

    with engine.connect() as conn:
        return pd.read_sql(
            text(query),
            conn
        )