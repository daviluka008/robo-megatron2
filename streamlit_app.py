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

# CLIENTES
clientes = carregar_dados(ARQUIVO_CLIENTES, [])

def buscar_cliente(cpf):
    for c in clientes:
        if c["cpf"] == cpf:
            return c
    return None

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

    cpf_input = st.text_input("CPF")
    cpf_formatado = formatar_cpf(cpf_input)

    cliente_existente = buscar_cliente(cpf_formatado)

    if cliente_existente:
        st.success("Cliente encontrado 👇")
        nome = st.text_input("Nome", value=cliente_existente["nome"])
    else:
        nome = st.text_input("Nome do cliente")

    st.write("📍 Local do evento")

    cep = st.text_input("CEP")

    endereco_base = ""
    numero = st.text_input("Número")
    complemento = st.text_input("Complemento")

    cidade = ""
    taxa_deslocamento = 0
    km = 0

    # =========================
    # CEP (CORRIGIDO)
    # =========================
    if cep:
        try:
            resposta = requests.get(
                f"https://viacep.com.br/ws/{cep}/json/",
                timeout=5
            )

            if resposta.status_code == 200:
                dados = resposta.json()

                if "erro" not in dados:
                    endereco_base = dados.get("logradouro", "")
                    cidade = dados.get("localidade", "")
                    estado = dados.get("uf", "")

                    st.success(f"{endereco_base} - {cidade}/{estado}")

                    if cidade.lower() != "são paulo":
                        st.warning("🚗 Fora da capital (até 50km sem custo)")

                        km = st.number_input("Distância (km)", min_value=1.0)

                        if km > 50:
                            taxa_deslocamento = (km - 50) * 2
                            st.info(f"💰 Taxa de deslocamento: R$ {(km - 50) * 2}")
                        else:
                            taxa_deslocamento = 0
                            st.info("Sem taxa de deslocamento (até 50km)")
                    else:
                        st.info("Sem taxa de deslocamento (capital)")
                else:
                    st.error("CEP não encontrado")
            else:
                st.error("Erro na consulta do CEP")

        except:
            st.error("Erro ao buscar CEP")

    endereco_final = f"{endereco_base}, {numero} - {complemento}"

    horario = st.time_input("Horário do evento")
    data_evento = st.date_input("Data do evento", min_value=date.today())

    tipo = st.selectbox("Tipo de evento", ["Casamento", "Festa", "15 anos", "Balada", "Outro"])

    st.write("🤖 Robôs (máx. 7)")

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

    letras = st.checkbox("🔠 Letras luminosas")
    qtd_letras = 0

    if letras:
        qtd_letras = st.number_input("Quantidade de letras", 1)

    salvar = st.form_submit_button("Salvar evento")

    # =========================
    # CÁLCULO
    # =========================

    if salvar:

        if not validar_cpf(cpf_input):
            st.error("CPF inválido!")
            st.stop()

        if len(robos) > 7:
            st.error("Máximo de 7 robôs.")
        else:

            total = 0

            if len(robos) >= 1 and tambor:
                total += config["combo"]
                if len(robos) > 1:
                    total += (len(robos) - 1) * config["robo"]
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

            total += taxa_deslocamento

            evento = {
                "nome": nome,
                "cpf": cpf_formatado,
                "endereco": endereco_final,
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

            if not cliente_existente:
                clientes.append({"nome": nome, "cpf": cpf_formatado})
                salvar_dados(ARQUIVO_CLIENTES, clientes)

            st.success(f"Evento cadastrado! 💰 Total: R$ {total}")

# =========================
# LISTA DE EVENTOS
# =========================

st.header("📅 Agenda de Eventos")

if not st.session_state.eventos:
    st.info("Nenhum evento cadastrado")
else:
    for i, evento in enumerate(st.session_state.eventos):

        col1, col2 = st.columns([4, 1])

        with col1:
            data_formatada = date.fromisoformat(evento["data"]).strftime("%d/%m/%Y")
            data_evento = date.fromisoformat(evento["data"])

            alerta = ""
            if data_evento == date.today():
                alerta = "🚨 EVENTO HOJE!"
            elif (data_evento - date.today()).days == 1:
                alerta = "⚠️ Evento amanhã"

            mensagem = f"""
📌 Cliente: {evento.get('nome')}  
🧾 CPF: {evento.get('cpf')}  

📅 Data: {data_formatada} às {evento.get('horario')}  
🎉 Tipo: {evento.get('tipo')}  

📍 Endereço: {evento.get('endereco')}  

🤖 Robôs: {len(evento['robos'])}  

🚗 Distância: {evento.get('km')} km  

💰 Total: R$ {evento.get('total')}  
{alerta}
"""
            st.success(mensagem)

        with col2:
            if st.button("❌ Excluir", key=f"del_{i}"):
                st.session_state.eventos.pop(i)
                salvar_dados(ARQUIVO_EVENTOS, st.session_state.eventos)
                st.rerun()

        st.divider()
