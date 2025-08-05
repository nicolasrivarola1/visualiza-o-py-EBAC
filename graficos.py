import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import plotly.figure_factory as ff

# 1. Carregar dados CSV
df = pd.read_csv("ecommerce_estatistica.csv")

# 2. Criar gráficos interativos com Plotly

# Histograma - Distribuição das Notas
fig_hist = px.histogram(
    df, x="Nota", nbins=10, marginal="box",
    title="Distribuição das Notas dos Produtos",
    color_discrete_sequence=["cyan"]
)

# Dispersão - Avaliações x Nota
fig_scatter = px.scatter(
    df, x="N_Avaliações", y="Nota",
    color="Desconto",
    title="Relação entre Número de Avaliações e Nota",
    color_continuous_scale="icefire"
)

# Mapa de Calor - Correlação
corr = df.corr(numeric_only=True)
fig_heatmap = px.imshow(
    corr, text_auto=True, color_continuous_scale="RdBu_r",
    title="Mapa de Calor das Correlações"
)

# Barra - Top 10 Marcas
top_marcas = df["Marca"].value_counts().head(10)
fig_bar = px.bar(
    x=top_marcas.values, y=top_marcas.index, orientation="h",
    title="Top 10 Marcas Mais Frequentes",
    color=top_marcas.values, color_continuous_scale="viridis"
)

# Pizza - Distribuição por Gênero
generos = df["Gênero"].value_counts()
fig_pie = px.pie(
    values=generos.values, names=generos.index,
    title="Distribuição por Gênero", hole=0.3,
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# Densidade - Preço Normalizado
fig_density = ff.create_distplot(
    [df["Preço_MinMax"].dropna()],
    ["Preço Normalizado"],
    colors=["magenta"], show_hist=False
)
fig_density.update_layout(title="Densidade dos Preços Normalizados")

# Regressão - Preço x Nota
fig_reg = px.scatter(
    df, x="Preço_MinMax", y="Nota",
    trendline="ols",
    title="Relação entre Preço Normalizado e Nota",
    color_discrete_sequence=["cyan"]
)
fig_reg.data[1].line.color = "red"


# 3. Criar aplicação Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard - Estatísticas E-commerce", style={"textAlign": "center"}),

    dcc.Graph(figure=fig_hist),
    dcc.Graph(figure=fig_scatter),
    dcc.Graph(figure=fig_heatmap),
    dcc.Graph(figure=fig_bar),
    dcc.Graph(figure=fig_pie),
    dcc.Graph(figure=fig_density),
    dcc.Graph(figure=fig_reg)
])

# 4. Rodar servidor local
if __name__ == "__main__":
    app.run(debug=True)
