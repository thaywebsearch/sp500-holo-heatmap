"""
FASE 1 — ESTRUTURA DE DADOS
============================
Antes de desenhar qualquer gráfico, precisamos de dados organizados.

No finviz, cada retângulo do mapa representa uma AÇÃO, agrupada por
INDÚSTRIA, agrupada por SETOR. O TAMANHO do retângulo normalmente reflete
a capitalização de mercado (market cap) e a COR reflete a variação % do dia.

Aqui usamos uma lista de dicionários — cada dicionário é uma linha de dados,
tal como uma linha numa folha de cálculo. Isto é dados de amostra (não em
tempo real); na Fase 5 mostramos como ligar a dados reais.
"""

# Cada entrada: setor, indústria, ticker, variação % no dia, market cap (em mil milhões USD)
DADOS_SP500 = [
    # --- TECHNOLOGY ---
    {"setor": "Technology", "industria": "Semiconductors", "ticker": "NVDA", "var_pct": 1.47, "market_cap": 3300},
    {"setor": "Technology", "industria": "Semiconductors", "ticker": "AVGO", "var_pct": 2.02, "market_cap": 900},
    {"setor": "Technology", "industria": "Semiconductors", "ticker": "MU", "var_pct": 12.09, "market_cap": 150},
    {"setor": "Technology", "industria": "Semiconductors", "ticker": "AMD", "var_pct": 7.68, "market_cap": 260},
    {"setor": "Technology", "industria": "Semiconductors", "ticker": "INTC", "var_pct": 8.24, "market_cap": 110},
    {"setor": "Technology", "industria": "Semiconductors", "ticker": "TXN", "var_pct": -1.10, "market_cap": 170},
    {"setor": "Technology", "industria": "Semiconductors", "ticker": "AMAT", "var_pct": 7.60, "market_cap": 145},
    {"setor": "Technology", "industria": "Semiconductors", "ticker": "LRCX", "var_pct": 4.32, "market_cap": 110},
    {"setor": "Technology", "industria": "Semiconductors", "ticker": "KLAC", "var_pct": -0.20, "market_cap": 105},
    {"setor": "Technology", "industria": "Semiconductors", "ticker": "MRVL", "var_pct": 6.72, "market_cap": 95},
    {"setor": "Technology", "industria": "Consumer Electronics", "ticker": "AAPL", "var_pct": 0.25, "market_cap": 3400},
    {"setor": "Technology", "industria": "Consumer Electronics", "ticker": "DELL", "var_pct": 5.69, "market_cap": 90},
    {"setor": "Technology", "industria": "Software - Infrastructure", "ticker": "MSFT", "var_pct": -0.92, "market_cap": 3200},
    {"setor": "Technology", "industria": "Software - Infrastructure", "ticker": "ORCL", "var_pct": 4.55, "market_cap": 500},
    {"setor": "Technology", "industria": "Software - Infrastructure", "ticker": "PANW", "var_pct": -2.70, "market_cap": 110},
    {"setor": "Technology", "industria": "Software - Infrastructure", "ticker": "CRWD", "var_pct": -3.85, "market_cap": 85},
    {"setor": "Technology", "industria": "Software - Application", "ticker": "PLTR", "var_pct": -0.84, "market_cap": 350},
    {"setor": "Technology", "industria": "Software - Application", "ticker": "CRM", "var_pct": -1.97, "market_cap": 250},
    {"setor": "Technology", "industria": "Software - Application", "ticker": "IBM", "var_pct": -0.73, "market_cap": 260},
    {"setor": "Technology", "industria": "Communication Equipment", "ticker": "CSCO", "var_pct": 0.51, "market_cap": 260},
    {"setor": "Technology", "industria": "Communication Equipment", "ticker": "GLW", "var_pct": 5.97, "market_cap": 55},

    # --- CONSUMER CYCLICAL ---
    {"setor": "Consumer Cyclical", "industria": "Internet Retail", "ticker": "AMZN", "var_pct": -0.87, "market_cap": 2100},
    {"setor": "Consumer Cyclical", "industria": "Auto Manufacturers", "ticker": "TSLA", "var_pct": 2.82, "market_cap": 950},
    {"setor": "Consumer Cyclical", "industria": "Home Improvement", "ticker": "HD", "var_pct": -0.94, "market_cap": 350},
    {"setor": "Consumer Cyclical", "industria": "Apparel Retail", "ticker": "TJX", "var_pct": -0.55, "market_cap": 140},
    {"setor": "Consumer Cyclical", "industria": "Restaurants", "ticker": "MCD", "var_pct": -0.23, "market_cap": 210},
    {"setor": "Consumer Cyclical", "industria": "Restaurants", "ticker": "SBUX", "var_pct": -0.23, "market_cap": 95},

    # --- HEALTHCARE ---
    {"setor": "Healthcare", "industria": "Drug Manufacturers", "ticker": "LLY", "var_pct": 1.49, "market_cap": 800},
    {"setor": "Healthcare", "industria": "Drug Manufacturers", "ticker": "JNJ", "var_pct": 0.22, "market_cap": 400},
    {"setor": "Healthcare", "industria": "Drug Manufacturers", "ticker": "ABBV", "var_pct": 0.74, "market_cap": 340},
    {"setor": "Healthcare", "industria": "Drug Manufacturers", "ticker": "MRK", "var_pct": 0.40, "market_cap": 260},
    {"setor": "Healthcare", "industria": "Healthcare Plans", "ticker": "UNH", "var_pct": 2.93, "market_cap": 300},
    {"setor": "Healthcare", "industria": "Diagnostics & Research", "ticker": "TMO", "var_pct": -1.02, "market_cap": 180},
    {"setor": "Healthcare", "industria": "Diagnostics & Research", "ticker": "DHR", "var_pct": -1.10, "market_cap": 150},
    {"setor": "Healthcare", "industria": "Medical Instruments", "ticker": "ISRG", "var_pct": -0.96, "market_cap": 170},
    {"setor": "Healthcare", "industria": "Medical Care", "ticker": "CVS", "var_pct": 1.70, "market_cap": 90},
    {"setor": "Healthcare", "industria": "Medical Care", "ticker": "ELV", "var_pct": -0.60, "market_cap": 95},

    # --- COMMUNICATION SERVICES ---
    {"setor": "Communication Services", "industria": "Internet Content & Info", "ticker": "GOOGL", "var_pct": -0.99, "market_cap": 2200},
    {"setor": "Communication Services", "industria": "Internet Content & Info", "ticker": "META", "var_pct": 0.24, "market_cap": 1400},
    {"setor": "Communication Services", "industria": "Entertainment", "ticker": "NFLX", "var_pct": 0.17, "market_cap": 380},
    {"setor": "Communication Services", "industria": "Entertainment", "ticker": "DIS", "var_pct": 0.18, "market_cap": 210},
    {"setor": "Communication Services", "industria": "Telecom Services", "ticker": "VZ", "var_pct": -0.42, "market_cap": 175},
    {"setor": "Communication Services", "industria": "Telecom Services", "ticker": "APP", "var_pct": -1.40, "market_cap": 130},

    # --- INDUSTRIALS ---
    {"setor": "Industrials", "industria": "Specialty Industrial Machinery", "ticker": "GE", "var_pct": 0.14, "market_cap": 260},
    {"setor": "Industrials", "industria": "Aerospace & Defense", "ticker": "RTX", "var_pct": 0.65, "market_cap": 190},
    {"setor": "Industrials", "industria": "Farm & Heavy Machinery", "ticker": "CAT", "var_pct": 2.94, "market_cap": 220},
    {"setor": "Industrials", "industria": "Conglomerates", "ticker": "HON", "var_pct": -0.30, "market_cap": 140},
    {"setor": "Industrials", "industria": "Railroads", "ticker": "UNP", "var_pct": 0.51, "market_cap": 145},
    {"setor": "Industrials", "industria": "Aerospace & Defense", "ticker": "BA", "var_pct": -0.90, "market_cap": 110},

    # --- CONSUMER DEFENSIVE ---
    {"setor": "Consumer Defensive", "industria": "Discount Stores", "ticker": "WMT", "var_pct": -1.46, "market_cap": 780},
    {"setor": "Consumer Defensive", "industria": "Beverages", "ticker": "KO", "var_pct": -0.03, "market_cap": 300},
    {"setor": "Consumer Defensive", "industria": "Beverages", "ticker": "PEP", "var_pct": -0.46, "market_cap": 200},
    {"setor": "Consumer Defensive", "industria": "Discount Stores", "ticker": "COST", "var_pct": -0.56, "market_cap": 440},
    {"setor": "Consumer Defensive", "industria": "Household Products", "ticker": "PG", "var_pct": -0.98, "market_cap": 380},
    {"setor": "Consumer Defensive", "industria": "Tobacco", "ticker": "PM", "var_pct": -0.20, "market_cap": 260},

    # --- FINANCIAL ---
    {"setor": "Financial", "industria": "Banks - Diversified", "ticker": "JPM", "var_pct": 1.80, "market_cap": 780},
    {"setor": "Financial", "industria": "Credit Services", "ticker": "V", "var_pct": 1.42, "market_cap": 620},
    {"setor": "Financial", "industria": "Credit Services", "ticker": "MA", "var_pct": -1.52, "market_cap": 480},
    {"setor": "Financial", "industria": "Insurance - Diversified", "ticker": "BRK-B", "var_pct": -0.31, "market_cap": 970},
    {"setor": "Financial", "industria": "Capital Markets", "ticker": "GS", "var_pct": -0.80, "market_cap": 200},
    {"setor": "Financial", "industria": "Capital Markets", "ticker": "MS", "var_pct": -0.65, "market_cap": 210},
    {"setor": "Financial", "industria": "Banks - Diversified", "ticker": "WFC", "var_pct": 1.85, "market_cap": 260},
    {"setor": "Financial", "industria": "Banks - Diversified", "ticker": "C", "var_pct": 2.10, "market_cap": 160},

    # --- ENERGY ---
    {"setor": "Energy", "industria": "Oil & Gas Integrated", "ticker": "XOM", "var_pct": 1.82, "market_cap": 520},
    {"setor": "Energy", "industria": "Oil & Gas Integrated", "ticker": "CVX", "var_pct": 0.90, "market_cap": 290},
    {"setor": "Energy", "industria": "Oil & Gas E&P", "ticker": "COP", "var_pct": -0.20, "market_cap": 130},
    {"setor": "Energy", "industria": "Oil & Gas Equipment", "ticker": "SLB", "var_pct": -1.10, "market_cap": 55},

    # --- UTILITIES ---
    {"setor": "Utilities", "industria": "Utilities - Regulated Electric", "ticker": "NEE", "var_pct": -0.15, "market_cap": 150},
    {"setor": "Utilities", "industria": "Utilities - Regulated Electric", "ticker": "SO", "var_pct": -0.40, "market_cap": 100},
    {"setor": "Utilities", "industria": "Utilities - Regulated Electric", "ticker": "CEG", "var_pct": -1.85, "market_cap": 90},

    # --- REAL ESTATE ---
    {"setor": "Real Estate", "industria": "REIT - Industrial", "ticker": "PLD", "var_pct": -1.09, "market_cap": 100},
    {"setor": "Real Estate", "industria": "REIT - Specialty", "ticker": "AMT", "var_pct": 0.30, "market_cap": 95},

    # --- BASIC MATERIALS ---
    {"setor": "Basic Materials", "industria": "Specialty Chemicals", "ticker": "LIN", "var_pct": -0.10, "market_cap": 220},
    {"setor": "Basic Materials", "industria": "Specialty Chemicals", "ticker": "APD", "var_pct": 0.55, "market_cap": 75},
]

if __name__ == "__main__":
    print(f"Total de ações no dataset: {len(DADOS_SP500)}")
    setores = sorted(set(d["setor"] for d in DADOS_SP500))
    print(f"Setores ({len(setores)}): {setores}")
