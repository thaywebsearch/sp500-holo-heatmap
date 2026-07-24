"""
FASE 4 — VERSÃO FINAL POLIDA
==============================
Últimos retoques que fazem a diferença entre "gráfico" e "produto":
  - texttemplate      -> controla o que aparece DENTRO de cada retângulo
  - hovertemplate     -> controla o que aparece ao passar o rato por cima
  - fonte customizada -> importada via Google Fonts dentro do HTML exportado
  - watermark/subtítulo com timestamp

Conceito novo: fig.write_html() aceita um parâmetro `full_html=True/False` e
podemos ainda injetar CSS/HTML extra à volta do gráfico exportado para
adicionar uma fonte tipo "monoespaçada futurista" (ex: Orbitron).
"""

import pandas as pd
import plotly.express as px
from datetime import datetime
from fase1_dados import DADOS_SP500

df = pd.DataFrame(DADOS_SP500)

ESCALA_HOLOGRAFICA = [
    [0.0, "#ff00c8"],
    [0.35, "#8a1a6b"],
    [0.5, "#150826"],
    [0.65, "#0a5f6b"],
    [1.0, "#00f0ff"],
]

fig = px.treemap(
    df,
    path=["setor", "industria", "ticker"],
    values="market_cap",
    color="var_pct",
    color_continuous_scale=ESCALA_HOLOGRAFICA,
    color_continuous_midpoint=0,
    range_color=[-4, 4],
    custom_data=["var_pct", "market_cap"],
)

# texttemplate: o que se vê ESCRITO dentro do retângulo (ticker + variação %)
fig.update_traces(
    texttemplate="<b>%{label}</b><br>%{customdata[0]:+.2f}%",
    textfont=dict(size=14, family="Orbitron, monospace", color="#f5f5f5"),
    hovertemplate=(
        "<b>%{label}</b><br>"
        "Variação: %{customdata[0]:+.2f}%<br>"
        "Market cap: $%{customdata[1]:,.0f} mM<extra></extra>"
    ),
    marker=dict(
        line=dict(color="#00f0ff", width=1.2),
        pad=dict(t=3, l=3, r=3, b=3),
    ),
    root_color="#000000",
)

fig.update_layout(
    title=dict(
        text=f"S&P 500 — PERFORMANCE HOLOGRÁFICA<br>"
             f"<span style='font-size:12px;color:#888'>Gerado em "
             f"{datetime.now().strftime('%d/%m/%Y %H:%M')} · dados de amostra</span>",
        font=dict(color="#00f0ff", family="Orbitron, sans-serif", size=24),
        x=0.01,
    ),
    paper_bgcolor="#000000",
    plot_bgcolor="#000000",
    font=dict(color="#e0e0e0", family="Orbitron, sans-serif"),
    coloraxis_colorbar=dict(
        title=dict(text="Variação %", font=dict(color="#e0e0e0")),
        tickfont=dict(color="#e0e0e0"),
    ),
    margin=dict(t=90, l=10, r=10, b=10),
)

# Exportamos só a "div" do gráfico (full_html=False) para poder envolvê-la
# em HTML próprio com a fonte holográfica importada do Google Fonts.
grafico_html = fig.to_html(full_html=False, include_plotlyjs="cdn")

pagina_final = f"""
<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<title>S&P 500 — Mapa Holográfico</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
<style>
  body {{
    background: #000000;
    margin: 0;
    padding: 20px;
    font-family: 'Orbitron', sans-serif;
  }}
  .glow-border {{
    border: 1px solid #00f0ff44;
    box-shadow: 0 0 25px #00f0ff33, inset 0 0 25px #ff00c822;
    border-radius: 12px;
    padding: 10px;
  }}
</style>
</head>
<body>
  <div class="glow-border">
    {grafico_html}
  </div>
</body>
</html>
"""

import os

# Caminho relativo: cria a pasta 'dist' junto deste script e guarda lá o HTML.
# Isto funciona tanto localmente como em CI/CD (ex: GitHub Actions).
pasta_saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
os.makedirs(pasta_saida, exist_ok=True)
caminho_saida = os.path.join(pasta_saida, "index.html")

with open(caminho_saida, "w", encoding="utf-8") as f:
    f.write(pagina_final)

print(f"Gráfico da Fase 4 (versão final) guardado em {caminho_saida}")
