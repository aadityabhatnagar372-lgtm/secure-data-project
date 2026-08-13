import os

import psycopg


def get_connection():
    """Create a PostgreSQL connection using environment variables."""
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "secure_data"),
        user=os.getenv("DB_USER", "secure_user"),
        password=os.getenv("DB_PASSWORD", "secure_password"),
    )