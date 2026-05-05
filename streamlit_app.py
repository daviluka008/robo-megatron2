import streamlit as st
from datetime import date

st.set_page_config(page_title="Sistema de Eventos", page_icon="📋")

st.title("📋 Controle de Eventos - Megatron")

# =========================
# BANCO
# =========================

if "eventos" not in st.session_state:
    st.session_state.eventos = []

# =========================
# TABELA DE PREÇOS
# =========================

precos = {
    "robo": 500,
    "tambor": 300,
    "pista": 400,
    "letras": 250,
    "plataforma": 600
}

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
        total = 0

        if robo:
            total += precos["robo"]
        if tambor:
            total += precos["tambor"]
        if pista:
            total += precos["pista"]
        if letras:
            total += precos["letras"]
        if plataforma:
            total += precos["plataforma"]

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
            },
            "total": total
        }

        st.session_state.eventos.append(evento)
        st.success(f"Evento cadastrado! 💰 Total: R$ {total}")

# =========================
# LISTA
# =========================

st.header("📅 Agenda de Eventos")

if not st.session_state.eventos:
    st.info("Nenhum evento cadastrado")
else:
    for evento in st.session_state.eventos:

        st.subheader(f"{evento['nome']} - {evento['data']}")

        st.write(f"Tipo: {evento['tipo']}")

        # ALERTA
        if evento["data"] == date.today():
            st.error("🚨 EVENTO HOJE!")
        elif (evento["data"] - date.today()).days == 1:
            st.warning("⚠️ Evento amanhã")

        # SERVIÇOS
        st.write("📦 Serviços:")
        for servico, ativo in evento["servicos"].items():
            if ativo:
                st.write(f"✔ {servico}")

        # VALOR
        st.success(f"💰 Total do evento: R$ {evento['total']}")

        st.divider()
