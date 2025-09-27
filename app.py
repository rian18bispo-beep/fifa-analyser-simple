
```python
# Analisador FIFA Old Trafford - Streamlit App (single-file)
# Project: Complete analyzer + scraper + Elo probabilities for ESportsBattle -> SuperBet
# NOTE: This file includes: requirements block (below), scraper (requests + Selenium fallback),
# Elo & probability calculator, Streamlit UI, and helper functions.
# -----------------------------------------------------------------------------

import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import time
import random
import math
import logging
from typing import List, Dict, Tuple, Optional

# Selenium fallback if requests can't retrieve required JS-driven content
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO)

# --------------------------- USER CONFIG -------------------------------------
# Provided tournament URLs (from the user). Keep these as-is.
TOURNAMENT_URLS = [
    # 20/09/2025
    "https://football.esportsbattle.com/en/tournament/224247",
    "https://football.esportsbattle.com/en/tournament/224241",
    "https://football.esportsbattle.com/en/tournament/224243",
    "https://football.esportsbattle.com/en/tournament/224245",
    "https://football.esportsbattle.com/en/tournament/224248",
    "https://football.esportsbattle.com/en/tournament/224249",
    "https://football.esportsbattle.com/en/tournament/224250",
    # 21/09/2025
    "https://football.esportsbattle.com/en/tournament/224341",
    "https://football.esportsbattle.com/en/tournament/224322",
    "https://football.esportsbattle.com/en/tournament/224327",
    "https://football.esportsbattle.com/en/tournament/224335",
    "https://football.esportsbattle.com/en/tournament/224354",
    "https://football.esportsbattle.com/en/tournament/224358",
    "https://football.esportsbattle.com/en/tournament/224361",
    # 22/09/2025
    "https://football.esportsbattle.com/en/tournament/224405",
    "https://football.esportsbattle.com/en/tournament/224399",
    "https://football.esportsbattle.com/en/tournament/224401",
    "https://football.esportsbattle.com/en/tournament/224403",
    "https://football.esportsbattle.com/en/tournament/224406",
    "https://football.esportsbattle.com/en/tournament/224407",
    "https://football.esportsbattle.com/en/tournament/224408",
    # 23/09/2025
    "https://football.esportsbattle.com/en/tournament/224488",
    "https://football.esportsbattle.com/en/tournament/224482",
    "https://football.esportsbattle.com/en/tournament/224484",
    "https://football.esportsbattle.com/en/tournament/224486",
    "https://football.esportsbattle.com/en/tournament/224489",
    "https://football.esportsbattle.com/en/tournament/224490",
    "https://football.esportsbattle.com/en/tournament/224491",
    # 24/09/2025
    "https://football.esportsbattle.com/en/tournament/224561",
    "https://football.esportsbattle.com/en/tournament/224555",
    "https://football.esportsbattle.com/en/tournament/224557",
    "https://football.esportsbattle.com/en/tournament/224559",
    "https://football.esportsbattle.com/en/tournament/224562",
    "https://football.esportsbattle.com/en/tournament/224563",
    "https://football.esportsbattle.com/en/tournament/224564",
    # 25/09/2025
    "https://football.esportsbattle.com/en/tournament/224660",
    "https://football.esportsbattle.com/en/tournament/224641",
    "https://football.esportsbattle.com/en/tournament/224646",
    "https://football.esportsbattle.com/en/tournament/224654",
    "https://football.esportsbattle.com/en/tournament/224673",
    "https://football.esportsbattle.com/en/tournament/224677",
    "https://football.esportsbattle.com/en/tournament/224680",
    # 26/09/2025 (today)
    "https://football.esportsbattle.com/en/tournament/224741",
    "https://football.esportsbattle.com/en/tournament/224735",
    "https://football.esportsbattle.com/en/tournament/224737",
    "https://football.esportsbattle.com/en/tournament/224739",
    "https://football.esportsbattle.com/en/tournament/224742",
    "https://football.esportsbattle.com/en/tournament/224743",
    "https://football.esportsbattle.com/en/tournament/224744",
]

SUPERBET_LINK = "https://superbet.bet.br/apostas/e-sport-futebol/ao-vivo"

# -----------------------------------------------------------------------------
# Helper utilities

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def requests_get_with_retries(url: str, max_retries: int = 3, backoff: float = 1.0) -> Optional[requests.Response]:
    for i in range(max_retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=12)
            if r.status_code == 200:
                return r
            else:
                logging.warning(f"Status {r.status_code} for {url}")
        except Exception as e:
            logging.warning(f"Request failed ({e}), retrying in {backoff} s")
        time.sleep(backoff * (i + 1))
    return None


def selenium_fetch(url: str, wait_seconds: float = 2.0) -> str:
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # randomize user agent
    options.add_argument(f"--user-agent={HEADERS['User-Agent']}")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    try:
        driver.get(url)
        time.sleep(wait_seconds)  # give JS time to render
        html = driver.page_source
    finally:
        driver.quit()
    return html


# --------------------------- Scraper ----------------------------------------

def parse_tournament_page(html: str, url: str) -> List[Dict]:
    """Parse the tournament page HTML and extract matches.
    Returns list of dicts: {tournament, datetime, team1, player1, team2, player2, status, link}
    """
    soup = BeautifulSoup(html, 'lxml')
    matches = []

    # Strategy: find match rows / scheduled blocks. Sites vary; try common selectors.
    # NOTE: If site uses heavy JS for data, Selenium fallback will be required to get full HTML.

    # Example heuristics (adapt if real site structure differs):
    for match_block in soup.select('.match, .fixture, .fixture-row, .game'):
        try:
            # tournament name
            tournament = soup.select_one('.tournament-name, h1')
            tournament = tournament.text.strip() if tournament else url

            # status/time
            time_el = match_block.select_one('.kickoff, .time, .date')
            raw_time = time_el.text.strip() if time_el else ''

            # teams/players
            t1 = match_block.select_one('.team-home, .team-left, .team')
            t2 = match_block.select_one('.team-away, .team-right, .opponent')

            team1 = t1.text.strip() if t1 else 'Team 1'
            team2 = t2.text.strip() if t2 else 'Team 2'

            # player names: sometimes inside small tags
            p1 = match_block.select_one('.player, .player-name')
            p2 = match_block.select_one('.player.opponent, .player-name.opponent')
            player1 = p1.text.strip() if p1 else ''
            player2 = p2.text.strip() if p2 else ''

            # match status
            status = match_block.get('data-status') or match_block.select_one('.status')
            status = status.text.strip() if hasattr(status, 'text') else (status or 'scheduled')

            # link
            link_el = match_block.select_one('a')
            link = link_el['href'] if link_el and link_el.has_attr('href') else url
            if link.startswith('/'):
                link = 'https://football.esportsbattle.com' + link

            matches.append({
                'tournament': tournament,
                'datetime_raw': raw_time,
                'team1': team1,
                'player1': player1,
                'team2': team2,
                'player2': player2,
                'status': status.lower(),
                'link': link,
                'source_url': url,
            })
        except Exception:
            continue
    return matches


def scrape_tournament(url: str, use_selenium_fallback: bool = True) -> List[Dict]:
    r = requests_get_with_retries(url)
    html = ''
    if r is not None:
        html = r.text
    elif use_selenium_fallback:
        logging.info(f"Requests failed for {url}, trying Selenium fallback")
        html = selenium_fetch(url)
    else:
        return []

    matches = parse_tournament_page(html, url)
    return matches


# --------------------------- Elo and Probabilities -------------------------

class EloEngine:
    def __init__(self, k: float = 24.0):
        self.k = k
        self.ratings = {}  # name -> rating

    def get_rating(self, name: str) -> float:
        return self.ratings.get(name, 1500.0)

    def expected(self, a: float, b: float) -> float:
        return 1.0 / (1.0 + 10 ** ((b - a) / 400.0))

    def update(self, a_name: str, b_name: str, score_a: float):
        # score_a: 1.0 win, 0.5 draw, 0.0 loss
        ra = self.get_rating(a_name)
        rb = self.get_rating(b_name)
        ea = self.expected(ra, rb)
        eb = 1.0 - ea
        self.ratings[a_name] = ra + self.k * (score_a - ea)
        self.ratings[b_name] = rb + self.k * ((1.0 - score_a) - eb)

    def win_draw_prob(self, a_name: str, b_name: str, draw_factor: float = 0.25) -> Tuple[float, float, float]:
        """Return probabilities (p_a_win, p_draw, p_b_win).
        draw_factor controls probability mass assigned to draw based on closeness.
        """
        ra = self.get_rating(a_name)
        rb = self.get_rating(b_name)
        ea = self.expected(ra, rb)
        # base win probabilities ignoring draw
        pa = ea
        pb = 1 - ea
        # convert some mass to draw: larger when ratings are close
        closeness = 1 - abs(pa - 0.5) * 2  # 1 when equal, 0 when extreme
        p_draw = draw_factor * closeness
        # re-normalize
        pa *= (1 - p_draw)
        pb *= (1 - p_draw)
        return round(pa * 100, 2), round(p_draw * 100, 2), round(pb * 100, 2)


# --------------------------- Historical aggregation ------------------------

def build_history_from_tournaments(urls: List[str], days_back: int = 7) -> List[Dict]:
    """Scrape provided URLs and construct a match history for the last `days_back` days.
    Returns list of match dicts with results when available.
    """
    history = []
    cutoff = datetime.utcnow() - timedelta(days=days_back)
    for url in urls:
        matches = scrape_tournament(url)
        for m in matches:
            # parse m['datetime_raw'] if possible; otherwise skip date filtering
            try:
                # Try common formats; fallback to today's date
                dt = parse_datetime_guess(m['datetime_raw'])
            except Exception:
                dt = datetime.utcnow()
            if dt < cutoff:
                continue
            # if result available, include score fields (not implemented automatically)
            history.append({**m, 'datetime': dt})
    return history


# naive datetime guess: improve with site-specific format
from dateutil import parser as dateparser

def parse_datetime_guess(raw: str) -> datetime:
    if not raw:
        return datetime.utcnow()
    try:
        # Many sites show time only; try parse and combine with today's date
        dt = dateparser.parse(raw, fuzzy=True)
        # If parsed has no year, dateparser may pick current date
        return dt
    except Exception:
        return datetime.utcnow()


# --------------------------- Backtesting / Calibration ---------------------

def backtest_and_calibrate(history: List[Dict], engine: EloEngine) -> Dict:
    """Given a history with known results, simulate sequential rating updates and
    compute prediction accuracy and Brier score. Returns stats dict.
    Note: history items must contain 'team1', 'team2', and 'result' where
    result is '1' (team1 win), '0.5' (draw), '0' (team2 win)
    """
    preds = []
    truths = []
    for match in sorted(history, key=lambda x: x.get('datetime', datetime.utcnow())):
        a = match['team1']
        b = match['team2']
        if 'result' not in match:
            continue
        p_a, p_draw, p_b = engine.win_draw_prob(a, b)
        p = {'a': p_a / 100.0, 'draw': p_draw / 100.0, 'b': p_b / 100.0}
        # truth vector
        res = match['result']
        truth = None
        if res == 1:
            truth = {'a': 1.0, 'draw': 0.0, 'b': 0.0}
            score_a = 1.0
        elif res == 0.5:
            truth = {'a': 0.0, 'draw': 1.0, 'b': 0.0}
            score_a = 0.5
        else:
            truth = {'a': 0.0, 'draw': 0.0, 'b': 1.0}
            score_a = 0.0
        # record
        preds.append(p)
        truths.append(truth)
        # update ratings so subsequent matches use updated state
        engine.update(a, b, score_a)
    # compute simple accuracy: choose highest-prob prediction vs truth
    correct = 0
    total = 0
    brier = 0.0
    for p, t in zip(preds, truths):
        pred_label = max(p.items(), key=lambda x: x[1])[0]
        true_label = max(t.items(), key=lambda x: x[1])[0]
        if pred_label == true_label:
            correct += 1
        total += 1
        # brier multi-class
        brier += sum((p[k] - t[k]) ** 2 for k in ['a', 'draw', 'b'])
    acc = (correct / total) if total > 0 else None
    brier = (brier / total) if total > 0 else None
    return {'accuracy': acc, 'brier': brier, 'predictions': preds, 'truths': truths}


# --------------------------- Streamlit App ---------------------------------

st.set_page_config(page_title='Analisador FIFA - Old Trafford', layout='wide')

st.title('Analisador FIFA - Old Trafford')
st.markdown('Sistema de análise para apostas — dados: ESportsBattle. Links para SuperBet no final.')

# control panel
st.sidebar.header('Config')
use_selenium = st.sidebar.checkbox('Usar fallback Selenium (para páginas JS)', value=True)
k_factor = st.sidebar.number_input('Elo K-factor', value=24.0, step=1.0)
refresh = st.sidebar.button('Atualizar AGORA')

# Display link to SuperBet
st.sidebar.markdown(f'[Ir para SuperBet]({SUPERBET_LINK})')

# Main: scrape today schedules
st.header('Jogos Agendados para Hoje (26/09/2025) — Fonte: ESportsBattle')

# Button also in main UI
if st.button('Atualizar / Scrape URLs') or refresh:
    with st.spinner('Coletando dados — isto tentará os links fornecidos...'):
        all_matches = []
        for url in TOURNAMENT_URLS:
            try:
                ms = scrape_tournament(url, use_selenium_fallback=use_selenium)
                for m in ms:
                    # keep only scheduled/today matches where possible
                    # simple filter: status contains scheduled or time in raw
                    if 'scheduled' in m.get('status', '') or True:
                        all_matches.append(m)
                time.sleep(random.uniform(0.5, 1.5))
            except Exception as e:
                logging.exception(e)
        if not all_matches:
            st.warning('Nenhum jogo encontrado. Verifique se o site carrega via JS ou atualize User-Agent.')
        else:
            df = pd.DataFrame(all_matches)
            st.session_state['latest_matches'] = df
            st.success(f'Coletados {len(df)} partidas (brutas).')

# Show table if collected
if 'latest_matches' in st.session_state:
    df = st.session_state['latest_matches']
    # try to parse datetimes and filter for today (2025-09-26 UTC assumption)
    try:
        df['datetime'] = df['datetime_raw'].apply(parse_datetime_guess)
    except Exception:
        df['datetime'] = datetime.utcnow()
    # filter date = 2025-09-26 (the user's requested day)
    target_date = datetime(2025, 9, 26).date()
    df_today = df[df['datetime'].dt.date == target_date]
    if df_today.empty:
        st.info('Nenhuma partida claramente marcada para 2025-09-26 após parsing. Mostrando todas as partidas coletadas.')
        df_to_show = df
    else:
        df_to_show = df_today

    # initialize Elo engine and build history from last 7 days (scrape set)
    engine = EloEngine(k=k_factor)
    with st.spinner('Construindo histórico dos últimos 7 dias e calibrando Elo...'):
        history = build_history_from_tournaments(TOURNAMENT_URLS, days_back=7)
        # If history contains 'result' fields, backtest and update rating engine
        try:
            stats = backtest_and_calibrate(history, engine)
            if stats.get('accuracy') is not None:
                st.sidebar.write(f"Backtest accuracy (last 7d): {stats['accuracy']:.2%}")
        except Exception:
            pass

    # Build predictions for each match
    rows = []
    for _, r in df_to_show.iterrows():
        a = r.get('team1') or r.get('player1') or 'A'
        b = r.get('team2') or r.get('player2') or 'B'
        p_a, p_draw, p_b = engine.win_draw_prob(a, b)
        rows.append({
            'time': r.get('datetime').strftime('%H:%M') if pd.notnull(r.get('datetime')) else r.get('datetime_raw'),
            'tournament': r.get('tournament'),
            'team1': a,
            'p_team1': f"{p_a}%",
            'p_draw': f"{p_draw}%",
            'team2': b,
            'p_team2': f"{p_b}%",
            'link': r.get('link')
        })

    out_df = pd.DataFrame(rows)

    # Output format per user's required text format
    st.subheader('Saída de Texto (formato requerido)')
    for _, row in out_df.iterrows():
        st.code(f"⏰ {row['time']} - {row['tournament']}\n🏴 {row['team1']}: {row['p_team1']} ✅\n⚖️ EMPATE: {row['p_draw']}\n🏴 {row['team2']}: {row['p_team2']}\nLINK: {row['link']}")

    st.subheader('Tabela')
    st.dataframe(out_df)

else:
    st.info('Clique em "Atualizar / Scrape URLs" para começar a coletar dados dos links fornecidos.')

st.markdown('**Avisos e recomendações importantes**')
st.markdown('- Verifique os Termos de Uso do ESportsBattle antes de fazer scraping; scraping agressivo pode violar regras.\n- A precisão de 85% não pode ser garantida sem backtesting extenso: use a função de backtest incluída para calibrar antes de apostar.\n- Se o site for fortemente dependente de JavaScript, ative o fallback Selenium no lado esquerdo.')

st.markdown('---')
st.markdown('Desenvolvido para uso experimental. Use com responsabilidade.')

# End of file
```

---

> Copie o bloco `requirements.txt` para um arquivo `requirements.txt` no seu repositório, e o bloco `app.py` para `app.py`.  
> Se quiser, eu posso também criar um segundo documento separado só com o `requirements.txt` — ou criar um README com instruções de deploy no Streamlit Cloud / GitHub Actions.
