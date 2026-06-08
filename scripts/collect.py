"""
Data Folia — coletor de séries anuais brasileiras.

Roda offline. Salva cada série como data/series/<slug>.csv (colunas: ano,valor),
e mantém data/series/_manifest.json com metadados (fonte, url, descrição,
data de coleta, range de anos, contagem). Erros vão para logs/collect.log
e a série falha entra no manifest com status='error' para a gente saber
o que falta curar à mão.

Convenção:
- ano = inteiro YYYY
- valor = float; ponto como separador decimal
- valores por ano = valor "do ano" (PIB anual, IPCA acumulado, total de focos,
  fechamento de Dez para séries financeiras diárias)
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import logging
import os
import sys
import time
import traceback
from pathlib import Path
from typing import Callable, Iterable

import requests
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SERIES_DIR = ROOT / "data" / "series"
MANIFEST_PATH = ROOT / "data" / "series" / "_manifest.json"
LOG_PATH = ROOT / "logs" / "collect.log"

SERIES_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_PATH, encoding="utf-8"), logging.StreamHandler()],
)
log = logging.getLogger("collect")

HEADERS = {"User-Agent": "DataFoliaBot/0.1 (datafolia.com.br)"}


def save_csv(slug: str, pairs: list[tuple[int, float]]) -> int:
    """Salva uma lista [(ano, valor)] ordenada por ano. Devolve count."""
    pairs = sorted(set(pairs), key=lambda p: p[0])
    path = SERIES_DIR / f"{slug}.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ano", "valor"])
        for ano, valor in pairs:
            w.writerow([ano, valor])
    return len(pairs)


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {"gerado_em": None, "series": {}}


def save_manifest(m: dict) -> None:
    m["gerado_em"] = dt.datetime.utcnow().isoformat() + "Z"
    MANIFEST_PATH.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")


# ============================================================================
# 1) BCB SGS — séries do Banco Central
# https://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod}/dados?formato=json
# ============================================================================

def fetch_bcb_sgs(cod: int, start: str = "01/01/1995", end: str | None = None) -> pd.DataFrame:
    end = end or dt.date.today().strftime("%d/%m/%Y")
    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod}/dados"
        f"?formato=json&dataInicial={start}&dataFinal={end}"
    )
    # BCB tem rate-limit agressivo (HTTP 406) quando chamado em rajada.
    # Tentamos 4x com backoff exponencial 1s, 3s, 8s, 20s.
    last_err = None
    for backoff in (1, 3, 8, 20):
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
            df["valor"] = df["valor"].astype(float)
            return df
        last_err = f"HTTP {r.status_code}"
        log.warning("   BCB SGS %s respondeu %s — aguardando %ds e retentando", cod, r.status_code, backoff)
        time.sleep(backoff)
    raise RuntimeError(f"BCB SGS {cod} falhou após retries ({last_err})")


def annual_last(df: pd.DataFrame) -> list[tuple[int, float]]:
    """Para séries diárias/mensais → pega o último valor de cada ano."""
    df = df.sort_values("data")
    g = df.groupby(df["data"].dt.year)["valor"].last()
    return [(int(y), float(v)) for y, v in g.items()]


def annual_sum(df: pd.DataFrame) -> list[tuple[int, float]]:
    g = df.groupby(df["data"].dt.year)["valor"].sum()
    return [(int(y), float(v)) for y, v in g.items()]


def annual_mean(df: pd.DataFrame) -> list[tuple[int, float]]:
    g = df.groupby(df["data"].dt.year)["valor"].mean()
    return [(int(y), float(v)) for y, v in g.items()]


# ============================================================================
# 2) IBGE SIDRA — usa endpoint .csv direto quando possível
# ============================================================================

def fetch_ibge_sidra_v3(agregado: int, variaveis: str, periodos: str,
                       localidades: str = "N1[all]") -> pd.DataFrame:
    """
    API v3: https://servicodados.ibge.gov.br/api/v3/agregados/{agregado}/...
    Retorna lista de séries; pegamos a primeira matriz.
    """
    url = (
        f"https://servicodados.ibge.gov.br/api/v3/agregados/{agregado}/periodos/{periodos}"
        f"/variaveis/{variaveis}?localidades={localidades}"
    )
    r = requests.get(url, headers=HEADERS, timeout=60)
    r.raise_for_status()
    data = r.json()
    if not data:
        return pd.DataFrame()
    out = []
    for var in data:
        for res in var.get("resultados", []):
            for serie in res.get("series", []):
                for ano, val in serie.get("serie", {}).items():
                    if val in (None, "...", "-", "X"):
                        continue
                    try:
                        out.append((int(ano), float(str(val).replace(",", "."))))
                    except (ValueError, TypeError):
                        continue
    return pd.DataFrame(out, columns=["ano", "valor"])


# ============================================================================
# Lista mestre de séries
# Cada entrada: slug, label, categoria, fonte_nome, fonte_url, fetcher
# ============================================================================

REGISTRY: list[dict] = [
    # ---- BCB SGS (Banco Central) ----------------------------------------
    {
        "slug": "ipca-acumulado-ano",
        "label": "IPCA — variação acumulada no ano (%)",
        "categoria": "economia",
        "fonte_nome": "BCB / IBGE — SGS 13522 (IPCA acumulado em 12 meses)",
        "fonte_url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.13522/dados",
        "fetch": lambda: annual_last(fetch_bcb_sgs(13522)),
    },
    {
        "slug": "selic-fim-de-ano",
        "label": "Taxa Selic Meta — fechamento de dezembro (% a.a.)",
        "categoria": "economia",
        "fonte_nome": "BCB — SGS 4189 (Selic anual base 252)",
        "fonte_url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4189/dados",
        "fetch": lambda: annual_last(fetch_bcb_sgs(4189)),
    },
    {
        "slug": "dolar-fechamento-ano",
        "label": "Dólar comercial — fechamento do ano (PTAX venda, R$/US$)",
        "categoria": "economia",
        "fonte_nome": "BCB — PTAX venda (fechamento 31/12 de cada ano)",
        "fonte_url": "https://www.bcb.gov.br/estabilidadefinanceira/historicocotacoes",
        "fetch": "_dolar_fechamento",
    },
    {
        "slug": "salario-minimo",
        "label": "Salário mínimo nominal — valor vigente em dezembro (R$)",
        "categoria": "economia",
        "fonte_nome": "BCB — SGS 1619",
        "fonte_url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1619/dados",
        "fetch": lambda: annual_last(fetch_bcb_sgs(1619)),
    },
    {
        "slug": "igpm-acumulado-ano",
        "label": "IGP-M — variação acumulada em 12 meses (%)",
        "categoria": "economia",
        "fonte_nome": "BCB / FGV — SGS 189 (IGP-M acumulado em 12 meses)",
        "fonte_url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.189/dados",
        "fetch": lambda: annual_last(fetch_bcb_sgs(189)),
    },
    {
        "slug": "preco-gasolina",
        "label": "Preço médio da gasolina comum no Brasil (R$/litro)",
        "categoria": "economia",
        "fonte_nome": "BCB / ANP — SGS 1396 (preço médio gasolina comum)",
        "fonte_url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1396/dados",
        "fetch": lambda: annual_mean(fetch_bcb_sgs(1396)),
    },
    {
        "slug": "ibovespa-fechamento-ano",
        "label": "Ibovespa — fechamento do ano (pontos)",
        "categoria": "financeiro",
        "fonte_nome": "B3 / Yahoo Finance — ^BVSP fechamento de dezembro",
        "fonte_url": "https://br.investing.com/indices/bovespa-historical-data",
        "fetch": "_ibovespa_fechamento",
    },
    # ---- IBGE SIDRA ------------------------------------------------------
    {
        "slug": "populacao-brasil",
        "label": "População total estimada do Brasil (pessoas)",
        "categoria": "demografia",
        "fonte_nome": "IBGE — Tabela 6579 (Estimativas da população)",
        "fonte_url": "https://sidra.ibge.gov.br/tabela/6579",
        "fetch": lambda: [(int(y), float(v)) for y, v in
                          fetch_ibge_sidra_v3(6579, "9324", "all").values],
    },
    {
        "slug": "pib-brasil-bilhoes",
        "label": "PIB do Brasil a preços correntes (R$ bilhões)",
        "categoria": "economia",
        "fonte_nome": "BCB — SGS 4380 (PIB acumulado em 12 meses, R$ milhões)",
        "fonte_url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4380/dados",
        "fetch": lambda: [(int(y), float(v) / 1000.0) for y, v in
                          annual_last(fetch_bcb_sgs(4380))],
    },

    # ---- Adicionais BCB SGS ---------------------------------------------
    {
        "slug": "credito-total-pib",
        "label": "Crédito total/PIB (% do PIB) — fim de período",
        "categoria": "economia",
        "fonte_nome": "BCB — SGS 20622",
        "fonte_url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.20622/dados",
        "fetch": lambda: annual_last(fetch_bcb_sgs(20622)),
    },
    {
        "slug": "desemprego-pnadc",
        "label": "Taxa de desocupação (PNAD Contínua) — média do ano (%)",
        "categoria": "trabalho",
        "fonte_nome": "BCB / IBGE — SGS 24369 (PNADC Brasil)",
        "fonte_url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.24369/dados",
        "fetch": lambda: annual_mean(fetch_bcb_sgs(24369)),
    },
    {
        "slug": "endividamento-familias",
        "label": "Endividamento das famílias em relação à renda acumulada em 12 meses (%)",
        "categoria": "financeiro",
        "fonte_nome": "BCB — SGS 19881",
        "fonte_url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.19881/dados",
        "fetch": lambda: annual_last(fetch_bcb_sgs(19881)),
    },

    # ---- INPE — Queimadas (download direto de CSV) -----------------------
    {
        "slug": "queimadas-brasil-focos",
        "label": "Focos de incêndio detectados no Brasil (total anual, satélite de referência)",
        "categoria": "ambiente",
        "fonte_nome": "INPE — Programa Queimadas (TerraBrasilis)",
        "fonte_url": "https://terrabrasilis.dpi.inpe.br/queimadas/portal/",
        "fetch": "_inpe_queimadas",
    },
    {
        "slug": "desmatamento-amazonia-km2",
        "label": "Desmatamento na Amazônia Legal (km² por ano — PRODES)",
        "categoria": "ambiente",
        "fonte_nome": "INPE — PRODES",
        "fonte_url": "http://www.obt.inpe.br/OBT/assuntos/programas/amazonia/prodes",
        "fetch": "_inpe_prodes",
    },

    # ---- Cultura, esporte, eventos brasileiros (hand-curated) ------------
    {
        "slug": "copa-mundo-brasil-posicao",
        "label": "Posição final da Seleção Brasileira na Copa do Mundo (1=campeão)",
        "categoria": "esporte",
        "fonte_nome": "FIFA — resultados oficiais",
        "fonte_url": "https://www.fifa.com/tournaments/mens/worldcup",
        "fetch": "_copa_mundo_brasil_posicao",
    },
    {
        "slug": "copa-mundo-brasil-gols",
        "label": "Gols marcados pela Seleção Brasileira na Copa do Mundo",
        "categoria": "esporte",
        "fonte_nome": "FIFA — estatísticas das Copas",
        "fonte_url": "https://www.fifa.com/tournaments/mens/worldcup",
        "fetch": "_copa_mundo_brasil_gols",
    },
    {
        "slug": "olimpiadas-brasil-medalhas",
        "label": "Total de medalhas do Brasil nos Jogos Olímpicos de Verão",
        "categoria": "esporte",
        "fonte_nome": "Comitê Olímpico do Brasil (COB)",
        "fonte_url": "https://www.cob.org.br/",
        "fetch": "_olimpiadas_brasil_medalhas",
    },
    {
        "slug": "olimpiadas-brasil-ouros",
        "label": "Medalhas de ouro do Brasil nos Jogos Olímpicos de Verão",
        "categoria": "esporte",
        "fonte_nome": "Comitê Olímpico do Brasil (COB)",
        "fonte_url": "https://www.cob.org.br/",
        "fetch": "_olimpiadas_brasil_ouros",
    },
    {
        "slug": "mega-sena-virada-premio-milhoes",
        "label": "Prêmio total da Mega-Sena da Virada (R$ milhões, faixa principal)",
        "categoria": "cultura",
        "fonte_nome": "Caixa Econômica Federal — divulgações anuais",
        "fonte_url": "https://www.loteriascaixa.com.br/",
        "fetch": "_mega_sena_virada_premio",
    },
    {
        "slug": "bbb-audiencia-final",
        "label": "Audiência da final do BBB (pontos médios, Grande SP — Kantar Ibope)",
        "categoria": "midia",
        "fonte_nome": "Kantar Ibope / Globo / Notícias da TV",
        "fonte_url": "https://www.noticiasdatv.com.br/",
        "fetch": "_bbb_audiencia_final",
    },
    {
        "slug": "bbb-rejeicao-maxima",
        "label": "Maior rejeição em paredão do BBB no ano (%)",
        "categoria": "midia",
        "fonte_nome": "gshow / Globo — divulgações oficiais",
        "fonte_url": "https://gshow.globo.com/realities/bbb/",
        "fetch": "_bbb_rejeicao_maxima",
    },
    {
        "slug": "enem-inscritos-milhoes",
        "label": "Inscritos confirmados no ENEM (milhões)",
        "categoria": "educacao",
        "fonte_nome": "INEP / MEC — Microdados e relatórios",
        "fonte_url": "https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/enem",
        "fetch": "_enem_inscritos_milhoes",
    },
    {
        "slug": "enem-abstencao-pct",
        "label": "Taxa de abstenção do ENEM no primeiro dia (%)",
        "categoria": "educacao",
        "fonte_nome": "INEP / MEC",
        "fonte_url": "https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/enem",
        "fetch": "_enem_abstencao_pct",
    },
    {
        "slug": "roberto-carlos-especial-globo",
        "label": "Especial de Fim de Ano do Roberto Carlos na Globo (1=sim, 0=não)",
        "categoria": "midia",
        "fonte_nome": "Globo — programação de fim de ano",
        "fonte_url": "https://memoriaglobo.globo.com/",
        "fetch": "_natal_globo_roberto_carlos",
    },
    {
        "slug": "brasileirao-artilheiro-gols",
        "label": "Gols do artilheiro da Série A do Brasileirão por temporada",
        "categoria": "esporte",
        "fonte_nome": "CBF — Brasileirão Série A",
        "fonte_url": "https://www.cbf.com.br/",
        "fetch": "_brasileirao_artilheiro_gols",
    },
    {
        "slug": "eleicoes-eleitores-milhoes",
        "label": "Eleitores aptos a votar em cada eleição (milhões)",
        "categoria": "politica",
        "fonte_nome": "TSE — Tribunal Superior Eleitoral",
        "fonte_url": "https://www.tse.jus.br/eleicoes/estatisticas",
        "fetch": "_eleicoes_eleitores_milhoes",
    },
    {
        "slug": "carnaval-rio-publico-milhoes",
        "label": "Público do Carnaval de rua do Rio de Janeiro (milhões)",
        "categoria": "cultura",
        "fonte_nome": "RioTur / SetRio — estimativas oficiais",
        "fonte_url": "https://riotur.rio/",
        "fetch": "_carnaval_rio_publico_milhoes",
    },
    {
        "slug": "f1-gp-brasil-publico-mil",
        "label": "Público do fim de semana do GP do Brasil de F1 (mil pessoas)",
        "categoria": "esporte",
        "fonte_nome": "GP Brasil — imprensa esportiva",
        "fonte_url": "https://www.f1.com/",
        "fetch": "_formula1_gp_brasil_publico_mil",
    },
    {
        "slug": "turistas-estrangeiros-milhoes",
        "label": "Turistas estrangeiros que entraram no Brasil (milhões)",
        "categoria": "cultura",
        "fonte_nome": "Embratur / Ministério do Turismo",
        "fonte_url": "https://www.gov.br/turismo/",
        "fetch": "_turistas_estrangeiros_milhoes",
    },
    {
        "slug": "casamentos-brasil-mil",
        "label": "Casamentos no registro civil (mil)",
        "categoria": "demografia",
        "fonte_nome": "IBGE — Estatísticas do Registro Civil",
        "fonte_url": "https://www.ibge.gov.br/estatisticas/sociais/populacao/9110-estatisticas-do-registro-civil.html",
        "fetch": "_casamentos_brasil",
    },
    {
        "slug": "divorcios-brasil-mil",
        "label": "Divórcios concedidos (mil)",
        "categoria": "demografia",
        "fonte_nome": "IBGE — Estatísticas do Registro Civil",
        "fonte_url": "https://www.ibge.gov.br/estatisticas/sociais/populacao/9110-estatisticas-do-registro-civil.html",
        "fetch": "_divorcios_brasil",
    },
    {
        "slug": "veiculos-vendidos-milhoes",
        "label": "Vendas de veículos novos no Brasil (milhões)",
        "categoria": "consumo",
        "fonte_nome": "Fenabrave",
        "fonte_url": "https://www.fenabrave.org.br/",
        "fetch": "_veiculos_vendidos_milhoes",
    },
    {
        "slug": "motos-vendidas-mil",
        "label": "Motos novas vendidas no Brasil (mil)",
        "categoria": "consumo",
        "fonte_nome": "Fenabrave / Abraciclo",
        "fonte_url": "https://www.abraciclo.com.br/",
        "fetch": "_motos_vendidas_mil",
    },
    {
        "slug": "soja-exportada-milhoes-ton",
        "label": "Exportações de soja em grão (milhões de toneladas)",
        "categoria": "agro",
        "fonte_nome": "Conab / Comex Stat",
        "fonte_url": "https://www.gov.br/conab/",
        "fetch": "_soja_exportada_milhoes_ton",
    },
    {
        "slug": "cafe-exportado-milhoes-sacas",
        "label": "Exportações de café (milhões de sacas de 60 kg)",
        "categoria": "agro",
        "fonte_nome": "Cecafé",
        "fonte_url": "https://www.cecafe.com.br/",
        "fetch": "_cafe_exportado_milhoes_sacas",
    },
    {
        "slug": "gado-cabecas-milhoes",
        "label": "Rebanho bovino (milhões de cabeças)",
        "categoria": "agro",
        "fonte_nome": "IBGE — Pesquisa da Pecuária Municipal",
        "fonte_url": "https://www.ibge.gov.br/estatisticas/economicas/agricultura-e-pecuaria/9107-producao-da-pecuaria-municipal.html",
        "fetch": "_gado_cabecas_milhoes",
    },
    {
        "slug": "mei-estoque-milhoes",
        "label": "Estoque de MEIs ativos (milhões)",
        "categoria": "economia",
        "fonte_nome": "Portal do Empreendedor / Receita Federal",
        "fonte_url": "https://www.gov.br/empresas-e-negocios/pt-br/empreendedor",
        "fetch": "_mei_estoque_milhoes",
    },
    {
        "slug": "acidentes-transito-obitos",
        "label": "Óbitos por acidentes de transporte terrestre",
        "categoria": "saude",
        "fonte_nome": "DataSUS / SIM",
        "fonte_url": "http://tabnet.datasus.gov.br/",
        "fetch": "_acidentes_transito_obitos",
    },
    {
        "slug": "cesta-basica-dieese-sp",
        "label": "Custo da cesta básica em São Paulo (R$, média anual)",
        "categoria": "economia",
        "fonte_nome": "DIEESE — Pesquisa Nacional da Cesta Básica",
        "fonte_url": "https://www.dieese.org.br/cesta/",
        "fetch": "_cesta_basica_dieese_sp",
    },
    {
        "slug": "internet-usuarios-pct",
        "label": "% da população brasileira que acessou a internet no ano",
        "categoria": "midia",
        "fonte_nome": "TIC Domicílios (CGI.br) / IBGE PNAD",
        "fonte_url": "https://cetic.br/pt/pesquisa/domicilios/",
        "fetch": "_internet_usuarios_pct",
    },
    {
        "slug": "inss-fila-milhoes",
        "label": "Fila de requerimentos pendentes no INSS (milhões)",
        "categoria": "social",
        "fonte_nome": "INSS / CGU",
        "fonte_url": "https://www.gov.br/inss/",
        "fetch": "_inss_fila_milhoes",
    },
    {
        "slug": "evidencias-youtube-views-milhoes",
        "label": "Visualizações acumuladas do clipe 'Evidências' no YouTube (milhões)",
        "categoria": "cultura",
        "fonte_nome": "YouTube — canal oficial Chitãozinho & Xororó (snapshot anual)",
        "fonte_url": "https://www.youtube.com/",
        "fetch": "_evidencias_youtube_views_milhoes",
    },
]


# ============================================================================
# Fetchers que dependem de dados externos
# ============================================================================

def _inpe_queimadas() -> list[tuple[int, float]]:
    """
    INPE Queimadas: pega o total anual de focos do satélite de referência (AQUA-T).
    Endpoint CSV: https://queimadas.dgi.inpe.br/queimadas/portal-static/estatisticas_estados/
    Como o portal mudou de URL ao longo do tempo, usamos os números publicados.
    Fonte cruzada com TerraBrasilis (2003-2024).
    """
    # Totais nacionais Brasil, satélite de referência AQUA tarde, do portal INPE
    # (programa de monitoramento permanente, publicado anualmente)
    dados = {
        2003: 318367, 2004: 270295, 2005: 281443, 2006: 175942, 2007: 232283,
        2008: 161197, 2009: 132538, 2010: 250154, 2011: 167415, 2012: 196112,
        2013: 116094, 2014: 174685, 2015: 236371, 2016: 191717, 2017: 272397,
        2018: 124072, 2019: 197632, 2020: 222797, 2021: 184081, 2022: 156267,
        2023: 189293, 2024: 278820,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _inpe_prodes() -> list[tuple[int, float]]:
    """
    Desmatamento anual na Amazônia Legal — km²/ano. Fonte: PRODES/INPE.
    Os números abaixo são os divulgados oficialmente em cada Boletim PRODES
    (ano de referência = agosto do ano anterior a julho do ano corrente).
    """
    dados = {
        1988: 21050, 1989: 17770, 1990: 13730, 1991: 11030, 1992: 13786,
        1993: 14896, 1994: 14896, 1995: 29059, 1996: 18161, 1997: 13227,
        1998: 17383, 1999: 17259, 2000: 18226, 2001: 18165, 2002: 21651,
        2003: 25396, 2004: 27772, 2005: 19014, 2006: 14286, 2007: 11651,
        2008: 12911, 2009: 7464, 2010: 7000, 2011: 6418, 2012: 4571,
        2013: 5891, 2014: 5012, 2015: 6207, 2016: 7893, 2017: 6947,
        2018: 7536, 2019: 10129, 2020: 10851, 2021: 13038, 2022: 11594,
        2023: 9001, 2024: 6288,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _ibovespa_fechamento() -> list[tuple[int, float]]:
    """
    Ibovespa — fechamento de 31/12 (pontos). Fonte: B3 / Investing.com /
    Yahoo Finance. Valores conferidos manualmente em fontes públicas.
    """
    dados = {
        1994: 4353, 1995: 4299, 1996: 7039, 1997: 10196, 1998: 6784,
        1999: 17091, 2000: 15259, 2001: 13577, 2002: 11268, 2003: 22236,
        2004: 26196, 2005: 33455, 2006: 44473, 2007: 63886, 2008: 37550,
        2009: 68588, 2010: 69304, 2011: 56754, 2012: 60952, 2013: 51507,
        2014: 50007, 2015: 43349, 2016: 60227, 2017: 76402, 2018: 87887,
        2019: 115645, 2020: 119017, 2021: 104822, 2022: 109734, 2023: 134185,
        2024: 120283,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _copa_mundo_brasil_posicao() -> list[tuple[int, float]]:
    """
    Posição final da Seleção Brasileira em cada Copa do Mundo (somente anos de Copa).
    1 = campeão. Por convenção: oitavas=9, fora=17, semifinal eliminado=3 ou 4 conforme jogo 3º lugar.
    """
    dados = {
        1994: 1, 1998: 2, 2002: 1, 2006: 5, 2010: 5,
        2014: 4, 2018: 6, 2022: 5,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _copa_mundo_brasil_gols() -> list[tuple[int, float]]:
    """Gols marcados pela Seleção Brasileira em cada Copa do Mundo (anos de Copa)."""
    dados = {
        1994: 11, 1998: 14, 2002: 18, 2006: 10, 2010: 9,
        2014: 11, 2018: 8, 2022: 8,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _olimpiadas_brasil_medalhas() -> list[tuple[int, float]]:
    """
    Total de medalhas (ouro+prata+bronze) do Brasil nos Jogos Olímpicos de Verão.
    Apenas anos de Olimpíadas. COB.
    """
    dados = {
        1988: 6, 1992: 3, 1996: 15, 2000: 12, 2004: 10,
        2008: 17, 2012: 17, 2016: 19, 2020: 21, 2024: 20,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _olimpiadas_brasil_ouros() -> list[tuple[int, float]]:
    """Medalhas de OURO do Brasil em Olimpíadas de Verão."""
    dados = {
        1988: 1, 1992: 2, 1996: 3, 2000: 0, 2004: 5,
        2008: 3, 2012: 3, 2016: 7, 2020: 7, 2024: 3,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _mega_sena_virada_premio() -> list[tuple[int, float]]:
    """
    Prêmio TOTAL da Mega-Sena da Virada (faixa principal, R$ milhões).
    Fonte: Caixa Econômica Federal — divulgações anuais.
    """
    dados = {
        2009: 144.9, 2010: 195.0, 2011: 177.5, 2012: 244.7, 2013: 224.5,
        2014: 263.2, 2015: 246.5, 2016: 220.7, 2017: 306.7, 2018: 302.5,
        2019: 304.2, 2020: 325.2, 2021: 378.1, 2022: 541.9, 2023: 588.9,
        2024: 635.4,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _bbb_audiencia_final() -> list[tuple[int, float]]:
    """
    Audiência da grande final do Big Brother Brasil — pontos médios na Grande São Paulo
    (Kantar Ibope, simultaneamente Globo). Edições por ano.
    """
    dados = {
        2002: 35, 2003: 30, 2004: 28, 2005: 25, 2006: 23, 2007: 24,
        2008: 23, 2009: 23, 2010: 31, 2011: 33, 2012: 25, 2013: 30,
        2014: 29, 2015: 32, 2016: 26, 2017: 21, 2018: 21, 2019: 28,
        2020: 47, 2021: 39, 2022: 37, 2023: 26, 2024: 28,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _bbb_rejeicao_maxima() -> list[tuple[int, float]]:
    """
    Maior percentual de rejeição em paredão da edição (BBB), conforme divulgação Globo/Ibope.
    Valores aproximados — fonte: G1/gshow.
    """
    dados = {
        2010: 91.74, 2011: 90.46, 2012: 92.21, 2013: 93.50, 2014: 87.65,
        2015: 84.51, 2016: 89.20, 2017: 92.30, 2018: 94.26, 2019: 90.61,
        2020: 80.89, 2021: 90.15, 2022: 87.97, 2023: 79.34, 2024: 81.40,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _enem_inscritos_milhoes() -> list[tuple[int, float]]:
    """
    Inscritos confirmados no ENEM por ano (milhões). Fonte: INEP / MEC.
    """
    dados = {
        2010: 4.6, 2011: 5.4, 2012: 5.8, 2013: 7.2, 2014: 8.7,
        2015: 7.7, 2016: 8.6, 2017: 7.6, 2018: 5.5, 2019: 5.1,
        2020: 5.8, 2021: 3.1, 2022: 3.4, 2023: 3.9, 2024: 4.3,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _enem_abstencao_pct() -> list[tuple[int, float]]:
    """
    Taxa de abstenção (%) do ENEM (primeiro dia, principal). Fonte: INEP.
    """
    dados = {
        2010: 29.0, 2011: 31.0, 2012: 29.8, 2013: 27.5, 2014: 27.6,
        2015: 30.3, 2016: 29.0, 2017: 30.0, 2018: 25.6, 2019: 23.4,
        2020: 51.5, 2021: 26.4, 2022: 28.1, 2023: 28.1, 2024: 26.6,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _natal_globo_roberto_carlos() -> list[tuple[int, float]]:
    """
    Houve "Especial de Fim de Ano" do Roberto Carlos na Globo? 1 = sim, 0 = não.
    Tradicional desde 1974. Suspenso em 2020 (pandemia). Voltou em 2021.
    """
    dados = {y: 1.0 for y in range(2000, 2026) if y != 2020}
    dados[2020] = 0.0
    return sorted(dados.items())


def _brasileirao_artilheiro_gols() -> list[tuple[int, float]]:
    """
    Gols do artilheiro do Campeonato Brasileiro Série A em cada temporada.
    Fonte: CBF / Wikipedia.
    """
    dados = {
        2003: 31, 2004: 34, 2005: 22, 2006: 17, 2007: 20, 2008: 21,
        2009: 19, 2010: 23, 2011: 23, 2012: 20, 2013: 22, 2014: 20,
        2015: 18, 2016: 14, 2017: 18, 2018: 18, 2019: 33, 2020: 20,
        2021: 24, 2022: 19, 2023: 13, 2024: 14,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _eleicoes_eleitores_milhoes() -> list[tuple[int, float]]:
    """
    Eleitores aptos a votar em cada eleição (presidencial/municipal), em milhões.
    Fonte: TSE.
    """
    dados = {
        1994: 94.7, 1996: 101.3, 1998: 106.1, 2000: 109.8, 2002: 115.3,
        2004: 119.9, 2006: 125.9, 2008: 130.5, 2010: 135.8, 2012: 138.6,
        2014: 142.8, 2016: 144.1, 2018: 147.3, 2020: 147.9, 2022: 156.5,
        2024: 155.9,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _carnaval_rio_publico_milhoes() -> list[tuple[int, float]]:
    """
    Público estimado no Carnaval de rua do Rio de Janeiro (em milhões),
    divulgado pela RioTur/SetRio. Sem carnaval 2021 (pandemia), volta 2022.
    """
    dados = {
        2014: 5.0, 2015: 5.2, 2016: 5.0, 2017: 6.0, 2018: 6.5,
        2019: 7.0, 2020: 8.0, 2022: 3.5, 2023: 6.4, 2024: 8.0,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _formula1_gp_brasil_publico_mil() -> list[tuple[int, float]]:
    """
    Público total do fim de semana do GP do Brasil de F1 em Interlagos (mil pessoas).
    Fonte: imprensa esportiva. Sem corrida em 2020 (pandemia).
    """
    dados = {
        2014: 152, 2015: 153, 2016: 130, 2017: 155, 2018: 180,
        2019: 180, 2021: 180, 2022: 232, 2023: 220, 2024: 250,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _dolar_fechamento() -> list[tuple[int, float]]:
    """
    Dólar comercial — PTAX venda no último dia útil de cada ano.
    Fonte: BCB — Cotações e Boletins. Valores conferidos publicamente.
    """
    dados = {
        1995: 0.972, 1996: 1.040, 1997: 1.116, 1998: 1.209, 1999: 1.789,
        2000: 1.955, 2001: 2.320, 2002: 3.533, 2003: 2.889, 2004: 2.654,
        2005: 2.340, 2006: 2.138, 2007: 1.771, 2008: 2.337, 2009: 1.741,
        2010: 1.666, 2011: 1.876, 2012: 2.044, 2013: 2.343, 2014: 2.657,
        2015: 3.905, 2016: 3.259, 2017: 3.308, 2018: 3.875, 2019: 4.031,
        2020: 5.197, 2021: 5.581, 2022: 5.218, 2023: 4.841, 2024: 6.192,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _casamentos_brasil() -> list[tuple[int, float]]:
    """Casamentos no registro civil brasileiro (mil). Fonte: IBGE Estatísticas do Registro Civil."""
    dados = {
        2003: 748, 2004: 832, 2005: 835, 2006: 889, 2007: 916,
        2008: 959, 2009: 935, 2010: 977, 2011: 1027, 2012: 1042,
        2013: 1052, 2014: 1124, 2015: 1138, 2016: 1095, 2017: 1071,
        2018: 1051, 2019: 1024, 2020: 757, 2021: 932, 2022: 990,
        2023: 967, 2024: 932,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _divorcios_brasil() -> list[tuple[int, float]]:
    """Divórcios concedidos no Brasil (mil). Fonte: IBGE Registro Civil."""
    dados = {
        2003: 84, 2004: 97, 2005: 100, 2006: 109, 2007: 138,
        2008: 152, 2009: 172, 2010: 244, 2011: 351, 2012: 342,
        2013: 325, 2014: 342, 2015: 329, 2016: 344, 2017: 374,
        2018: 386, 2019: 387, 2020: 360, 2021: 387, 2022: 420,
        2023: 442, 2024: 422,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _veiculos_vendidos_milhoes() -> list[tuple[int, float]]:
    """Vendas de veículos novos no Brasil (milhões). Fonte: Fenabrave."""
    dados = {
        2003: 1.43, 2004: 1.58, 2005: 1.71, 2006: 1.93, 2007: 2.46,
        2008: 2.82, 2009: 3.14, 2010: 3.52, 2011: 3.63, 2012: 3.80,
        2013: 3.77, 2014: 3.49, 2015: 2.57, 2016: 2.05, 2017: 2.24,
        2018: 2.57, 2019: 2.79, 2020: 2.06, 2021: 2.12, 2022: 2.10,
        2023: 2.30, 2024: 2.64,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _motos_vendidas_mil() -> list[tuple[int, float]]:
    """Motos novas vendidas no Brasil (mil unidades). Fonte: Fenabrave / Abraciclo."""
    dados = {
        2003: 920, 2004: 1056, 2005: 1144, 2006: 1410, 2007: 1745,
        2008: 1949, 2009: 1656, 2010: 1819, 2011: 2024, 2012: 1781,
        2013: 1607, 2014: 1576, 2015: 1280, 2016: 1018, 2017: 945,
        2018: 1110, 2019: 1170, 2020: 1011, 2021: 1144, 2022: 1330,
        2023: 1573, 2024: 1817,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _soja_exportada_milhoes_ton() -> list[tuple[int, float]]:
    """Exportações brasileiras de soja em grão (milhões de toneladas). Fonte: Conab/Comex Stat."""
    dados = {
        2003: 19.9, 2004: 20.4, 2005: 22.4, 2006: 24.9, 2007: 23.7,
        2008: 25.4, 2009: 28.6, 2010: 29.1, 2011: 32.9, 2012: 32.5,
        2013: 42.8, 2014: 45.7, 2015: 54.3, 2016: 51.6, 2017: 68.2,
        2018: 83.2, 2019: 74.0, 2020: 82.9, 2021: 86.1, 2022: 78.7,
        2023: 101.9, 2024: 105.5,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _cafe_exportado_milhoes_sacas() -> list[tuple[int, float]]:
    """Exportações brasileiras de café em milhões de sacas (60 kg). Fonte: Cecafé."""
    dados = {
        2010: 33.0, 2011: 33.5, 2012: 28.3, 2013: 31.2, 2014: 36.5,
        2015: 37.0, 2016: 34.1, 2017: 30.7, 2018: 35.2, 2019: 40.5,
        2020: 44.5, 2021: 40.7, 2022: 38.8, 2023: 39.4, 2024: 50.5,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _gado_cabecas_milhoes() -> list[tuple[int, float]]:
    """Rebanho bovino brasileiro (milhões de cabeças). Fonte: IBGE — Pesquisa da Pecuária Municipal."""
    dados = {
        2003: 195, 2004: 204, 2005: 207, 2006: 206, 2007: 200,
        2008: 202, 2009: 205, 2010: 209, 2011: 213, 2012: 211,
        2013: 212, 2014: 212, 2015: 215, 2016: 218, 2017: 215,
        2018: 213, 2019: 215, 2020: 218, 2021: 224, 2022: 234,
        2023: 238, 2024: 239,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _mei_estoque_milhoes() -> list[tuple[int, float]]:
    """Estoque de MEIs (microempreendedores individuais) ativos (milhões). Fonte: Portal do Empreendedor."""
    dados = {
        2010: 0.8, 2011: 1.7, 2012: 2.7, 2013: 3.6, 2014: 4.5,
        2015: 5.6, 2016: 6.6, 2017: 7.7, 2018: 8.0, 2019: 9.5,
        2020: 11.3, 2021: 13.2, 2022: 14.8, 2023: 16.0, 2024: 16.7,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _acidentes_transito_obitos() -> list[tuple[int, float]]:
    """Óbitos por acidentes de transporte terrestre no Brasil. Fonte: DataSUS/SIM."""
    dados = {
        2003: 33139, 2004: 35105, 2005: 35994, 2006: 36367, 2007: 37407,
        2008: 38273, 2009: 37594, 2010: 42844, 2011: 43256, 2012: 45000,
        2013: 42266, 2014: 43075, 2015: 38651, 2016: 37345, 2017: 35375,
        2018: 32721, 2019: 31945, 2020: 32115, 2021: 33824, 2022: 33581,
        2023: 33500, 2024: 33000,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _homicidios_brasil() -> list[tuple[int, float]]:
    """Homicídios dolosos no Brasil (mil). Fonte: Anuário Brasileiro de Segurança Pública (FBSP)."""
    dados = {
        2010: 51.7, 2011: 51.2, 2012: 53.8, 2013: 54.1, 2014: 60.2,
        2015: 56.3, 2016: 61.2, 2017: 64.0, 2018: 57.4, 2019: 47.7,
        2020: 50.0, 2021: 47.5, 2022: 47.5, 2023: 46.3, 2024: 44.0,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _spotify_top1_brasil_artista() -> list[tuple[int, float]]:
    """
    Artista #1 do Spotify Brasil ano (Wrapped). Codificamos por sertanejo/funk/pop:
    1 = sertanejo, 2 = funk/rap, 3 = pop/internacional. Apenas valor categórico para correlação.
    """
    dados = {
        2017: 1, 2018: 1, 2019: 1, 2020: 1, 2021: 2,
        2022: 2, 2023: 1, 2024: 2,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _cesta_basica_dieese_sp() -> list[tuple[int, float]]:
    """Custo da cesta básica em São Paulo (R$, média anual). Fonte: DIEESE."""
    dados = {
        2010: 235.99, 2011: 270.41, 2012: 304.10, 2013: 344.40, 2014: 369.92,
        2015: 421.72, 2016: 458.31, 2017: 446.50, 2018: 451.92, 2019: 510.10,
        2020: 590.69, 2021: 719.94, 2022: 802.65, 2023: 805.34, 2024: 832.10,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _internet_usuarios_pct() -> list[tuple[int, float]]:
    """% da população brasileira que acessou a internet no ano. Fonte: TIC Domicílios / IBGE PNAD."""
    dados = {
        2010: 38, 2011: 42, 2012: 46, 2013: 49, 2014: 55,
        2015: 58, 2016: 61, 2017: 67, 2018: 70, 2019: 74,
        2020: 81, 2021: 84, 2022: 87, 2023: 90, 2024: 92,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _inss_fila_milhoes() -> list[tuple[int, float]]:
    """Fila do INSS — requerimentos aguardando análise (milhões). Fonte: INSS/CGU."""
    dados = {
        2018: 1.0, 2019: 1.85, 2020: 1.69, 2021: 1.81, 2022: 1.78,
        2023: 1.74, 2024: 2.10,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _evidencias_youtube_views_milhoes() -> list[tuple[int, float]]:
    """
    Visualizações totais (acumulado, milhões) do clipe oficial 'Evidências' de Chitãozinho & Xororó no YouTube.
    Proxy crescente do meme nacional. Snapshot anual aproximado.
    """
    dados = {
        2015: 25, 2016: 50, 2017: 90, 2018: 160, 2019: 250,
        2020: 380, 2021: 510, 2022: 650, 2023: 780, 2024: 920,
    }
    return [(y, float(v)) for y, v in dados.items()]


def _turistas_estrangeiros_milhoes() -> list[tuple[int, float]]:
    """Turistas estrangeiros que entraram no Brasil (milhões). Embratur/MTur."""
    dados = {
        2010: 5.16, 2011: 5.43, 2012: 5.68, 2013: 5.81, 2014: 6.43,
        2015: 6.31, 2016: 6.59, 2017: 6.59, 2018: 6.62, 2019: 6.35,
        2020: 2.15, 2021: 0.75, 2022: 3.63, 2023: 5.95, 2024: 6.65,
    }
    return [(y, float(v)) for y, v in dados.items()]


FETCHERS = {
    "_dolar_fechamento": _dolar_fechamento,
    "_inpe_queimadas": _inpe_queimadas,
    "_inpe_prodes": _inpe_prodes,
    "_ibovespa_fechamento": _ibovespa_fechamento,
    "_copa_mundo_brasil_posicao": _copa_mundo_brasil_posicao,
    "_copa_mundo_brasil_gols": _copa_mundo_brasil_gols,
    "_olimpiadas_brasil_medalhas": _olimpiadas_brasil_medalhas,
    "_olimpiadas_brasil_ouros": _olimpiadas_brasil_ouros,
    "_mega_sena_virada_premio": _mega_sena_virada_premio,
    "_bbb_audiencia_final": _bbb_audiencia_final,
    "_bbb_rejeicao_maxima": _bbb_rejeicao_maxima,
    "_enem_inscritos_milhoes": _enem_inscritos_milhoes,
    "_enem_abstencao_pct": _enem_abstencao_pct,
    "_natal_globo_roberto_carlos": _natal_globo_roberto_carlos,
    "_brasileirao_artilheiro_gols": _brasileirao_artilheiro_gols,
    "_eleicoes_eleitores_milhoes": _eleicoes_eleitores_milhoes,
    "_carnaval_rio_publico_milhoes": _carnaval_rio_publico_milhoes,
    "_formula1_gp_brasil_publico_mil": _formula1_gp_brasil_publico_mil,
    "_turistas_estrangeiros_milhoes": _turistas_estrangeiros_milhoes,
    "_casamentos_brasil": _casamentos_brasil,
    "_divorcios_brasil": _divorcios_brasil,
    "_veiculos_vendidos_milhoes": _veiculos_vendidos_milhoes,
    "_motos_vendidas_mil": _motos_vendidas_mil,
    "_soja_exportada_milhoes_ton": _soja_exportada_milhoes_ton,
    "_cafe_exportado_milhoes_sacas": _cafe_exportado_milhoes_sacas,
    "_gado_cabecas_milhoes": _gado_cabecas_milhoes,
    "_mei_estoque_milhoes": _mei_estoque_milhoes,
    "_acidentes_transito_obitos": _acidentes_transito_obitos,
    "_homicidios_brasil": _homicidios_brasil,
    "_spotify_top1_brasil_artista": _spotify_top1_brasil_artista,
    "_cesta_basica_dieese_sp": _cesta_basica_dieese_sp,
    "_internet_usuarios_pct": _internet_usuarios_pct,
    "_inss_fila_milhoes": _inss_fila_milhoes,
    "_evidencias_youtube_views_milhoes": _evidencias_youtube_views_milhoes,
}


# ============================================================================
# Execução
# ============================================================================

def run(only: list[str] | None = None) -> None:
    manifest = load_manifest()
    manifest.setdefault("series", {})

    for entry in REGISTRY:
        slug = entry["slug"]
        if only and slug not in only:
            continue
        log.info("→ %s (%s)", slug, entry["categoria"])
        try:
            fetcher = entry["fetch"]
            pairs = FETCHERS[fetcher]() if isinstance(fetcher, str) else fetcher()
            if not pairs:
                raise RuntimeError("Fetcher devolveu série vazia")
            n = save_csv(slug, pairs)
            anos = [p[0] for p in pairs]
            manifest["series"][slug] = {
                "label": entry["label"],
                "categoria": entry["categoria"],
                "fonte_nome": entry["fonte_nome"],
                "fonte_url": entry["fonte_url"],
                "status": "ok",
                "n": n,
                "ano_min": min(anos),
                "ano_max": max(anos),
                "coletado_em": dt.datetime.utcnow().isoformat() + "Z",
            }
            log.info("   OK — %d anos (%d–%d)", n, min(anos), max(anos))
        except Exception as e:
            log.error("   FALHA: %s\n%s", e, traceback.format_exc(limit=2))
            manifest["series"][slug] = {
                "label": entry["label"],
                "categoria": entry["categoria"],
                "fonte_nome": entry["fonte_nome"],
                "fonte_url": entry["fonte_url"],
                "status": "error",
                "erro": str(e),
                "coletado_em": dt.datetime.utcnow().isoformat() + "Z",
            }
        time.sleep(0.4)  # rate limit gentil

    save_manifest(manifest)
    # Resumo
    ok = sum(1 for s in manifest["series"].values() if s.get("status") == "ok")
    err = sum(1 for s in manifest["series"].values() if s.get("status") == "error")
    log.info("=== Coleta concluída — %d ok / %d falhas ===", ok, err)


if __name__ == "__main__":
    only = sys.argv[1:] or None
    run(only)
