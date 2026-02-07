import pyodbc

def get_connection():
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=LOQ\SQLEXPRESS;"
        "Database=career_db;"
        "Trusted_Connection=yes;"
    )
    return conn
