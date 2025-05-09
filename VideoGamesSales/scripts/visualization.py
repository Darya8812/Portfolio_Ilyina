import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Подключаемся к базе данных
conn = sqlite3.connect("sales.db")

# Топ-10 продаваемых игр
query_top_games = """
    SELECT Name, SUM(Global_Sales) AS Total_Sales
    FROM vgsales
    GROUP BY Name
    ORDER BY Total_Sales DESC
    LIMIT 10;
"""
df_top_games = pd.read_sql(query_top_games, conn)

# Продажи по жанрам
query_genre_sales = """
    SELECT Genre, SUM(Global_Sales) AS Total_Sales
    FROM vgsales
    GROUP BY Genre
    ORDER BY Total_Sales DESC;
"""
df_genre_sales = pd.read_sql(query_genre_sales, conn)

# Продажи по платформам
query_platform_sales = """
    SELECT Platform, SUM(Global_Sales) AS Total_Sales
    FROM vgsales
    GROUP BY Platform
    ORDER BY Total_Sales DESC;
"""
df_platform_sales = pd.read_sql(query_platform_sales, conn)

# Динамика продаж по годам
query_sales_by_year = """
    SELECT Year, SUM(Global_Sales) AS Total_Sales
    FROM vgsales
    GROUP BY Year
    ORDER BY Year;
"""
df_sales_by_year = pd.read_sql(query_sales_by_year, conn)

conn.close()

plt.figure(figsize=(12, 6))
sns.barplot(x="Total_Sales", y="Name", data=df_top_games, palette="Blues_r")
plt.title("Топ-10 продаваемых игр")
plt.xlabel("Продажи (млн копий)")
plt.ylabel("Название игры")
plt.show()

#Продажи по жанрам
plt.figure(figsize=(12, 6))
sns.barplot(x="Total_Sales", y="Genre", data=df_genre_sales, palette="coolwarm")
plt.title("Продажи по жанрам")
plt.xlabel("Продажи (млн копий)")
plt.ylabel("Жанр")
plt.show()

#Продажи по платформам
fig = px.bar(df_platform_sales, x="Platform", y="Total_Sales", title="Продажи по платформам", color="Platform")
fig.show()

# Динамика продаж по годам
plt.figure(figsize=(10, 5))
sns.lineplot(x="Year", y="Total_Sales", data=df_sales_by_year, marker="o", color="red")
plt.title("Динамика продаж видеоигр по годам")
plt.xlabel("Год")
plt.ylabel("Общий объем продаж (млн копий)")
plt.grid(True)
plt.show()
