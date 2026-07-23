"""
FASE 3 — ESTILO HOLOGRÁFICO
=============================
Aqui trocamos a paleta padrão (vermelho/verde tradicional) por uma escala
"holográfica": magenta/roxo profundo para quedas fortes, passando por um
roxo escuro neutro perto de 0%, até ciano/verde-elétrico para subidas fortes.

Conceitos novos:
  - color_continuous_scale pode ser uma LISTA de cores em vez de um nome
    (cada cor corresponde a um ponto de 0.0 a 1.0 na escala)
  - fig.update_layout(paper_bgcolor=..., plot_bgcolor=...) pinta o fundo
  - marker=dict(line=dict(...)) desenha contornos brilhantes em cada retângulo
"""

import pandas as pd
import plotly.express as px
from fase1_dados import DADOS_SP500

df = pd.DataFrame(DADOS_SP500)

# Escala holográfica: de magenta escuro (queda forte) -> roxo profundo (neutro) -> ciano (subida forte)
ESCALA_HOLOGRAFICA = [
    [0.0, "#ff00c8"],   # queda forte -> magenta vibrante
    [0.35, "#8a1a6b"],  # queda leve -> roxo/magenta escuro
    [0.5, "#150826"],   # ~0% -> roxo quase preto (funde com o fundo)
    [0.65, "#0a5f6b"],  # subida leve -> ciano escuro
    [1.0, "#00f0ff"],   # subida forte -> ciano elétrico
]

fig = px.treemap(
    df,
    path=["setor", "industria", "ticker"],
    values="market_cap",
    color="var_pct",
    color_continuous_scale=ESCALA_HOLOGRAFICA,
    color_continuous_midpoint=0,
    range_color=[-4, 4],   # satura a cor a partir de +-4% para dar mais contraste
)

fig.update_layout(
    title=dict(
        text="S&P 500 — Fase 3: Fundo preto + paleta holográfica",
        font=dict(color="#00f0ff"),
    ),
    paper_bgcolor="#000000",   # fundo geral da figura
    plot_bgcolor="#000000",    # fundo da área do gráfico
    font=dict(color="#e0e0e0"),
)

# Contorno brilhante em cada retângulo, para reforçar o efeito "holograma"
fig.update_traces(
    marker=dict(line=dict(color="#00f0ff", width=1)),
)

fig.write_html("/home/claude/sp500_heatmap/fase3_output.html")
print("Gráfico da Fase 3 guardado em fase3_output.html")
