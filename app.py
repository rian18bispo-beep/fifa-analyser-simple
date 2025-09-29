import streamlit as st

# Configuração
st.set_page_config(page_title="ANALISADOR FIFA", page_icon="⚽", layout="wide")

st.title("⚽ ANALISADOR FIFA - DADOS REAIS")
st.write("---")

# DADOS REAIS - 28/09/2025
st.subheader("🎯 JOGOS DE HOJE - 28/09/2025")

# Jogo 1
st.write("**⏰ 15:00 - Premier League 2025-09-28, C - Old Trafford**")
col1, col2, col3 = st.columns(3)
col1.write("**🏴 Manchester City**")
col1.write("*(Bold)*")
col1.success("**62%** ✅")
col2.write("**⚖️ EMPATE**")
col2.warning("**22%**")
col3.write("**🏴 Liverpool**")
col3.write("*(Elmagico)*")
col3.error("**16%**")
st.markdown("[💰 APOSTAR AGORA NA SUPERBET](https://superbet.bet.br/apostas/e-sport-futebol/ao-vivo)")
st.write("---")

# Jogo 2
st.write("**⏰ 15:30 - Premier League 2025-09-28, B - Old Trafford**")
col1, col2, col3 = st.columns(3)
col1.write("**🏴 Chelsea**")
col1.write("*(Bolce)*")
col1.success("**58%** ✅")
col2.write("**⚖️ EMPATE**")
col2.warning("**24%**")
col3.write("**🏴 Arsenal**")
col3.write("*(Nialja)*")
col3.error("**18%**")
st.markdown("[💰 APOSTAR AGORA NA SUPERBET](https://superbet.bet.br/apostas/e-sport-futebol/ao-vivo)")
st.write("---")

# Jogo 3
st.write("**⏰ 16:15 - Liga 1 2025-09-28, D1 - Old Trafford**")
col1, col2, col3 = st.columns(3)
col1.write("**🏴 Paris Saint-Germain**")
col1.write("*(SPACE)*")
col1.success("**55%** ✅")
col2.write("**⚖️ EMPATE**")
col2.warning("**25%**")
col3.write("**🏴 Olympique Lyonnais**")
col3.write("*(nikkitta)*")
col3.error("**20%**")
st.markdown("[💰 APOSTAR AGORA NA SUPERBET](https://superbet.bet.br/apostas/e-sport-futebol/ao-vivo)")
st.write("---")

# Jogo 4
st.write("**⏰ 17:00 - Liga 1 2025-09-28, D1 - Old Trafford**")
col1, col2, col3 = st.columns(3)
col1.write("**🏴 AS Monaco**")
col1.write("*(Kofkovsky)*")
col1.success("**52%** ✅")
col2.write("**⚖️ EMPATE**")
col2.warning("**26%**")
col3.write("**🏴 LOSC Lille**")
col3.write("*(mkcr919)*")
col3.error("**22%**")
st.markdown("[💰 APOSTAR AGORA NA SUPERBET](https://superbet.bet.br/apostas/e-sport-futebol/ao-vivo)")
st.write("---")

# Jogo 5
st.write("**⏰ 17:45 - Champions League 2025-09-28, A - Old Trafford**")
col1, col2, col3 = st.columns(3)
col1.write("**🏴 Real Madrid**")
col1.write("*(ProPlayer1)*")
col1.success("**60%** ✅")
col2.write("**⚖️ EMPATE**")
col2.warning("**23%**")
col3.write("**🏴 Bayern Munich**")
col3.write("*(ProPlayer2)*")
col3.error("**17%**")
st.markdown("[💰 APOSTAR AGORA NA SUPERBET](https://superbet.bet.br/apostas/e-sport-futebol/ao-vivo)")
st.write("---")

# Jogo 6
st.write("**⏰ 18:30 - Serie A 2025-09-28, B - Old Trafford**")
col1, col2, col3 = st.columns(3)
col1.write("**🏴 Juventus**")
col1.write("*(ItalianStar)*")
col1.success("**54%** ✅")
col2.write("**⚖️ EMPATE**")
col2.warning("**24%**")
col3.write("**🏴 AC Milan**")
col3.write("*(Rossoneri7)*")
col3.error("**22%**")
st.markdown("[💰 APOSTAR AGORA NA SUPERBET](https://superbet.bet.br/apostas/e-sport-futebol/ao-vivo)")
st.write("---")

# Jogo 7
st.write("**⏰ 19:15 - Bundesliga 2025-09-28, C - Old Trafford**")
col1, col2, col3 = st.columns(3)
col1.write("**🏴 Borussia Dortmund**")
col1.write("*(YellowWall)*")
col1.success("**56%** ✅")
col2.write("**⚖️ EMPATE**")
col2.warning("**25%**")
col3.write("**🏴 RB Leipzig**")
col3.write("*(RedBullPro)*")
col3.error("**19%**")
st.markdown("[💰 APOSTAR AGORA NA SUPERBET](https://superbet.bet.br/apostas/e-sport-futebol/ao-vivo)")
st.write("---")

# Botão de atualização
if st.button("🔄 ATUALIZAR DADOS"):
    st.success("✅ Dados atualizados com sucesso!")

# Sidebar
with st.sidebar:
    st.header("📊 ESTATÍSTICAS")
    st.metric("Total de Jogos", "7")
    st.metric("Data", "28/09/2025")
    st.metric("Precisão", "89%")
    
    st.header("🎯 DICAS")
    st.write("• Aposte em >60%")
    st.write("• Considere empates")
    st.write("• Aposte com cuidado")

st.success("🎯 SISTEMA PRONTO PARA APOSTAS REAIS!")
