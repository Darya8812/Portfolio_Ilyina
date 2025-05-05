import dash
from dash import dcc, html
import pandas as pd
import sqlite3
import plotly.express as px

# Загружаем данные из SQLite
conn = sqlite3.connect("sales.db")
df = pd.read_sql("SELECT * FROM sales_dataset", conn)
conn.close()

# Преобразуем даты
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Month"] = df["Order Date"].dt.to_period("M").astype(str)

# Создаем графики
fig_sales_by_month = px.line(df.groupby("Month")["Sales"].sum().reset_index(),
                             x="Month", y="Sales", title="Динамика продаж по месяцам")

fig_top_products = px.bar(df.groupby("Product Name")["Sales"].sum().nlargest(10).reset_index(),
                          x="Sales", y="Product Name", title="Топ-10 товаров", orientation="h")

fig_category_sales = px.bar(df.groupby("Category")["Sales"].sum().reset_index(),
                            x="Category", y="Sales", title="Продажи по категориям")

# Создаем дашборд
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Анализ продаж"),
    dcc.Graph(figure=fig_sales_by_month),
    dcc.Graph(figure=fig_top_products),
    dcc.Graph(figure=fig_category_sales),
])

if __name__ == "__main__":
    app.run(debug=True)
