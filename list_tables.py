import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
PROJECT_ROOT = os.getenv('PROJECT_ROOT', os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, 'env', 'botssys', 'sqlitedb', 'botsdb')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables in database:')
for t in tables:
    print(f'  {t[0]}')
conn.close()
