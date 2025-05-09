import sqlite3
import pandas as pd

# Создаем базу SQLite
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# Загружаем CSV
df = pd.read_csv("D:/sales_dataset.csv")

# Перезаписываем таблицу в SQLite
df.to_sql("sales_dataset", conn, if_exists="replace", index=False)

# Сохраняем данные в таблицу SQL
df.to_sql("sales_dataset", conn, if_exists="replace", index=False)

# Проверяем, что данные загрузились
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Список таблиц:", cursor.fetchall())  # Выведет все таблицы в базе


conn.close()
