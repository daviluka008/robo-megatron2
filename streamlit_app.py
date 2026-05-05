import streamlit as st

st.set_page_config(page_title="Megatron Show", page_icon="🤖", layout="wide")

# =========================================
# ESTADO
# =========================================

if "energia" not in st.session_state:
    st.session_state.energia = 0

if "ativo" not in st.session_state:
    st.session_state.ativo = False

# =========================================
# TÍTULO
# =========================================

st.title("🎉🤖 Megatron Kronos - Show de Robôs")

# =========================================
# FUNÇÃO SEGURA PRA IMAGEM
# =========================================

def mostrar_imagem(caminho):
    try:
        st.image(caminho, use_container_width=True)
    except:
        st.warning(f"Erro ao carregar imagem: {caminho}")

# =========================================
# IMAGEM INICIAL
# =========================================

if not st.session_state.ativo:
    mostrar_imagem("robo1.png")

# =========================================
# CONTROLES
# =========================================

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ Iniciar Evento"):
        st.session_state.ativo = True
        st.session_state.energia = 20

with col2:
    if st.button("🤖 Ativar Robôs"):
        if st.session_state.ativo:
            st.session_state.energia += 30
        else:
            st.warning("Inicie o evento primeiro")

with col3:
    if st.button("🎉 Modo Festa Máxima"):
        if st.session_state.ativo:
            st.session_state.energia += 40

# =========================================
# SHOW
# =========================================

if st.session_state.ativo:

    st.subheader("🔥 Show em andamento")

    colA, colB = st.columns(2)

    with colA:
        mostrar_imagem("robo1.png")

    with colB:
        mostrar_imagem("robo2.png")

    st.success("🤖 Robôs Megatron dominando a pista!")
    st.info("💃 Coreografia sincronizada")
    st.info("🎧 DJ elevando a energia")
    st.info("✨ Luzes em modo espetáculo")

# =========================================
# ENERGIA
# =========================================

st.subheader("📊 Energia do Evento")

energia = st.session_state.energia

st.progress(min(energia / 100, 1.0))
st.write(f"🔥 Energia: {energia}/100")

# =========================================
# STATUS FINAL
# =========================================

if energia >= 100:
    st.success("🚀 EVENTO INSANO! PÚBLICO EM ÊXTASE 🔥🤯")
elif energia >= 60:
    st.info("🎉 Festa bombando!")
elif energia > 0:
    st.warning("🎵 Festa começando...")
else:
    st.write("⏳ Evento parado")
