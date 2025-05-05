import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Загружаем данные из SQLite
conn = sqlite3.connect("sales.db")
df = pd.read_sql("SELECT * FROM sales_dataset", conn)
conn.close()

# Проверяем данные
print(df.head())

df["Order Date"] = pd.to_datetime(df["Order Date"])  # Конвертируем даты
df["Month"] = df["Order Date"].dt.to_period("M")

# Группируем данные по месяцам
sales_by_month = df.groupby("Month")["Sales"].sum()

# Линейный график продаж по месяцам
sns.lineplot(x=df.groupby("Month")["Sales"].sum().index.astype(str),
             y=df.groupby("Month")["Sales"].sum().values, marker="o")
plt.xticks(rotation=45)
plt.title("Динамика продаж по месяцам")
plt.xlabel("Месяц")
plt.ylabel("Сумма продаж")
plt.show()

# Столбчатый график "Топ-10 товаров по продажам"
top_products = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_products.values, y=top_products.index)
plt.title("Топ-10 товаров по продажам")
plt.xlabel("Сумма продаж")
plt.ylabel("Товар")
plt.show()

# Столбчатый график "Продажи по категориям"
sales_by_category = df.groupby("Category")["Sales"].sum()

plt.figure(figsize=(10, 5))
sns.barplot(x=sales_by_category.index, y=sales_by_category.values)
plt.title("Продажи по категориям")
plt.xlabel("Категория")
plt.ylabel("Сумма продаж")
plt.xticks(rotation=30)
plt.show()

# Круговая диаграмма "Продажи по сегментам клиентов"
sales_by_segment = df.groupby("Segment")["Sales"].sum()

plt.figure(figsize=(7, 7))
plt.pie(sales_by_segment.values, labels=sales_by_segment.index, autopct="%1.1f%%", colors=sns.color_palette("pastel"))
plt.title("Распределение продаж по сегментам")
plt.show()
# Тепловая карта "Общий объем продаж по регионам"
sales_by_region = df.groupby("Region")["Sales"].sum()

plt.figure(figsize=(10, 5))
sns.heatmap(pd.DataFrame(sales_by_region), annot=True, cmap="coolwarm", fmt=".0f")
plt.title("Продажи по регионам")
plt.xlabel("Регион")
plt.ylabel("Объем продаж")
plt.show()
