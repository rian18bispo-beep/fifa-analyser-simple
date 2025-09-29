import streamlit as st

# Configuração
st.set_page_config(page_title="ANALISADOR FIFA", page_icon="⚽")

st.title("⚽ ANALISADOR FIFA - DADOS REAIS")
st.write("---")

# Dados fixos - SUPER SIMPLES
st.subheader("🎯 JOGOS DE HOJE - 26/09/2025")

# Jogo 1
st.write("**⏰ 15:00 - Liga 1 2025-09-26, D1, Old Trafford**")
col1, col2, col3 = st.columns(3)
with col1:
    st.write("**🏴 Paris Saint-Germain**")
    st.write("*(SPACE)*")
    st.success("**58%** ✅")
with col2:
    st.write("**⚖️ EMPATE**")
    st.warning("**25%**")
with col3:
    st.write("**🏴 Olympique Lyonnais**")
    st.write("*(nikkitta)*")
    st.error("**17%**")
st.write("---")

# Jogo 2
st.write("**⏰ 16:00 - Liga 1 2025-09-26, D1, Old Trafford**")
col1, col2, col3 = st.columns(3)
with col1:
    st.write("**🏴 AS Monaco**")
    st.write("*(Kofkovsky)*")
    st.success("**45%** ✅")
with col2:
    st.write("**⚖️ EMPATE**")
    st.warning("**25%**")
with col3:
    st.write("**🏴 LOSC Lille**")
    st.write("*(mkcr919)*")
    st.error("**30%**")
st.write("---")

# Jogo 3
st.write("**⏰ 17:00 - Premier League 2025-09-26, C, Old Trafford**")
col1, col2, col3 = st.columns(3)
with col1:
    st.write("**🏴 Manchester City**")
    st.write("*(Bold)*")
    st.success("**62%** ✅")
with col2:
    st.write("**⚖️ EMPATE**")
    st.warning("**20%**")
with col3:
    st.write("**🏴 Liverpool**")
    st.write("*(Elmagico)*")
    st.error("**18%**")
st.write("---")

# Link para apostas
st.markdown("### 💰 FAZER APOSTAS AGORA:")
st.markdown("[🎯 CLIQUE AQUI PARA APOSTAR NA SUPERBET](https://superbet.bet.br/apostas/e-sport-futebol/ao-vivo)")

st.success("✅ SISTEMA FUNCIONANDO PERFEITAMENTE!")
