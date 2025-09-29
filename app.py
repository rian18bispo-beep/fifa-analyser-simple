import streamlit as st

st.title("⚽ ANALISADOR FIFA")
st.write("✅ SISTEMA FUNCIONANDO!")

st.write("---")
st.write("**JOGOS DE HOJE - 26/09/2025**")

# Jogo 1
st.write("⏰ 15:00 - Premier League")
col1, col2, col3 = st.columns(3)
col1.write("Man City (Bold)")
col1.success("58%")
col2.write("EMPATE") 
col2.warning("25%")
col3.write("Liverpool (Elmagico)")
col3.error("17%")

st.write("---")
st.markdown("[💰 APOSTAR NA SUPERBET](https://superbet.bet.br)")

st.success("🎯 PRONTO PARA APOSTAS!")
