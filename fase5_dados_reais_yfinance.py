"""
FASE 5 — DADOS REAIS COM yfinance (integrado no pipeline)
=============================================================
Este módulo obtém variação % e capitalização de mercado REAIS via yfinance,
mantendo o setor/indústria de cada ticker vindos da lista estática da Fase 1
(classificação setorial raramente muda, por isso não vale a pena pedi-la à
API todos os dias — é mais rápido e mais fiável usar o mapa estático).

Requisito: pip install yfinance

Função principal: obter_dados_reais()
  -> devolve uma lista de dicionários no MESMO formato de DADOS_SP500
     (fase1_dados.py), pronta a usar em pd.DataFrame() no fase4.

Comportamento defensivo (importante para correr em CI/CD todos os dias):
  - Se UM ticker falhar (ex: delisted, rate limit pontual), é ignorado
    com um aviso — não trava a geração do resto do mapa.
  - Se a MAIORIA falhar (ex: sem rede, API em baixo), a função levanta
    RuntimeError, e o fase4_versao_final.py apanha esse erro e usa os
    dados de amostra como rede de segurança.
"""

import time
import yfinance as yf

from fase1_dados import DADOS_SP500

# Mapa ticker -> (setor, industria), construído a partir da Fase 1.
# Mantemos a classificação setorial estática; só os números (var%, market cap)
# vêm em tempo real.
MAPA_SETOR_INDUSTRIA = {d["ticker"]: (d["setor"], d["industria"]) for d in DADOS_SP500}
TICKERS_SP500 = list(MAPA_SETOR_INDUSTRIA.keys())


def obter_dados_reais(tickers=None, pausa_entre_pedidos=0.15, minimo_sucesso_pct=0.5):
    """
    Obtém dados reais de mercado para a lista de tickers indicada
    (por omissão, todos os tickers conhecidos da Fase 1).

    tickers               : lista de símbolos a consultar (default: TICKERS_SP500)
    pausa_entre_pedidos   : segundos de espera entre pedidos, para não
                            disparar o rate limiting da Yahoo Finance
    minimo_sucesso_pct    : fração mínima de tickers que tem de ter sucesso
                            (ex: 0.5 = pelo menos 50%) para considerarmos
                            a recolha válida; caso contrário, RuntimeError

    Devolve: lista de dicionários {setor, industria, ticker, var_pct, market_cap}
    """
    tickers = tickers or TICKERS_SP500
    dados = []
    falhas = []

    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).fast_info  # mais rápido que .info

            preco_atual = info["last_price"]
            preco_fecho_anterior = info["previous_close"]
            market_cap = info["market_cap"]

            if not preco_fecho_anterior or not preco_atual:
                raise ValueError("preços em falta")

            var_pct = (preco_atual - preco_fecho_anterior) / preco_fecho_anterior * 100
            setor, industria = MAPA_SETOR_INDUSTRIA.get(ticker, ("Other", "Other"))

            dados.append({
                "setor": setor,
                "industria": industria,
                "ticker": ticker,
                "var_pct": round(var_pct, 2),
                "market_cap": round((market_cap or 0) / 1e9, 1),
            })
        except Exception as erro:
            falhas.append((ticker, str(erro)))

        time.sleep(pausa_entre_pedidos)

    if falhas:
        print(f"  Aviso: {len(falhas)} ticker(s) falharam e foram ignorados: "
              f"{[f[0] for f in falhas]}")

    taxa_sucesso = len(dados) / len(tickers) if tickers else 0
    if taxa_sucesso < minimo_sucesso_pct:
        raise RuntimeError(
            f"Apenas {taxa_sucesso:.0%} dos tickers foram obtidos com sucesso "
            f"(mínimo exigido: {minimo_sucesso_pct:.0%}). Possível rate limit "
            f"ou falha de rede na Yahoo Finance."
        )

    return dados


if __name__ == "__main__":
    print(f"A obter dados reais para {len(TICKERS_SP500)} tickers via yfinance...")
    dados_reais = obter_dados_reais()
    print(f"Obtidos dados para {len(dados_reais)}/{len(TICKERS_SP500)} tickers.")
