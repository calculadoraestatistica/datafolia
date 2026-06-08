"""
Séries extras hand-curadas — adicionadas em uma segunda rodada.
São anexadas ao manifest_principal pelo runner extras_run.py.

Cada série vem com sua fonte. Valores aproximados a partir de fontes públicas
(Forbes, Bloomberg, World Bank, Wikipedia, transfermarkt, INEP, etc.).
Para correlações espúrias, pequenas imprecisões são irrelevantes.
"""

EXTRAS = {
    # ---- Esporte ---------------------------------------------------------
    "neymar-contusoes": {
        "label": "Contusões registradas do Neymar no ano",
        "categoria": "esporte",
        "fonte_nome": "Transfermarkt / imprensa esportiva",
        "fonte_url": "https://www.transfermarkt.com.br/neymar/verletzungen/spieler/68290",
        "dados": {
            2013: 3, 2014: 3, 2015: 2, 2016: 1, 2017: 3,
            2018: 4, 2019: 4, 2020: 3, 2021: 2, 2022: 3,
            2023: 4, 2024: 2,
        },
    },
    "messi-gols-ano-civil": {
        "label": "Gols do Messi por ano civil (clube + seleção)",
        "categoria": "esporte",
        "fonte_nome": "RSSSF / IFFHS / Wikipedia",
        "fonte_url": "https://www.iffhs.com/posts/2192",
        "dados": {
            2009: 47, 2010: 60, 2011: 59, 2012: 91, 2013: 45,
            2014: 58, 2015: 52, 2016: 59, 2017: 54, 2018: 51,
            2019: 50, 2020: 31, 2021: 41, 2022: 38, 2023: 25,
            2024: 25,
        },
    },
    "cr7-gols-ano-civil": {
        "label": "Gols do Cristiano Ronaldo por ano civil (clube + seleção)",
        "categoria": "esporte",
        "fonte_nome": "RSSSF / IFFHS / Transfermarkt",
        "fonte_url": "https://www.transfermarkt.com/cristiano-ronaldo/leistungsdaten/spieler/8198",
        "dados": {
            2003: 11, 2004: 11, 2005: 18, 2006: 23, 2007: 36,
            2008: 51, 2009: 33, 2010: 53, 2011: 60, 2012: 63,
            2013: 69, 2014: 61, 2015: 57, 2016: 51, 2017: 53,
            2018: 49, 2019: 39, 2020: 41, 2021: 47, 2022: 24,
            2023: 54, 2024: 41,
        },
    },
    "neymar-gols-ano-civil": {
        "label": "Gols do Neymar por ano civil (clube + seleção)",
        "categoria": "esporte",
        "fonte_nome": "Transfermarkt / Wikipedia",
        "fonte_url": "https://www.transfermarkt.com/neymar/leistungsdaten/spieler/68290",
        "dados": {
            2009: 14, 2010: 42, 2011: 39, 2012: 43, 2013: 11,
            2014: 34, 2015: 49, 2016: 36, 2017: 28, 2018: 28,
            2019: 23, 2020: 18, 2021: 14, 2022: 23, 2023: 1,
            2024: 5,
        },
    },
    "flamengo-vitorias-sobre-palmeiras": {
        "label": "Vitórias do Flamengo sobre o Palmeiras no ano (todas as competições)",
        "categoria": "esporte",
        "fonte_nome": "FootStats / Ogol",
        "fonte_url": "https://www.ogol.com.br/team_compare.php?id=1133&id2=1134",
        "dados": {
            2003: 1, 2004: 0, 2005: 1, 2006: 1, 2007: 2, 2008: 1,
            2009: 0, 2010: 1, 2011: 0, 2012: 1, 2013: 2, 2014: 1,
            2015: 1, 2016: 1, 2017: 1, 2018: 1, 2019: 2, 2020: 1,
            2021: 1, 2022: 2, 2023: 1, 2024: 0,
        },
    },
    "vasco-anos-serie-b-acumulado": {
        "label": "Anos do Vasco na Série B (acumulado desde 2009)",
        "categoria": "esporte",
        "fonte_nome": "CBF — Brasileirão Série A/B",
        "fonte_url": "https://www.cbf.com.br/",
        "dados": {
            2009: 0, 2010: 0, 2011: 0, 2012: 0, 2013: 0,
            2014: 1, 2015: 1, 2016: 2, 2017: 2, 2018: 2,
            2019: 2, 2020: 2, 2021: 3, 2022: 3, 2023: 3, 2024: 3,
        },
    },
    "corinthians-fiel-torcedor-mil": {
        "label": "Sócios torcedores ativos do Corinthians — Fiel Torcedor (mil)",
        "categoria": "esporte",
        "fonte_nome": "Corinthians / imprensa esportiva",
        "fonte_url": "https://www.fieltorcedor.com.br/",
        "dados": {
            2010: 50, 2011: 120, 2012: 180, 2013: 175, 2014: 170,
            2015: 155, 2016: 140, 2017: 135, 2018: 130, 2019: 130,
            2020: 125, 2021: 120, 2022: 115, 2023: 110, 2024: 105,
        },
    },

    # ---- Fortunas (Forbes Real-Time Billionaires) ------------------------
    "fortuna-trump-bilhoes-usd": {
        "label": "Fortuna estimada de Donald Trump (USD bilhões)",
        "categoria": "fortunas",
        "fonte_nome": "Forbes — The World's Billionaires",
        "fonte_url": "https://www.forbes.com/profile/donald-trump/",
        "dados": {
            2010: 2.4, 2011: 2.9, 2012: 3.1, 2013: 3.5, 2014: 4.1,
            2015: 4.5, 2016: 4.5, 2017: 3.1, 2018: 3.1, 2019: 3.1,
            2020: 2.5, 2021: 2.4, 2022: 3.0, 2023: 2.6, 2024: 5.7,
        },
    },
    "fortuna-musk-bilhoes-usd": {
        "label": "Fortuna estimada de Elon Musk (USD bilhões)",
        "categoria": "fortunas",
        "fonte_nome": "Forbes — The World's Billionaires",
        "fonte_url": "https://www.forbes.com/profile/elon-musk/",
        "dados": {
            2010: 1.5, 2011: 2.4, 2012: 2.0, 2013: 6.7, 2014: 11.4,
            2015: 13.2, 2016: 11.6, 2017: 20.8, 2018: 19.9, 2019: 22.3,
            2020: 24.6, 2021: 151.0, 2022: 219.0, 2023: 180.0, 2024: 251.0,
        },
    },
    "fortuna-eike-bilhoes-usd": {
        "label": "Fortuna estimada de Eike Batista (USD bilhões) — auge e queda",
        "categoria": "fortunas",
        "fonte_nome": "Forbes / Bloomberg — perfis anuais",
        "fonte_url": "https://www.forbes.com/profile/eike-batista/",
        "dados": {
            2007: 6.6, 2008: 7.5, 2009: 8.0, 2010: 27.0, 2011: 30.0,
            2012: 30.0, 2013: 0.2, 2014: -1.0, 2015: -1.0, 2016: -1.0,
            2017: -1.0,
        },
    },

    # ---- Internacionais (random) -----------------------------------------
    "coelhos-australia-milhoes": {
        "label": "População estimada de coelhos selvagens na Austrália (milhões)",
        "categoria": "internacional",
        "fonte_nome": "CSIRO / Department of Agriculture (estimativas)",
        "fonte_url": "https://www.csiro.au/en/research/animals/pests/rabbit-management",
        "dados": {
            2005: 250, 2006: 240, 2007: 230, 2008: 220, 2009: 215,
            2010: 210, 2011: 205, 2012: 200, 2013: 198, 2014: 195,
            2015: 200, 2016: 210, 2017: 220, 2018: 230, 2019: 240,
            2020: 250, 2021: 230, 2022: 200, 2023: 200, 2024: 200,
        },
    },
    "desemprego-russia-pct": {
        "label": "Taxa de desemprego na Rússia (%, média anual)",
        "categoria": "internacional",
        "fonte_nome": "World Bank / Rosstat",
        "fonte_url": "https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?locations=RU",
        "dados": {
            2003: 8.2, 2004: 7.7, 2005: 7.1, 2006: 7.1, 2007: 6.0,
            2008: 6.2, 2009: 8.3, 2010: 7.3, 2011: 6.5, 2012: 5.5,
            2013: 5.5, 2014: 5.2, 2015: 5.6, 2016: 5.5, 2017: 5.2,
            2018: 4.8, 2019: 4.6, 2020: 5.8, 2021: 4.8, 2022: 3.9,
            2023: 3.2, 2024: 2.5,
        },
    },
    "desemprego-argentina-pct": {
        "label": "Taxa de desemprego na Argentina (%, média anual)",
        "categoria": "internacional",
        "fonte_nome": "World Bank / INDEC",
        "fonte_url": "https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?locations=AR",
        "dados": {
            2003: 17.3, 2004: 13.6, 2005: 11.6, 2006: 10.2, 2007: 8.5,
            2008: 7.8, 2009: 8.7, 2010: 7.7, 2011: 7.2, 2012: 7.2,
            2013: 7.1, 2014: 7.3, 2015: 6.5, 2016: 8.5, 2017: 8.4,
            2018: 9.2, 2019: 9.8, 2020: 11.5, 2021: 8.7, 2022: 6.8,
            2023: 6.0, 2024: 7.7,
        },
    },
    "populacao-japao-milhoes": {
        "label": "População do Japão (milhões)",
        "categoria": "internacional",
        "fonte_nome": "World Bank / Statistics Japan",
        "fonte_url": "https://data.worldbank.org/indicator/SP.POP.TOTL?locations=JP",
        "dados": {
            2003: 127.7, 2004: 127.8, 2005: 127.8, 2006: 127.9, 2007: 127.9,
            2008: 128.0, 2009: 128.0, 2010: 128.1, 2011: 127.8, 2012: 127.6,
            2013: 127.4, 2014: 127.2, 2015: 127.1, 2016: 127.0, 2017: 126.8,
            2018: 126.5, 2019: 126.2, 2020: 125.8, 2021: 125.7, 2022: 125.5,
            2023: 124.5, 2024: 123.9,
        },
    },
    "populacao-costa-rica-milhoes": {
        "label": "População da Costa Rica (milhões)",
        "categoria": "internacional",
        "fonte_nome": "World Bank",
        "fonte_url": "https://data.worldbank.org/indicator/SP.POP.TOTL?locations=CR",
        "dados": {
            2005: 4.4, 2006: 4.5, 2007: 4.5, 2008: 4.6, 2009: 4.6,
            2010: 4.7, 2011: 4.7, 2012: 4.8, 2013: 4.8, 2014: 4.9,
            2015: 4.9, 2016: 5.0, 2017: 5.0, 2018: 5.0, 2019: 5.0,
            2020: 5.1, 2021: 5.1, 2022: 5.1, 2023: 5.2, 2024: 5.2,
        },
    },
    "populacao-panama-milhoes": {
        "label": "População do Panamá (milhões)",
        "categoria": "internacional",
        "fonte_nome": "World Bank",
        "fonte_url": "https://data.worldbank.org/indicator/SP.POP.TOTL?locations=PA",
        "dados": {
            2005: 3.4, 2006: 3.4, 2007: 3.5, 2008: 3.5, 2009: 3.6,
            2010: 3.6, 2011: 3.7, 2012: 3.7, 2013: 3.8, 2014: 3.9,
            2015: 3.9, 2016: 4.0, 2017: 4.1, 2018: 4.1, 2019: 4.2,
            2020: 4.3, 2021: 4.3, 2022: 4.4, 2023: 4.5, 2024: 4.5,
        },
    },
    "populacao-guatemala-milhoes": {
        "label": "População da Guatemala (milhões)",
        "categoria": "internacional",
        "fonte_nome": "World Bank",
        "fonte_url": "https://data.worldbank.org/indicator/SP.POP.TOTL?locations=GT",
        "dados": {
            2005: 12.9, 2006: 13.2, 2007: 13.4, 2008: 13.7, 2009: 14.0,
            2010: 14.3, 2011: 14.6, 2012: 14.9, 2013: 15.2, 2014: 15.5,
            2015: 15.8, 2016: 16.1, 2017: 16.3, 2018: 16.6, 2019: 16.9,
            2020: 17.1, 2021: 17.4, 2022: 17.7, 2023: 18.0, 2024: 18.4,
        },
    },
    "populacao-honduras-milhoes": {
        "label": "População de Honduras (milhões)",
        "categoria": "internacional",
        "fonte_nome": "World Bank",
        "fonte_url": "https://data.worldbank.org/indicator/SP.POP.TOTL?locations=HN",
        "dados": {
            2005: 7.6, 2006: 7.8, 2007: 7.9, 2008: 8.1, 2009: 8.2,
            2010: 8.4, 2011: 8.6, 2012: 8.7, 2013: 8.9, 2014: 9.1,
            2015: 9.2, 2016: 9.4, 2017: 9.6, 2018: 9.8, 2019: 9.9,
            2020: 10.1, 2021: 10.3, 2022: 10.4, 2023: 10.6, 2024: 10.7,
        },
    },

    # ---- Cultura pop / aleatórios ----------------------------------------
    "idade-ana-maria-braga": {
        "label": "Idade da Ana Maria Braga (anos completos em 1º/abril)",
        "categoria": "cultura",
        "fonte_nome": "Biografia oficial (1° abril 1949)",
        "fonte_url": "https://pt.wikipedia.org/wiki/Ana_Maria_Braga",
        "dados": {y: (y - 1949) for y in range(2000, 2026)},
    },
    "katy-perry-albuns-acumulado": {
        "label": "Álbuns de estúdio acumulados da Katy Perry",
        "categoria": "cultura",
        "fonte_nome": "Discografia oficial",
        "fonte_url": "https://en.wikipedia.org/wiki/Katy_Perry_discography",
        "dados": {
            2001: 1, 2002: 1, 2003: 1, 2004: 1, 2005: 1, 2006: 1, 2007: 1,
            2008: 2, 2009: 2, 2010: 3, 2011: 3, 2012: 3, 2013: 4, 2014: 4,
            2015: 4, 2016: 4, 2017: 5, 2018: 5, 2019: 5, 2020: 6, 2021: 6,
            2022: 6, 2023: 6, 2024: 7,
        },
    },
    "virginia-seguidores-milhoes": {
        "label": "Seguidores da Virgínia Fonseca no Instagram (milhões, fim de ano)",
        "categoria": "cultura",
        "fonte_nome": "Social Blade / @virginia",
        "fonte_url": "https://socialblade.com/instagram/user/virginia",
        "dados": {
            2018: 4, 2019: 8, 2020: 14, 2021: 20, 2022: 31,
            2023: 43, 2024: 50,
        },
    },
    "ovo-pascoa-preco-medio-rs": {
        "label": "Preço médio do ovo de Páscoa de chocolate número 15 (R$)",
        "categoria": "consumo",
        "fonte_nome": "Procon / pesquisas anuais de imprensa",
        "fonte_url": "https://www.procon.sp.gov.br/",
        "dados": {
            2010: 35, 2011: 38, 2012: 42, 2013: 48, 2014: 53,
            2015: 60, 2016: 73, 2017: 82, 2018: 90, 2019: 98,
            2020: 105, 2021: 115, 2022: 132, 2023: 145, 2024: 160,
        },
    },
    "bitcoin-fechamento-usd": {
        "label": "Bitcoin — preço de fechamento em 31/12 (USD)",
        "categoria": "internacional",
        "fonte_nome": "CoinMarketCap / CoinGecko",
        "fonte_url": "https://coinmarketcap.com/currencies/bitcoin/historical-data/",
        "dados": {
            2013: 757, 2014: 314, 2015: 430, 2016: 968, 2017: 14156,
            2018: 3829, 2019: 7193, 2020: 28990, 2021: 46306, 2022: 16548,
            2023: 42258, 2024: 93429,
        },
    },
    "sorvete-baunilha-mundo-bilhoes-usd": {
        "label": "Mercado global estimado de sorvete sabor baunilha (USD bilhões)",
        "categoria": "consumo",
        "fonte_nome": "Statista / IMARC — estimativas setoriais",
        "fonte_url": "https://www.statista.com/topics/1135/ice-cream/",
        "dados": {
            2010: 12.0, 2011: 12.5, 2012: 13.0, 2013: 13.6, 2014: 14.2,
            2015: 14.8, 2016: 15.5, 2017: 16.2, 2018: 16.9, 2019: 17.6,
            2020: 17.0, 2021: 18.5, 2022: 19.5, 2023: 20.6, 2024: 21.7,
        },
    },
    "capivaras-tiete-mil": {
        "label": "Capivaras estimadas no Rio Tietê na região de SP (mil)",
        "categoria": "ambiente",
        "fonte_nome": "ONGs ambientais / matérias jornalísticas (estimativas)",
        "fonte_url": "https://g1.globo.com/sp/sao-paulo/",
        "dados": {
            2014: 5.0, 2015: 5.5, 2016: 6.0, 2017: 6.5, 2018: 7.0,
            2019: 7.5, 2020: 8.5, 2021: 9.5, 2022: 10.5, 2023: 11.0,
            2024: 12.0,
        },
    },
    "havaianas-vendidas-br-milhoes": {
        "label": "Pares de Havaianas vendidos no Brasil (milhões)",
        "categoria": "consumo",
        "fonte_nome": "Alpargatas — relatórios anuais",
        "fonte_url": "https://ri.alpargatas.com.br/",
        "dados": {
            2010: 152, 2011: 158, 2012: 162, 2013: 168, 2014: 170,
            2015: 165, 2016: 160, 2017: 168, 2018: 175, 2019: 180,
            2020: 168, 2021: 175, 2022: 188, 2023: 192, 2024: 195,
        },
    },
    "havaianas-vendidas-ext-milhoes": {
        "label": "Pares de Havaianas vendidos no exterior (milhões)",
        "categoria": "consumo",
        "fonte_nome": "Alpargatas — relatórios anuais",
        "fonte_url": "https://ri.alpargatas.com.br/",
        "dados": {
            2010: 32, 2011: 38, 2012: 45, 2013: 52, 2014: 55,
            2015: 52, 2016: 48, 2017: 50, 2018: 56, 2019: 60,
            2020: 52, 2021: 60, 2022: 64, 2023: 65, 2024: 65,
        },
    },
    "alpargatas-receita-bilhoes-rs": {
        "label": "Receita líquida da Alpargatas (R$ bilhões)",
        "categoria": "economia",
        "fonte_nome": "Alpargatas — relatórios anuais (4T)",
        "fonte_url": "https://ri.alpargatas.com.br/",
        "dados": {
            2010: 2.4, 2011: 2.6, 2012: 2.9, 2013: 3.2, 2014: 3.5,
            2015: 3.7, 2016: 4.2, 2017: 4.4, 2018: 3.8, 2019: 3.6,
            2020: 3.5, 2021: 4.2, 2022: 4.4, 2023: 4.0, 2024: 4.3,
        },
    },
    "milei-aprovacao-pct": {
        "label": "Aprovação do governo Milei na Argentina (%, média anual de pesquisas)",
        "categoria": "internacional",
        "fonte_nome": "Pesquisas agregadas (CB Consultora, Ibarómetro, Zuban Córdoba)",
        "fonte_url": "https://www.cba.consult/",
        "dados": {
            2023: 55, 2024: 51, 2025: 46,
        },
    },
    "pistache-mundo-mil-toneladas": {
        "label": "Produção mundial de pistache (mil toneladas)",
        "categoria": "consumo",
        "fonte_nome": "International Nut & Dried Fruit Council (INC)",
        "fonte_url": "https://www.nutfruit.org/industry/statistics",
        "dados": {
            2010: 600, 2011: 750, 2012: 950, 2013: 850, 2014: 875,
            2015: 800, 2016: 950, 2017: 850, 2018: 900, 2019: 1100,
            2020: 1050, 2021: 1200, 2022: 950, 2023: 1100, 2024: 1300,
        },
    },

    # ---- ENEM abstenção em números absolutos ----------------------------
    "enem-abstencao-absoluto-milhoes": {
        "label": "ENEM — total de candidatos faltantes no primeiro dia (milhões)",
        "categoria": "educacao",
        "fonte_nome": "INEP / MEC — inscritos × abstenção",
        "fonte_url": "https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/enem",
        "dados": {
            # inscritos * abstencao_pct / 100, arredondado a 0,01 milhão
            2010: 1.33, 2011: 1.67, 2012: 1.73, 2013: 1.98, 2014: 2.40,
            2015: 2.33, 2016: 2.49, 2017: 2.28, 2018: 1.41, 2019: 1.19,
            2020: 2.99, 2021: 0.82, 2022: 0.96, 2023: 1.10, 2024: 1.14,
        },
    },

    # ---- Brasileirão: pontos dos 12 grandes clubes ----------------------
    # Brasileirão por pontos corridos desde 2003. 38 jogos por temporada
    # desde 2006. Para anos na Série B, marcamos como 0 (clube fora da Série A).
    # Fonte: CBF + Wikipedia (Campeonato Brasileiro Série A).
}


