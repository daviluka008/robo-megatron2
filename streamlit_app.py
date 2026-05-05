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
        try:
            with open(arquivo, "r") as f:
                return json.load(f)
        except:
            return padrao
    return padrao

def salvar_dados(arquivo, dados):
    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)

# =========================
# CONFIG
# =========================

config_padrao = {
    "robo": 1200,
    "tambor": 2800,
    "combo": 3000,
    "pista": 4000,
    "plataforma": 2500,
    "letra": 200
}

config = carregar_dados(ARQUIVO_CONFIG, config_padrao)

st.sidebar.header("⚙️ Configurar preços")

config["robo"] = st.sidebar.number_input("Robô", value=config["robo"])
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
    endereco = st.text_input("Endereço do evento")
    cep = st.text_input("CEP")
    horario = st.time_input("Horário do evento")

    data_evento = st.date_input(
        "Data do evento",
        min_value=date.today(),
        format="DD/MM/YYYY"
    )

    tipo = st.selectbox("Tipo de evento", [
        "Casamento", "Festa", "15 anos", "Balada", "Outro"
    ])

    # ROBÔS
    st.write("🤖 Quantidade de cada robô (máx. 7)")

    qtd_megatron = st.number_input("Megatron", min_value=0, max_value=7)
    qtd_bumblebee = st.number_input("Bumblebee", min_value=0, max_value=7)
    qtd_tequileiro = st.number_input("Tequileiro", min_value=0, max_value=7)

    total_robos = qtd_megatron + qtd_bumblebee + qtd_tequileiro

    if total_robos > 7:
        st.error("Máximo de 7 robôs no total.")

    robos = (
        ["Megatron"] * qtd_megatron +
        ["Bumblebee"] * qtd_bumblebee +
        ["Tequileiro"] * qtd_tequileiro
    )

    # SERVIÇOS
    tambor = st.checkbox("🥁 Tambor LED")
    pista = st.checkbox("💃 Pista Paris")
    plataforma = st.checkbox("🎥 Plataforma 360")

    letras = st.checkbox("🔠 Letras luminosas")
    qtd_letras = 0

    if letras:
        qtd_letras = st.number_input("Quantidade de letras", min_value=1)

    # DESLOCAMENTO
    st.write("🚗 Deslocamento")
    km = st.number_input("Distância (km)", min_value=0.0)
    taxa_deslocamento = km * 2

    salvar = st.form_submit_button("Salvar evento")

    if salvar:

        if total_robos > 7:
            st.error("Corrija a quantidade de robôs.")
        else:

            total = 0
            qtd_robos = len(robos)

            valor_robos = qtd_robos * config["robo"]

            if qtd_robos >= 1 and tambor:
                total += config["combo"]

                if qtd_robos > 1:
                    total += (qtd_robos - 1) * config["robo"]
            else:
                total += valor_robos

                if tambor:
                    total += config["tambor"]

            if pista:
                total += config["pista"]

            if plataforma:
                total += config["plataforma"]

            if letras:
                total += qtd_letras * config["letra"]

            total += taxa_deslocamento

            evento = {
                "nome": nome,
                "endereco": endereco,
                "cep": cep,
                "horario": str(horario),
                "data": data_evento.strftime("%Y-%m-%d"),
                "tipo": tipo,
                "total": total,
                "robos": robos,
                "letras": qtd_letras if letras else 0,
                "km": km
            }

            st.session_state.eventos.append(evento)
            salvar_dados(ARQUIVO_EVENTOS, st.session_state.eventos)

            st.success(f"Evento cadastrado! 💰 Total: R$ {total}")

# =========================
# LISTA (CORRIGIDA)
# =========================

st.header("📅 Agenda de Eventos")

if not st.session_state.eventos:
    st.info("Nenhum evento cadastrado")
else:
    for evento in st.session_state.eventos:

        data_formatada = date.fromisoformat(evento["data"]).strftime("%d/%m/%Y")
        data_evento = date.fromisoformat(evento["data"])

        alerta = ""
        if data_evento == date.today():
            alerta = "🚨 EVENTO HOJE!"
        elif (data_evento - date.today()).days == 1:
            alerta = "⚠️ Evento amanhã"

        # 🔥 CORREÇÃO AQUI
        horario = evento.get("horario", "Não informado")
        endereco = evento.get("endereco", "Não informado")
        cep = evento.get("cep", "Não informado")
        km = evento.get("km", 0)

        robos_txt = f"{len(evento['robos'])} robôs: {', '.join(evento['robos'])}" if evento.get("robos") else "Nenhum"
        letras_txt = f"{evento.get('letras', 0)} letras" if evento.get("letras", 0) > 0 else "Nenhuma"

        mensagem = f"""
📌 Cliente: {evento.get('nome', '')}  
📅 Data: {data_formatada} às {horario}  
🎉 Tipo: {evento.get('tipo', '')}  

📍 Endereço: {endereco}  
📮 CEP: {cep}  

🤖 Robôs: {robos_txt}  
🔠 Letras: {letras_txt}  

🚗 Distância: {km} km  

💰 Total: R$ {evento.get('total', 0)}  
{alerta}
"""

        st.success(mensagem)
        st.divider()
