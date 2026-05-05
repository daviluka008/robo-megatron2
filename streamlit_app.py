import streamlit as st
import time

# =========================================
# 🎉 CONFIG
# =========================================

st.set_page_config(page_title="🎉 Megatron Control", page_icon="🤖")

st.title("🎉🤖 Painel de Controle - Megatron Eventos")

# =========================================
# 📊 ESTADO DO EVENTO
# =========================================

if "energia" not in st.session_state:
    st.session_state.energia = 0

if "ativo" not in st.session_state:
    st.session_state.ativo = False

# =========================================
# 🎛️ CONTROLES DO EVENTO
# =========================================

evento = st.selectbox(
    "🎉 Tipo de evento",
    ["Aniversário", "Casamento", "Formatura", "Festa Infantil"]
)

nivel = st.slider("🔥 Intensidade da festa", 1, 10, 5)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ Iniciar festa"):
        st.session_state.ativo = True
        st.session_state.energia = 10

with col2:
    if st.button("🤖 Ativar robôs"):
        if st.session_state.ativo:
            st.session_state.energia += 25
        else:
            st.warning("Inicie o evento primeiro")

with col3:
    if st.button("🎉 Boost de energia"):
        if st.session_state.ativo:
            st.session_state.energia += 15

# =========================================
# 🤖 ROBÔS EM AÇÃO
# =========================================

if st.session_state.ativo:

    st.subheader("🤖 Show dos Robôs")

    st.write("🤖 Megatron entrou na pista!")
    st.write("💃 Robô dançarino ativado!")
    st.write("🎤 Robô animador chamando o público!")
    st.write("✨ Luzes sincronizadas com a música!")

# =========================================
# 📊 ENERGIA DA FESTA
# =========================================

st.subheader("📊 Energia do evento")

energia = st.session_state.energia

st.progress(min(energia / 100, 1.0))

st.write(f"🔥 Energia atual: {energia}/100")

# =========================================
# 🎉 STATUS FINAL
# =========================================

if energia >= 100:
    st.success("🎉 FESTA NO MÁXIMO! PÚBLICO EM ÊXTASE 🤯🔥")
elif energia >= 60:
    st.info("🎊 Festa muito animada!")
elif energia > 0:
    st.warning("🎵 Festa começando...")
else:
    st.write("⏳ Evento parado")
