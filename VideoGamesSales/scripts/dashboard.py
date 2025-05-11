import sqlite3
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Подключаемся к базе данных
conn = sqlite3.connect("sales.db")

# Загружаем данные
df_genre_sales = pd.read_sql("""
    SELECT Genre, SUM(Global_Sales) AS Total_Sales
    FROM vgsales
    GROUP BY Genre
    ORDER BY Total_Sales DESC;
""", conn)

df_platform_sales = pd.read_sql("""
    SELECT Platform, SUM(Global_Sales) AS Total_Sales
    FROM vgsales
    GROUP BY Platform
    ORDER BY Total_Sales DESC;
""", conn)

df_publisher_sales = pd.read_sql("""
    SELECT Publisher, SUM(Global_Sales) AS Total_Sales
    FROM vgsales
    GROUP BY Publisher
    ORDER BY Total_Sales DESC
    LIMIT 10;
""", conn)

df_yearly_sales = pd.read_sql("""
    SELECT Year, SUM(Global_Sales) AS Total_Sales
    FROM vgsales
    GROUP BY Year
    ORDER BY Year;
""", conn)

df_top_games = pd.read_sql("""
    SELECT Name, SUM(Global_Sales) AS Total_Sales
    FROM vgsales
    GROUP BY Name
    ORDER BY Total_Sales DESC
    LIMIT 10;
""", conn)

conn.close()

# Создаем приложение Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Анализ продаж видеоигр", style={"textAlign": "center", "color": "#4CAF50"}),

    # Фильтр по году
    html.Div([
        html.Label("Выбери год:", style={"fontSize": "16px", "color": "#333"}),
        dcc.Dropdown(
            id="year-filter",
            options=[{"label": str(year), "value": year} for year in df_yearly_sales["Year"]],
            value=df_yearly_sales["Year"].max(),
            placeholder="Выбери год",
            style={"width": "50%"}
        )
    ], style={"padding": "20px"}),

    # График продаж по жанрам
    dcc.Graph(
        id="genre-sales-graph",
        figure=px.bar(df_genre_sales, x="Total_Sales", y="Genre", orientation="h",
                      title="Продажи по жанрам", color="Genre",
                      labels={"Total_Sales": "Продажи (млн копий)", "Genre": "Жанр"},
                      color_discrete_sequence=px.colors.qualitative.Set3)
    ),

    # График продаж по платформам
    dcc.Graph(
        id="platform-sales-graph",
        figure=px.bar(df_platform_sales, x="Total_Sales", y="Platform", orientation="h",
                      title="Продажи по платформам", color="Platform",
                      labels={"Total_Sales": "Продажи (млн копий)", "Platform": "Платформа"},
                      color_discrete_sequence=px.colors.qualitative.Prism)
    ),

    # График доли издателей
    dcc.Graph(
        id="publisher-sales-graph",
        figure=px.bar(df_publisher_sales, x="Total_Sales", y="Publisher", orientation="h",
                      title="Топ-10 издателей по продажам", color="Publisher",
                      labels={"Total_Sales": "Продажи (млн копий)", "Publisher": "Издатель"},
                      color_discrete_sequence=px.colors.qualitative.Bold)
    ),

    # Линейный график динамики продаж по годам
    dcc.Graph(
        id="yearly-sales-graph",
        figure=px.line(df_yearly_sales, x="Year", y="Total_Sales", markers=True,
                       title="Динамика продаж видеоигр по годам",
                       labels={"Total_Sales": "Продажи (млн копий)", "Year": "Год"},
                       color_discrete_sequence=["#007ACC"])
    ),

    # График топ-10 игр
    dcc.Graph(
        id="top-games-graph",
        figure=px.bar(df_top_games, x="Total_Sales", y="Name", orientation="h",
                      title="Топ-10 продаваемых игр", color="Name",
                      labels={"Total_Sales": "Продажи (млн копий)", "Name": "Игра"},
                      color_discrete_sequence=px.colors.qualitative.Pastel)
    )
])

# Запускаем сервер
if __name__ == "__main__":
    app.run(debug=True)
