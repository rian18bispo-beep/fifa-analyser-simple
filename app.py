import streamlit as st, requests, pandas as pd, datetime as dt, math
from bs4 import BeautifulSoup

# ---------- ELO INLINE ----------
K = 32
def rate_1vs1(rA, rB):
    EA = 1/(1+10**((rB-rA)/400))
    EB = 1 - EA
    return rA + K*(1 - EA), rB + K*(0 - EB)
# --------------------------------

st.set_page_config(page_title="Old Trafford Analyzer", layout="wide")
st.markdown("""
<style>
.block-container{padding-top:1rem;}
.stButton>button{width:100%; background-color:#0e4b99; color:white; font-weight:bold;}
</style>
""", unsafe_allow_html=True)

API_BASE = "https://football.esportsbattle.com/en/tournament"
TOUR_IDS = [224741,224735,224737,224739,224742,224743,224744]
SUPERBET = "https://superbet.bet.br/apostas/e-sport-futebol/ao-vivo"

@st.cache_data(ttl=60)
def fetch_page(tour_id):
    url = f"{API_BASE}/{tour_id}"
    r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
    return BeautifulSoup(r.text, "lxml")

@st.cache_data(ttl=60)
def get_matches():
    rows = []
    for tid in TOUR_IDS:
        soup = fetch_page(tid)
        tor = soup.select_one("h1.tournament-title").text.strip()
        for card in soup.select("div.match-card"):
            if "scheduled" not in card.select_one("div.match-status").text.lower(): continue
            t = card.select_one("div.match-time").text.strip()
            p1, p2 = [x.text.strip() for x in card.select("div.team-name")]
            rows.append({"tor":tor, "time":t, "p1":p1, "p2":p2})
    return pd.DataFrame(rows)

@st.cache_data(ttl=300)
def build_elo():
    hist_ids = [224247,224241,224243,224245,224248,224249,224250,
                224341,224322,224327,224335,224354,224358,224361,
                224405,224399,224401,224403,224406,224407,224408,
                224488,224482,224484,224486,224489,224490,224491,
                224561,224555,224557,224559,224562,224563,224564,
                224660,224641,224646,224654,224673,224677,224680]
    elo = {}
    for tid in hist_ids:
        soup = fetch_page(tid)
        for card in soup.select("div.match-card"):
            try:
                g1, g2 = map(int, card.select_one("div.match-score").text.strip().split("-"))
                t1, t2 = [x.text.strip() for x in card.select("div.team-name")]
                rA, rB = rate_1vs1(elo.get(t1,1500), elo.get(t2,1500))
                if g1>g2:   elo[t1], elo[t2] = rA, rB
                elif g1<g2: elo[t1], elo[t2] = rB, rA
            except: pass
    return elo

def probs(p1, p2, elo):
    e1, e2 = elo.get(p1,1500), elo.get(p2,1500)
    pwin = 1/(1+10**((e2-e1)/400))
    pdraw = 0.5 - abs(pwin - 0.5)*0.4
    pwin2 = 1 - pwin - pdraw
    return max(0,round(pwin*100)), max(0,round(pdraw*100)), max(0,round(pwin2*100))

st.title("🏟️ Analisador FIFA – Old Trafford")
st.markdown(f"[🔗 Apostar agora na SuperBet]({SUPERBET})", unsafe_allow_html=True)

if st.button("🔄 Atualizar dados ao vivo"):
    st.cache_data.clear()

df = get_matches()
elo = build_elo()

if df.empty:
    st.warning("Nenhuma partida agendada encontrada.")
else:
    for _,r in df.iterrows():
        w,d,l = probs(r.p1, r.p2, elo)
        st.markdown(f"**⏰ {r.time} – {r.tor}**  
🏴 **{r.p1}**: {w}% ✅ ⚖️ EMPATE: {d}% 🏴 **{r.p2}**: {l}%")
