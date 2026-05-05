import streamlit as st

st.set_page_config(page_title="Megatron Show", page_icon="🤖")

st.title("🎉🤖 Megatron Show - Controle de Festa")

# =============================
# ESTADO
# =============================

if "energia" not in st.session_state:
    st.session_state.energia = 0

if "ativo" not in st.session_state:
    st.session_state.ativo = False

# =============================
# CONTROLES
# =============================

col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Iniciar Show"):
        st.session_state.ativo = True
        st.session_state.energia = 20

with col2:
    if st.button("🤖 Ativar Robô"):
        if st.session_state.ativo:
            st.session_state.energia += 30

# =============================
# VISUAL DO ROBÔ
# =============================

if st.session_state.ativo:

    st.subheader("🤖 Megatron em ação")

    # GIF (troca depois se quiser)
    st.image("https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif")

    st.write("🔥 Robô dançando com luzes!")
    st.write("🎉 Público animado!")

# =============================
# ENERGIA
# =============================

energia = st.session_state.energia

st.progress(min(energia / 100, 1.0))
st.write(f"🔥 Energia: {energia}/100")

if energia >= 100:
    st.success("🎉 FESTA EXPLODIU!")
