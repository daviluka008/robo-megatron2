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
ARQUIVO_CLIENTES = "clientes.json"

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

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    dig1 = (soma * 10 % 11) % 10

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    dig2 = (soma * 10 % 11) % 10

    return dig1 == int(cpf[9]) and dig2 == int(cpf[10])

def formatar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf

# =========================
# DADOS
# =========================

clientes = carregar_dados(ARQUIVO_CLIENTES, [])

config = carregar_dados(ARQUIVO_CONFIG, {
    "robo": 1200,
    "tambor": 2800,
    "combo": 3000,
    "pista": 4000,
    "plataforma": 2500,
    "letra": 200
})

if "eventos" not in st.session_state:
    st.session_state.eventos = carregar_dados(ARQUIVO_EVENTOS, [])

# =========================
# CONFIG PREÇOS
# =========================

st.sidebar.header("⚙️ Configurar preços")

config["robo"] = st.sidebar.number_input("Robô", value=config["robo"])
config["tambor"] = st.sidebar.number_input("Tambor LED", value=config["tambor"])
config["combo"] = st.sidebar.number_input("Combo", value=config["combo"])
config["pista"] = st.sidebar.number_input("Pista", value=config["pista"])
config["plataforma"] = st.sidebar.number_input("Plataforma", value=config["plataforma"])
config["letra"] = st.sidebar.number_input("Letras", value=config["letra"])

if st.sidebar.button("💾 Salvar preços"):
    salvar_dados(ARQUIVO_CONFIG, config)
    st.sidebar.success("Preços salvos!")

# =========================
# FORMULÁRIO
# =========================

st.header("➕ Novo Evento")

with st.form("form_evento"):

    cpf_input = st.text_input("CPF")
    cpf_formatado = formatar_cpf(cpf_input)

    cliente_existente = next((c for c in clientes if c["cpf"] == cpf_formatado), None)

    if cliente_existente:
        nome = st.text_input("Nome", value=cliente_existente["nome"])
    else:
        nome = st.text_input("Nome do cliente")

    cep = st.text_input("CEP")
    endereco = st.text_input("Endereço")
    numero = st.text_input("Número")
    complemento = st.text_input("Complemento")

    horario = st.time_input("Horário")
    data_evento = st.date_input("Data", min_value=date.today())

    tipo = st.selectbox("Tipo de evento", ["Casamento", "Festa", "15 anos", "Balada", "Outro"])

    qtd_megatron = st.number_input("Megatron", 0, 7)
    qtd_bumblebee = st.number_input("Bumblebee", 0, 7)
    qtd_tequileiro = st.number_input("Tequileiro", 0, 7)

    robos = (
        ["Megatron"] * qtd_megatron +
        ["Bumblebee"] * qtd_bumblebee +
        ["Tequileiro"] * qtd_tequileiro
    )

    salvar = st.form_submit_button("Salvar evento")

    if salvar:
        st.session_state["_cpf"] = cpf_input
        st.session_state["_cpf_formatado"] = cpf_formatado
        st.session_state["_nome"] = nome
        st.session_state["_endereco"] = f"{endereco}, {numero} - {complemento}"
        st.session_state["_horario"] = str(horario)
        st.session_state["_data"] = data_evento.strftime("%Y-%m-%d")
        st.session_state["_tipo"] = tipo
        st.session_state["_robos"] = robos
        st.session_state["_salvar"] = True

# =========================
# SERVIÇOS
# =========================

st.subheader("🎛️ Serviços extras")

combo_manual = st.checkbox("Combo (Robô + Tambor LED)")
tambor = st.checkbox("🥁 Tambor LED")
pista = st.checkbox("💃 Pista Paris")
plataforma = st.checkbox("🎥 Plataforma 360")

letras = st.checkbox("🔠 Letras")

qtd_letras = 0
nome_letras = ""

if letras:
    qtd_letras = st.number_input("Quantidade de letras", min_value=1, value=1)
    nome_letras = st.text_input("Nome das letras")

# =========================
# SALVAR EVENTO
# =========================

if st.session_state.get("_salvar"):

    if not validar_cpf(st.session_state["_cpf"]):
        st.error("CPF inválido!")
        st.stop()

    robos = st.session_state["_robos"]

    total = 0

    combo_auto = len(robos) >= 1 and tambor

    if combo_manual or combo_auto:
        total += config["combo"]
    else:
        total += len(robos) * config["robo"]
        if tambor:
            total += config["tambor"]

    if pista:
        total += config["pista"]

    if plataforma:
        total += config["plataforma"]

    if letras:
        total += qtd_letras * config["letra"]

    evento = {
        "nome": st.session_state["_nome"],
        "cpf": st.session_state["_cpf_formatado"],
        "endereco": st.session_state["_endereco"],
        "horario": st.session_state["_horario"],
        "data": st.session_state["_data"],
        "tipo": st.session_state["_tipo"],
        "robos": robos,
        "letras": qtd_letras,
        "nome_letras": nome_letras,
        "tambor": tambor,
        "pista": pista,
        "plataforma": plataforma,
        "combo": combo_manual or combo_auto,
        "total": total
    }

    st.session_state.eventos.append(evento)
    salvar_dados(ARQUIVO_EVENTOS, st.session_state.eventos)

    st.session_state["_salvar"] = False

    st.success(f"Evento cadastrado! 💰 Total: R$ {total}")

# =========================
# LISTA
# =========================

st.header("📅 Agenda de Eventos")

if not st.session_state.eventos:
    st.info("Nenhum evento cadastrado")
else:
    for i, evento in enumerate(st.session_state.eventos):

        col1, col2 = st.columns([4, 1])

        with col1:

            data_formatada = date.fromisoformat(evento["data"]).strftime("%d/%m/%Y")

            extras = []

            if evento.get("combo"):
                extras.append("🔥 Combo ( Robô + Tambor LED )")  # ✔️ CORRIGIDO AQUI
            if evento.get("tambor"):
                extras.append("🥁 Tambor LED")
            if evento.get("pista"):
                extras.append("💃 Pista Paris")
            if evento.get("plataforma"):
                extras.append("🎥 Plataforma 360")

            if evento.get("letras", 0) > 0:
                extras.append(f"🔠 Letras: {evento.get('nome_letras')} ({evento.get('letras')})")

            st.success(f"""
📌 Cliente: {evento.get('nome')}  
🧾 CPF: {evento.get('cpf')}  

📅 Data: {data_formatada} às {evento.get('horario')}  
🎉 Tipo: {evento.get('tipo')}  

📍 Endereço: {evento.get('endereco')}  

🤖 Robôs: {len(evento.get('robos', []))} ({", ".join(evento.get('robos', []))})  
🎛️ Serviços: {", ".join(extras) if extras else "Nenhum serviço extra"}  

💰 Total: R$ {evento.get('total')}  
""")

        with col2:
            if st.button("❌ Excluir", key=f"del_{i}"):
                st.session_state.eventos.pop(i)
                salvar_dados(ARQUIVO_EVENTOS, st.session_state.eventos)
                st.rerun()

        st.divider()
