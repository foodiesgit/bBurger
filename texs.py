import pandas as pd
from datetime import datetime
import sqlite3
SQLITE_PATH = "/Users/enriquecrespodebenito/Desktop/Betburger API/surebets.sqlite"
sqliteConnection = sqlite3.connect(SQLITE_PATH)
cursor = sqliteConnection.cursor()


df = pd.read_sql_query("SELECT * from arbs", con=sqliteConnection)

print(df)