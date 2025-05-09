import dash
from dash import dcc, html
import pandas as pd
import sqlite3
import plotly.express as px

# Загружаем данные из SQLite
conn = sqlite3.connect("sales.db")
df_games = pd.read_sql("SELECT * FROM vgsales", conn)
conn.close()

# Преобразуем годы в числовой формат
df_games["Year"] = pd.to_numeric(df_games["Year"], errors="coerce")

# График: Динамика продаж по годам
fig_sales_by_year = px.line(df_games.groupby("Year")["Global_Sales"].sum().reset_index(),
                            x="Year", y="Global_Sales", title="📈 Динамика продаж видеоигр",
                            markers=True, color_discrete_sequence=["red"])

# График: Топ-10 продаваемых игр
fig_top_games = px.bar(df_games.groupby("Name")["Global_Sales"].sum().nlargest(10).reset_index(),
                       x="Global_Sales", y="Name", title="🏆 Топ-10 игр",
                       orientation="h", color="Name", color_discrete_sequence=px.colors.qualitative.Bold)

# График: Продажи по жанрам
fig_genre_sales = px.bar(df_games.groupby("Genre")["Global_Sales"].sum().reset_index(),
                         x="Genre", y="Global_Sales", title="🎮 Продажи по жанрам",
                         color="Genre", color_discrete_sequence=px.colors.qualitative.Set3)

# График: Продажи по платформам
fig_platform_sales = px.bar(df_games.groupby("Platform")["Global_Sales"].sum().reset_index(),
                            x="Platform", y="Global_Sales", title="🕹️ Продажи по платформам",
                            color="Platform", color_discrete_sequence=px.colors.qualitative.Pastel)

# Создаем дашборд
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Аналитика продаж видеоигр", style={"textAlign": "center"}),

    dcc.Graph(figure=fig_sales_by_year),
    dcc.Graph(figure=fig_top_games),
    dcc.Graph(figure=fig_genre_sales),
    dcc.Graph(figure=fig_platform_sales),
])

if __name__ == "__main__":
    app.run(debug=True)