# Pontos dos 12 grandes na Série A por ano (2003–2024).
# 0 quando o clube esteve na Série B ou Série C.
BRASILEIRAO_PONTOS = {
    "flamengo": {
        2003: 60, 2004: 56, 2005: 49, 2006: 41, 2007: 61, 2008: 51,
        2009: 67, 2010: 50, 2011: 65, 2012: 58, 2013: 49, 2014: 52,
        2015: 53, 2016: 71, 2017: 56, 2018: 72, 2019: 90, 2020: 71,
        2021: 71, 2022: 70, 2023: 66, 2024: 79,
    },
    "palmeiras": {
        2003: 67, 2004: 47, 2005: 60, 2006: 50, 2007: 67, 2008: 65,
        2009: 67, 2010: 41, 2011: 45, 2012: 36, 2013: 0, 2014: 41,  # 2013: Serie B
        2015: 59, 2016: 80, 2017: 63, 2018: 80, 2019: 74, 2020: 70,
        2021: 66, 2022: 81, 2023: 73, 2024: 73,
    },
    "corinthians": {
        2003: 53, 2004: 53, 2005: 81, 2006: 53, 2007: 44, 2008: 0,  # 2008: Serie B
        2009: 56, 2010: 65, 2011: 71, 2012: 64, 2013: 64, 2014: 69,
        2015: 81, 2016: 51, 2017: 72, 2018: 44, 2019: 56, 2020: 51,
        2021: 57, 2022: 65, 2023: 47, 2024: 44,
    },
    "sao-paulo": {
        2003: 54, 2004: 64, 2005: 66, 2006: 78, 2007: 77, 2008: 75,
        2009: 67, 2010: 57, 2011: 64, 2012: 66, 2013: 53, 2014: 70,
        2015: 62, 2016: 50, 2017: 50, 2018: 63, 2019: 63, 2020: 66,
        2021: 49, 2022: 49, 2023: 51, 2024: 54,
    },
    "santos": {
        2003: 65, 2004: 89, 2005: 60, 2006: 60, 2007: 64, 2008: 56,
        2009: 64, 2010: 71, 2011: 63, 2012: 53, 2013: 53, 2014: 60,
        2015: 64, 2016: 71, 2017: 63, 2018: 50, 2019: 74, 2020: 54,
        2021: 47, 2022: 54, 2023: 43, 2024: 0,  # 2024: Serie B
    },
    "vasco": {
        2003: 64, 2004: 47, 2005: 53, 2006: 47, 2007: 54, 2008: 31,
        2009: 0, 2010: 56, 2011: 65, 2012: 49, 2013: 32, 2014: 0,
        2015: 41, 2016: 0, 2017: 56, 2018: 43, 2019: 49, 2020: 41,
        2021: 0, 2022: 0, 2023: 42, 2024: 50,
    },
    "fluminense": {
        2003: 49, 2004: 38, 2005: 51, 2006: 56, 2007: 49, 2008: 49,
        2009: 46, 2010: 71, 2011: 53, 2012: 77, 2013: 42, 2014: 56,
        2015: 53, 2016: 51, 2017: 60, 2018: 49, 2019: 46, 2020: 64,
        2021: 54, 2022: 70, 2023: 55, 2024: 46,
    },
    "botafogo": {
        2003: 59, 2004: 49, 2005: 0, 2006: 55, 2007: 53, 2008: 50,
        2009: 56, 2010: 56, 2011: 53, 2012: 53, 2013: 65, 2014: 38,
        2015: 0, 2016: 55, 2017: 53, 2018: 51, 2019: 43, 2020: 27,
        2021: 0, 2022: 53, 2023: 68, 2024: 79,
    },
    "atletico-mg": {
        2003: 53, 2004: 36, 2005: 0, 2006: 0, 2007: 0, 2008: 0,
        2009: 41, 2010: 47, 2011: 58, 2012: 72, 2013: 64, 2014: 69,
        2015: 70, 2016: 71, 2017: 54, 2018: 59, 2019: 47, 2020: 68,
        2021: 84, 2022: 58, 2023: 66, 2024: 47,
    },
    "cruzeiro": {
        2003: 100, 2004: 80, 2005: 56, 2006: 60, 2007: 49, 2008: 67,
        2009: 67, 2010: 60, 2011: 41, 2012: 47, 2013: 76, 2014: 80,
        2015: 53, 2016: 50, 2017: 53, 2018: 52, 2019: 36, 2020: 0,
        2021: 0, 2022: 0, 2023: 47, 2024: 51,
    },
    "internacional": {
        2003: 49, 2004: 53, 2005: 71, 2006: 81, 2007: 51, 2008: 63,
        2009: 65, 2010: 65, 2011: 51, 2012: 47, 2013: 65, 2014: 69,
        2015: 69, 2016: 43, 2017: 0, 2018: 69, 2019: 65, 2020: 70,
        2021: 60, 2022: 73, 2023: 53, 2024: 70,
    },
    "gremio": {
        2003: 41, 2004: 0, 2005: 0, 2006: 67, 2007: 60, 2008: 67,
        2009: 67, 2010: 51, 2011: 63, 2012: 67, 2013: 65, 2014: 65,
        2015: 60, 2016: 56, 2017: 62, 2018: 75, 2019: 65, 2020: 51,
        2021: 43, 2022: 0, 2023: 68, 2024: 45,
    },
}


def expand_brasileirao_into_extras():
    """Adiciona uma série por clube ao dicionário EXTRAS."""
    nomes_amigaveis = {
        "flamengo": "Flamengo", "palmeiras": "Palmeiras",
        "corinthians": "Corinthians", "sao-paulo": "São Paulo",
        "santos": "Santos", "vasco": "Vasco",
        "fluminense": "Fluminense", "botafogo": "Botafogo",
        "atletico-mg": "Atlético Mineiro", "cruzeiro": "Cruzeiro",
        "internacional": "Internacional", "gremio": "Grêmio",
    }
    for slug, dados in BRASILEIRAO_PONTOS.items():
        EXTRAS[f"brasileirao-pontos-{slug}"] = {
            "label": f"Pontos do {nomes_amigaveis[slug]} no Brasileirão Série A (0 = ano em Série B/C)",
            "categoria": "esporte",
            "fonte_nome": "CBF / Wikipedia — Campeonato Brasileiro Série A",
            "fonte_url": f"https://pt.wikipedia.org/wiki/{nomes_amigaveis[slug].replace(' ', '_')}_(futebol)",
            "dados": dados,
        }


expand_brasileirao_into_extras()
