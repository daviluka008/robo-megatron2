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

    tambor = st.checkbox("🥁 Tambor LED (R$2800)")
    pista = st.checkbox("💃 Pista Paris (R$4000)")
    plataforma = st.checkbox("🎥 Plataforma 360 (R$2500)")

    letras = st.checkbox("🔠 Letras luminosas (R$200 por letra)")
    qtd_letras = 0

    if letras:
        qtd_letras = st.number_input("Quantidade de letras", min_value=1, step=1)

    salvar = st.form_submit_button("Salvar evento")

    if salvar:

        total = 0

        # =========================
        # ROBÔS
        # =========================

        qtd_robos = len(robos)

        if qtd_robos == 1:
            total += 1200
        elif qtd_robos > 1:
            # primeiro robô 1200 + 800 por adicional (ajustável)
            total += 1200 + (qtd_robos - 1) * 800

        # =========================
        # COMBO ROBÔ + TAMBOR
        # =========================

        if qtd_robos >= 1 and tambor:
            total -= 1200  # remove valor do robô calculado
            total -= 2800  # remove tambor
            total += 3000  # aplica combo

        else:
            if tambor:
                total += 2800

        # =========================
        # OUTROS
        # =========================

        if pista:
            total += 4000

        if plataforma:
            total += 2500

        if letras:
            total += qtd_letras * 200

        evento = {
            "nome": nome,
            "data": data_evento,
            "tipo": tipo,
            "total": total,
            "robos": robos,
            "letras": qtd_letras if letras else 0
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

        st.subheader(f"{evento['nome']} - {evento['data'].strftime('%d/%m/%Y')}")

        st.write(f"Tipo: {evento['tipo']}")

        if evento["robos"]:
            st.write(f"🤖 Robôs: {', '.join(evento['robos'])}")

        # ALERTA
        if evento["data"] == date.today():
            st.error("🚨 EVENTO HOJE!")
        elif (evento["data"] - date.today()).days == 1:
            st.warning("⚠️ Evento amanhã")

        st.success(f"💰 Total do evento: R$ {evento['total']}")

        if evento["letras"] > 0:
            st.write(f"🔠 Letras: {evento['letras']}")

        st.divider()
        
