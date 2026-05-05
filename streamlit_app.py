import streamlit as st
from datetime import date
import json
import os

st.set_page_config(page_title="Sistema de Eventos", page_icon="📋")

st.title("📋 Controle de Eventos - Megatron")

# =========================
# ARQUIVOS
# =========================

ARQUIVO_EVENTOS = "eventos.json"
ARQUIVO_CONFIG = "config.json"

# =========================
# FUNÇÕES
# =========================

def carregar_dados(arquivo, padrao):
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            return json.load(f)
    return padrao

def salvar_dados(arquivo, dados):
    with open(arquivo, "w") as f:
        json.dump(dados, f)

# =========================
# CONFIG (PREÇOS)
# =========================

config_padrao = {
    "robo": 1200,
    "extra": 800,
    "tambor": 2800,
    "combo": 3000,
    "pista": 4000,
    "plataforma": 2500,
    "letra": 200
}

config = carregar_dados(ARQUIVO_CONFIG, config_padrao)

st.sidebar.header("⚙️ Configurar preços")

config["robo"] = st.sidebar.number_input("Robô", value=config["robo"])
config["extra"] = st.sidebar.number_input("Robô adicional", value=config["extra"])
config["tambor"] = st.sidebar.number_input("Tambor", value=config["tambor"])
config["combo"] = st.sidebar.number_input("Combo", value=config["combo"])
config["pista"] = st.sidebar.number_input("Pista", value=config["pista"])
config["plataforma"] = st.sidebar.number_input("Plataforma", value=config["plataforma"])
config["letra"] = st.sidebar.number_input("Letra", value=config["letra"])

if st.sidebar.button("💾 Salvar preços"):
    salvar_dados(ARQUIVO_CONFIG, config)
    st.sidebar.success("Preços salvos!")

# =========================
# EVENTOS
# =========================

if "eventos" not in st.session_state:
    st.session_state.eventos = carregar_dados(ARQUIVO_EVENTOS, [])

# =========================
# CADASTRO
# =========================

st.header("➕ Novo Evento")

with st.form("form_evento"):
    nome = st.text_input("Nome do cliente")

    data_evento = st.date_input(
        "Data do evento",
        min_value=date.today(),
        format="DD/MM/YYYY"
    )

    tipo = st.selectbox("Tipo de evento", [
        "Casamento", "Festa", "15 anos", "Balada", "Outro"
    ])

    st.write("🤖 Escolha os robôs:")

    robos = st.multiselect(
        "Selecione os robôs",
        ["Megatron", "Bumblebee", "Tequileiro"]
    )

    tambor = st.checkbox("🥁 Tambor LED")
    pista = st.checkbox("💃 Pista Paris")
    plataforma = st.checkbox("🎥 Plataforma 360")

    letras = st.checkbox("🔠 Letras luminosas")
    qtd_letras = 0

    if letras:
        qtd_letras = st.number_input("Quantidade de letras", min_value=1, step=1)

    salvar = st.form_submit_button("Salvar evento")

    if salvar:

        total = 0
        qtd_robos = len(robos)

        # ROBÔS
        valor_robos = 0

        if qtd_robos == 1:
            valor_robos = config["robo"]
        elif qtd_robos > 1:
            valor_robos = config["robo"] + (qtd_robos - 1) * config["extra"]

        # COMBO
        if qtd_robos >= 1 and tambor:
            total += config["combo"]

            if qtd_robos > 1:
                total += (qtd_robos - 1) * config["extra"]
        else:
            total += valor_robos

            if tambor:
                total += config["tambor"]

        # OUTROS
        if pista:
            total += config["pista"]

        if plataforma:
            total += config["plataforma"]

        if letras:
            total += qtd_letras * config["letra"]

        evento = {
            "nome": nome,
            "data": data_evento.strftime("%Y-%m-%d"),
            "tipo": tipo,
            "total": total,
            "robos": robos,
            "letras": qtd_letras if letras else 0
        }

        st.session_state.eventos.append(evento)
        salvar_dados(ARQUIVO_EVENTOS, st.session_state.eventos)

        st.success(f"Evento cadastrado! 💰 Total: R$ {total}")

# =========================
# LISTA
# =========================

st.header("📅 Agenda de Eventos")

if not st.session_state.eventos:
    st.info("Nenhum evento cadastrado")
else:
    for evento in st.session_state.eventos:

        data_formatada = date.fromisoformat(evento["data"]).strftime("%d/%m/%Y")

        st.subheader(f"{evento['nome']} - {data_formatada}")

        st.write(f"Tipo: {evento['tipo']}")

        if evento["robos"]:
            st.write(f"🤖 Robôs ({len(evento['robos'])}): {', '.join(evento['robos'])}")

        data_evento = date.fromisoformat(evento["data"])

        if data_evento == date.today():
            st.error("🚨 EVENTO HOJE!")
        elif (data_evento - date.today()).days == 1:
            st.warning("⚠️ Evento amanhã")

        if evento["letras"] > 0:
            st.write(f"🔠 Letras: {evento['letras']}")

        st.success(f"💰 Total do evento: R$ {evento['total']}")

        st.divider()
        
