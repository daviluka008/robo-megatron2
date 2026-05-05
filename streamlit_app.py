import streamlit as st
from datetime import date

st.set_page_config(page_title="Sistema de Eventos", page_icon="📋")

st.title("📋 Controle de Eventos - Megatron")

# =========================
# BANCO SIMPLES (memória)
# =========================

if "eventos" not in st.session_state:
    st.session_state.eventos = []

# =========================
# CADASTRO
# =========================

st.header("➕ Novo Evento")

with st.form("form_evento"):
    nome = st.text_input("Nome do cliente")
    data_evento = st.date_input("Data do evento", min_value=date.today())

    tipo = st.selectbox("Tipo de evento", [
        "Casamento", "Festa", "15 anos", "Balada", "Outro"
    ])

    st.write("Serviços contratados:")

    robo = st.checkbox("🤖 Robô")
    tambor = st.checkbox("🥁 Tambor LED")
    pista = st.checkbox("💃 Pista Paris")
    letras = st.checkbox("🔠 Letras luminosas")
    plataforma = st.checkbox("🎥 Plataforma 360")

    salvar = st.form_submit_button("Salvar evento")

    if salvar:
        evento = {
            "nome": nome,
            "data": data_evento,
            "tipo": tipo,
            "servicos": {
                "robo": robo,
                "tambor": tambor,
                "pista": pista,
                "letras": letras,
                "plataforma": plataforma
            }
        }

        st.session_state.eventos.append(evento)
        st.success("Evento cadastrado!")

# =========================
# LISTA DE EVENTOS
# =========================

st.header("📅 Agenda de Eventos")

if not st.session_state.eventos:
    st.info("Nenhum evento cadastrado")
else:
    for i, evento in enumerate(st.session_state.eventos):

        st.subheader(f"{evento['nome']} - {evento['data']}")

        st.write(f"Tipo: {evento['tipo']}")

        # ALERTA
        if evento["data"] == date.today():
            st.error("🚨 EVENTO HOJE!")
        elif (evento["data"] - date.today()).days == 1:
            st.warning("⚠️ Evento amanhã")

        # CHECKLIST
        st.write("📦 Checklist:")

        if evento["servicos"]["robo"]:
            st.write("✔ Levar robô")

        if evento["servicos"]["tambor"]:
            st.write("✔ Levar tambor LED")

        if evento["servicos"]["pista"]:
            st.write("✔ Levar pista Paris")

        if evento["servicos"]["letras"]:
            st.write("✔ Levar letras luminosas")

        if evento["servicos"]["plataforma"]:
            st.write("✔ Levar plataforma 360")

        st.divider()
