import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Подключаемся к базе данных
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# Запросы данных
cursor.execute("""
    SELECT Genre, SUM(Global_Sales) AS Total_Sales
    FROM vgsales
    GROUP BY Genre
    ORDER BY Total_Sales DESC;
""")
df_genre_sales = pd.DataFrame(cursor.fetchall(), columns=["Genre", "Total Sales"])

cursor.execute("""
    SELECT Platform, SUM(Global_Sales) AS Total_Sales
    FROM vgsales
    GROUP BY Platform
    ORDER BY Total_Sales DESC;
""")
df_platform_sales = pd.DataFrame(cursor.fetchall(), columns=["Platform", "Total Sales"])

cursor.execute("""
    SELECT Publisher, SUM(Global_Sales) AS Total_Sales
    FROM vgsales
    GROUP BY Publisher
    ORDER BY Total_Sales DESC
    LIMIT 10;
""")
df_publisher_share = pd.DataFrame(cursor.fetchall(), columns=["Publisher", "Total Sales"])

cursor.execute("""
    SELECT Year, COUNT(*) AS Game_Count, SUM(Global_Sales) AS Total_Sales
    FROM vgsales
    GROUP BY Year
    ORDER BY Year;
""")
df_digital_sales_trend = pd.DataFrame(cursor.fetchall(), columns=["Year", "Game Count", "Total Sales"])

cursor.execute("""
    SELECT Name, SUM(Global_Sales) AS Total_Sales
    FROM vgsales
    GROUP BY Name
    ORDER BY Total_Sales DESC
    LIMIT 10;
""")
df_top_games = pd.DataFrame(cursor.fetchall(), columns=["Game Name", "Total Sales"])

conn.close()

# Настраиваем стиль графиков
sns.set_style("whitegrid")
fig, axes = plt.subplots(3, 2, figsize=(18, 15))

# Визуализация 1: Продажи по жанрам
sns.barplot(x="Total Sales", y="Genre", data=df_genre_sales, palette="coolwarm", ax=axes[0, 0])
axes[0, 0].set_title("Продажи по жанрам")
axes[0, 0].set_xlabel("Продажи (млн копий)")
axes[0, 0].set_ylabel("Жанр")

# Визуализация 2: Продажи по платформам
sns.barplot(x="Total Sales", y="Platform", data=df_platform_sales, palette="viridis", ax=axes[0, 1])
axes[0, 1].set_title("Продажи по платформам")
axes[0, 1].set_xlabel("Продажи (млн копий)")
axes[0, 1].set_ylabel("Платформа")

# Визуализация 3: Доля издателей на рынке
sns.barplot(x="Total Sales", y="Publisher", data=df_publisher_share, palette="pastel", ax=axes[1, 0])
axes[1, 0].set_title("Топ-10 издателей")
axes[1, 0].set_xlabel("Продажи (млн копий)")
axes[1, 0].set_ylabel("Издатель")

# Визуализация 4: Динамика продаж по годам
sns.lineplot(x="Year", y="Total Sales", data=df_digital_sales_trend, marker="o", color="blue", label="Общий объем продаж", ax=axes[1, 1])
axes[1, 1].set_title("Динамика продаж по годам")
axes[1, 1].set_xlabel("Год")
axes[1, 1].set_ylabel("Продажи (млн копий)")
axes[1, 1].legend()
axes[1, 1].grid(True)

# Визуализация 5: Топ-10 продаваемых игр
sns.barplot(x="Total Sales", y="Game Name", data=df_top_games, palette="magma", ax=axes[2, 0])
axes[2, 0].set_title("Топ-10 продаваемых игр")
axes[2, 0].set_xlabel("Продажи (млн копий)")
axes[2, 0].set_ylabel("Игра")

# Выключаем пустую ячейку
axes[2, 1].axis("off")

plt.tight_layout()
plt.show()
