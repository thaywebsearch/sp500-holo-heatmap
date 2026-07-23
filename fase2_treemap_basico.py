"""
FASE 2 — TREEMAP BÁSICO
=========================
Um "treemap" desenha uma hierarquia como retângulos aninhados:
  setor > indústria > ticker

Conceitos chave do plotly.express.treemap:
  - path=[...]     -> define a hierarquia (do mais geral ao mais específico)
  - values=...      -> define o TAMANHO de cada retângulo
  - color=...       -> define a COR de cada retângulo
  - color_continuous_scale -> a paleta de cores a aplicar sobre "color"

Nesta fase ainda usamos as cores padrão do plotly, só para confirmar que a
estrutura de dados -> gráfico funciona. O visual "holográfico" vem na Fase 3.
"""

import pandas as pd
import plotly.express as px
from fase1_dados import DADOS_SP500

# Converter a lista de dicionários num DataFrame do pandas (tabela)
df = pd.DataFrame(DADOS_SP500)

# path define os níveis do treemap, do mais amplo (setor) ao mais específico (ticker)
fig = px.treemap(
    df,
    path=["setor", "industria", "ticker"],
    values="market_cap",       # tamanho do retângulo = capitalização de mercado
    color="var_pct",           # cor do retângulo = variação % do dia
    color_continuous_scale="RdYlGn",   # escala padrão: vermelho -> amarelo -> verde
    color_continuous_midpoint=0,       # 0% fica no centro da escala de cores
)

fig.update_layout(title="S&P 500 — Fase 2: Treemap básico (sem estilo)")

fig.write_html("/home/claude/sp500_heatmap/fase2_output.html")
print("Gráfico da Fase 2 guardado em fase2_output.html")
