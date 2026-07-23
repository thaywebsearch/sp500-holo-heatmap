"""
FASE 5 (BÓNUS) — DADOS REAIS COM yfinance
============================================
Este script NÃO corre no ambiente onde construímos o projeto (aqui não há
acesso à Yahoo Finance), mas corre perfeitamente no teu computador.

Passos para usar dados reais em vez dos dados de amostra da Fase 1:

    pip install yfinance

E depois substitui, no teu ficheiro principal, DADOS_SP500 pelo resultado
da função obter_dados_reais() abaixo.

Nota: puxar os ~500 tickers do S&P 500 um a um é lento (pode demorar
alguns minutos) por causa dos limites da API gratuita do Yahoo Finance.
Para testar rápido, começa com uma lista pequena de tickers.
"""

import yfinance as yf


# Mapa manual: setor/indústria "estilo finviz" para cada ticker.
# yfinance devolve 'sector' e 'industry' em inglês, tal como aqui.
TICKERS_EXEMPLO = ["NVDA", "AAPL", "MSFT", "AMZN", "TSLA", "GOOGL", "META", "JPM"]


def obter_dados_reais(tickers=TICKERS_EXEMPLO):
    """
    Para cada ticker, obtém:
      - setor e indústria (via .info)
      - variação % do dia (via histórico de 2 dias)
      - capitalização de mercado (via .info)

    Devolve uma lista de dicionários no MESMO formato da Fase 1,
    para que o resto do pipeline (Fases 2-4) funcione sem alterações.
    """
    dados = []
    for ticker in tickers:
        acao = yf.Ticker(ticker)
        info = acao.info

        # histórico dos últimos 2 dias para calcular variação %
        hist = acao.history(period="2d")
        if len(hist) >= 2:
            fecho_ontem = hist["Close"].iloc[-2]
            fecho_hoje = hist["Close"].iloc[-1]
            var_pct = (fecho_hoje - fecho_ontem) / fecho_ontem * 100
        else:
            var_pct = 0.0

        dados.append({
            "setor": info.get("sector", "Other"),
            "industria": info.get("industry", "Other"),
            "ticker": ticker,
            "var_pct": round(var_pct, 2),
            # market_cap vem em dólares; convertemos para mil milhões (bilhões)
            "market_cap": round(info.get("marketCap", 0) / 1e9, 1),
        })
        print(f"  {ticker}: {dados[-1]}")

    return dados


if __name__ == "__main__":
    print("A obter dados reais via yfinance (pode demorar alguns segundos)...")
    dados_reais = obter_dados_reais()
    print(f"\nObtidos dados para {len(dados_reais)} tickers.")
    print("Substitui DADOS_SP500 nas Fases 2-4 por esta lista para usar dados reais.")
