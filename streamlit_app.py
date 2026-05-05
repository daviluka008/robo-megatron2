import streamlit as st
from datetime import date
import json
import os
import requests

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
# CONFIG PREÇOS
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
# FORMULÁRIO
# =========================

st.header("➕ Novo Evento")

with st.form("form_evento"):

    nome = st.text_input("Nome do cliente")

    # =========================
    # CEP (SEM API)
    # =========================

    st.write("📍 Local do evento")

    cep = st.text_input("CEP")

    endereco = ""
    cidade = ""
    taxa_deslocamento = 0
    km = 0

    if cep:
        try:
            resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()

            if "erro" not in resposta:
                endereco = f"{resposta['logradouro']}"
                cidade = resposta["localidade"]
                estado = resposta["uf"]

                st.success(f"{endereco} - {cidade}/{estado}")

                if cidade.lower() != "são paulo":
                    st.warning("🚗 Fora da capital")

                    km = st.number_input("Distância aproximada (km)", min_value=1.0)
                    taxa_deslocamento = km * 2
                else:
                    st.info("Sem taxa de deslocamento")

            else:
                st.error("CEP inválido")

        except:
            st.error("Erro ao buscar CEP")

    horario = st.time_input("Horário do evento")

    data_evento = st.date_input("Data do evento", min_value=date.today(), format="DD/MM/YYYY")

    tipo = st.selectbox("Tipo de evento", ["Casamento", "Festa", "15 anos", "Balada", "Outro"])

    # =========================
    # ROBÔS
    # =========================

    st.write("🤖 Robôs (máx. 7)")

    qtd_megatron = st.number_input("Megatron", 0, 7)
    qtd_bumblebee = st.number_input("Bumblebee", 0, 7)
    qtd_tequileiro = st.number_input("Tequileiro", 0, 7)

    total_robos = qtd_megatron + qtd_bumblebee + qtd_tequileiro

    robos = (
        ["Megatron"] * qtd_megatron +
        ["Bumblebee"] * qtd_bumblebee +
        ["Tequileiro"] * qtd_tequileiro
    )

    # =========================
    # SERVIÇOS
    # =========================

    tambor = st.checkbox("🥁 Tambor LED")
    pista = st.checkbox("💃 Pista Paris")
    plataforma = st.checkbox("🎥 Plataforma 360")

    letras = st.checkbox("🔠 Letras luminosas")
    qtd_letras = 0

    if letras:
        qtd_letras = st.number_input("Quantidade de letras", 1)

    salvar = st.form_submit_button("Salvar evento")

    # =========================
    # CÁLCULO
    # =========================

    if salvar:

        if total_robos > 7:
            st.error("Máximo de 7 robôs.")
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
                "cidade": cidade,
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
# LISTA
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

        horario = evento.get("horario", "Não informado")
        endereco = evento.get("endereco", "Não informado")
        cidade = evento.get("cidade", "")
        km = evento.get("km", 0)

        robos_txt = f"{len(evento['robos'])} robôs: {', '.join(evento['robos'])}" if evento.get("robos") else "Nenhum"

        mensagem = f"""
📌 Cliente: {evento.get('nome', '')}  
📅 Data: {data_formatada} às {horario}  
🎉 Tipo: {evento.get('tipo', '')}  

📍 Local: {endereco} - {cidade}  

🤖 Robôs: {robos_txt}  

🚗 Distância: {km} km  

💰 Total: R$ {evento.get('total', 0)}  
{alerta}
"""

        st.success(mensagem)
        st.divider()
