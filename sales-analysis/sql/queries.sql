import sqlite3
import pandas as pd

conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Список таблиц:", cursor.fetchall())

# Запрос: общий объем продаж
cursor.execute("SELECT SUM(Sales) FROM sales_dataset")
print("Общий объем продаж:", cursor.fetchone()[0])
print()
# Топ-5 товаров по продажам
cursor.execute("""
    SELECT "Product Name", SUM(Sales) AS Total_Sales
    FROM sales_dataset
    GROUP BY "Product Name"
    ORDER BY Total_Sales DESC
    LIMIT 5
""")
# Преобразуем результат в DataFrame
df = pd.DataFrame(cursor.fetchall(), columns=["Month", "Total Sales"])
 # Вывод красивой таблицы
print("Топ-5 товаров по продажам:")
print(df)
print()

# Средний чек (средняя сумма продажи)
cursor.execute("SELECT AVG(Sales) FROM sales_dataset")
print("Средняя стоимость заказа:", cursor.fetchone()[0])
print()

# Количество заказов по категориям
cursor.execute("""
    SELECT Category, COUNT(*) AS "Order Count"
    FROM sales_dataset
    GROUP BY Category
    ORDER BY "Order Count" DESC
""")
print("Количество заказов по категориям:", cursor.fetchall())
print()

# Динамика продаж по месяцам
cursor.execute("""
    SELECT strftime('%Y-%m', date("Order Date")) AS Month, SUM(Sales) AS Total_Sales
    FROM sales_dataset
    GROUP BY Month
    ORDER BY Month
""")
# Преобразуем результат в DataFrame
df = pd.DataFrame(cursor.fetchall(), columns=["Month", "Total Sales"])
print("Продажи по месяцам:")
print(df)  # Вывод красивой таблицы
print()

# Анализ прибыльности товаров
cursor.execute("""
    SELECT "Product Name", SUM(Sales) AS Total_Sales
    FROM sales_dataset
    GROUP BY "Product Name"
    ORDER BY Total_Sales DESC
    LIMIT 10
""")
df_products = pd.DataFrame(cursor.fetchall(), columns=["Product Name", "Total Sales"])
print("Анализ прибыльности товаров")
print(df_products)
print()

# Продажи по сегментам клиентов
cursor.execute("""
    SELECT Segment, SUM(Sales) AS Total_Sales
    FROM sales_dataset
    GROUP BY Segment
    ORDER BY Total_Sales DESC
""")
df_segments = pd.DataFrame(cursor.fetchall(), columns=["Segment", "Total Sales"])
print("Продажи по сегментам клиентов")
print(df_segments)
print()

#Анализ динамики продаж по категориям
cursor.execute("""
    SELECT Category, SUM(Sales) AS Total_Sales
    FROM sales_dataset
    GROUP BY Category
    ORDER BY Total_Sales DESC
""")
df_categories = pd.DataFrame(cursor.fetchall(), columns=["Category", "Total Sales"])
print("Динамика продаж по категориям")
print(df_categories)
conn.close()


