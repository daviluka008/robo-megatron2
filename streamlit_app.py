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

# CPF
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

clientes = carregar_dados(ARQUIVO_CLIENTES, [])

def buscar_cliente(cpf):
    for c in clientes:
        if c["cpf"] == cpf:
            return c
    return None

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

for key in config.keys():
    config[key] = st.sidebar.number_input(key.capitalize(), value=config[key])

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

    cpf_input = st.text_input("CPF")
    cpf_formatado = formatar_cpf(cpf_input)

    cliente_existente = buscar_cliente(cpf_formatado)

    if cliente_existente:
        nome = st.text_input("Nome", value=cliente_existente["nome"])
    else:
        nome = st.text_input("Nome do cliente")

    cep = st.text_input("CEP")
    endereco = st.text_input("Endereço")
    numero = st.text_input("Número")
    complemento = st.text_input("Complemento")

    cidade = ""

    if cep:
        try:
            r = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5)
            data = r.json()
            if "erro" not in data:
                cidade = data.get("localidade", "")
        except:
            pass

    endereco_final = f"{endereco}, {numero} - {complemento}"

    horario = st.time_input("Horário")
    data_evento = st.date_input("Data", min_value=date.today())

    tipo = st.selectbox("Tipo", ["Casamento", "Festa", "15 anos", "Balada", "Outro"])

    qtd_megatron = st.number_input("Megatron", 0, 7)
    qtd_bumblebee = st.number_input("Bumblebee", 0, 7)
    qtd_tequileiro = st.number_input("Tequileiro", 0, 7)

    robos = (
        ["Megatron"] * qtd_megatron +
        ["Bumblebee"] * qtd_bumblebee +
        ["Tequileiro"] * qtd_tequileiro
    )

    tambor = st.checkbox("🥁 Tambor LED")
    pista = st.checkbox("💃 Pista Paris")
    plataforma = st.checkbox("🎥 Plataforma 360")

    combo_manual = st.checkbox("🔥 Combo (Robô + Tambor LED)")

    salvar = st.form_submit_button("Salvar evento")

# =========================
# 🔥 LETRAS FORA DO FORM (CORRETO)
# =========================

st.subheader("🔠 Letras luminosas")

letras = st.checkbox("Ativar letras", key="letras")

if "letras" not in st.session_state:
    st.session_state.letras = False

st.session_state.letras = letras

if st.session_state.letras:
    qtd_letras = st.number_input("Quantidade de letras", min_value=1, key="qtd_letras")
    nome_letras = st.text_input("Nome das letras (ex: DAVI, 15 ANOS)", key="nome_letras")
else:
    qtd_letras = 0
    nome_letras = ""

# =========================
# CÁLCULO
# =========================

if salvar:

    if not validar_cpf(cpf_input):
        st.error("CPF inválido!")
        st.stop()

    total = 0
    qtd_robos = len(robos)

    combo_auto = qtd_robos >= 1 and tambor

    if combo_manual or combo_auto:
        total += config["combo"]
    else:
        total += qtd_robos * config["robo"]
        if tambor:
            total += config["tambor"]

    if pista:
        total += config["pista"]

    if plataforma:
        total += config["plataforma"]

    if letras:
        total += qtd_letras * config["letra"]

    evento = {
        "nome": nome,
        "cpf": cpf_formatado,
        "endereco": endereco_final,
        "cidade": cidade,
        "horario": str(horario),
        "data": data_evento.strftime("%Y-%m-%d"),
        "tipo": tipo,
        "total": total,
        "robos": robos,
        "letras": qtd_letras,
        "nome_letras": nome_letras,
        "tambor": tambor,
        "pista": pista,
        "plataforma": plataforma,
        "combo": combo_manual or combo_auto
    }

    st.session_state.eventos.append(evento)
    salvar_dados(ARQUIVO_EVENTOS, st.session_state.eventos)

    st.success(f"Evento cadastrado! 💰 R$ {total}")

# =========================
# LISTA
# =========================

st.header("📅 Agenda de Eventos")

for i, evento in enumerate(st.session_state.eventos):

    col1, col2 = st.columns([4, 1])

    with col1:

        extras = []

        if evento.get("tambor"):
            extras.append("🥁 Tambor LED")

        if evento.get("pista"):
            extras.append("💃 Pista Paris")

        if evento.get("plataforma"):
            extras.append("🎥 Plataforma 360")

        if evento.get("combo"):
            extras.append("🔥 Combo (Robô + Tambor LED)")

        if evento.get("letras", 0) > 0:
            extras.append(f"🔠 Letras: {evento.get('nome_letras')} ({evento.get('letras')})")

        robos_texto = ", ".join(evento.get("robos", []))

        st.success(f"""
📌 Cliente: {evento.get('nome')}  
🧾 CPF: {evento.get('cpf')}  

📅 Data: {evento.get('data')} às {evento.get('horario')}  
🎉 Tipo: {evento.get('tipo')}  

📍 Endereço: {evento.get('endereco')}  

🤖 Robôs: {len(evento.get('robos', []))} ({robos_texto})  
🎛️ Serviços: {", ".join(extras) if extras else "Nenhum serviço extra"}  

💰 Total: R$ {evento.get('total')}  
""")

    with col2:
        if st.button("❌ Excluir", key=f"del_{i}"):
            st.session_state.eventos.pop(i)
            salvar_dados(ARQUIVO_EVENTOS, st.session_state.eventos)
            st.rerun()
