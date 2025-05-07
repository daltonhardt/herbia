import streamlit as st
import pandas as pd
import time
import datetime
import re

def get_date():
    # Get the current date and time
    now = datetime.datetime.now()
    # Convert to string and format
    DATA = now.strftime("%d-%m-%Y")
    HORA = now.strftime("%H:%M")
    return DATA, HORA

# Email regex validation
def is_valid_syntax(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zAHZ0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Inicializa o arquivo CSV local
CSV_FILE = "cadastros.csv"
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Data", "Hora", "Nome", "Sobrenome", "Email", "Telefone", "Perfil"])
    df.to_csv(CSV_FILE, index=False)

# Inicializa os valores no session_state, uma vez
for chave in ['key_nome', 'key_sobrenome', 'key_email', 'key_telefone', 'key_perfil']:
    if chave not in st.session_state:
        st.session_state[chave] = None

st.set_page_config(page_title="Cadastro Herbia", layout="centered")

st.markdown(
        r"""
        <style>
        .stAppDeployButton {
                visibility: hidden;
            }
        </style>
        """, unsafe_allow_html=True
    )

st.title("Participe do Sorteio da Herbia!")
st.subheader("Preencha seus dados abaixo:")

with st.form("cadastro_form"):
    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        nome = st.text_input(label="Nome:",
                             value=st.session_state.key_nome,
                             key='key_nome')
    with col2:
        sobrenome = st.text_input(label="Sobrenome:",
                             value=st.session_state.key_sobrenome,
                             key='key_sobrenome')
    col3, col4 = st.columns([0.6, 0.4])
    with col3:
        email = st.text_input(label="Email:",
                              value=st.session_state.key_email,
                              key='key_email')
    with col4:
        telefone = st.text_input(label="Telefone:",
                                 placeholder='Somente números incluindo DDD',
                                 value=st.session_state.key_telefone,
                                 key='key_telefone')
    perfil = st.radio(label="Qual o seu perfil?",
                      options=['Consumidor Final', 'Especialista', 'Lojista', 'Revendedor autônomo'],
                      horizontal=True,
                      # index=st.session_state.key_perfil,
                      key='key_perfil')

    enviado = st.form_submit_button("Cadastrar")
    if enviado:
        if nome and email and telefone and perfil:
            if is_valid_syntax(email):
                # Salva no CSV
                dia, hora = get_date()
                novo_dado = pd.DataFrame([[dia, hora, nome, sobrenome, email, telefone, perfil]], columns=df.columns)
                novo_dado.to_csv(CSV_FILE, mode='a', header=False, index=False)
                # st.success("Cadastro realizado com sucesso! Boa sorte no sorteio 🎉")
                st.header(f":blue[Cadastro realizado! Boa sorte {nome.capitalize()}]")

                # Limpa os campos no session_state
                del st.session_state.key_nome
                del st.session_state.key_sobrenome
                del st.session_state.key_email
                del st.session_state.key_telefone
                del st.session_state.key_perfil

                st.balloons()

                # Força recarregamento para zerar os campos visivelmente
                time.sleep(3)
                st.rerun()
            else:
                st.header(":red-background[Tem algo errado com o Email.]")

        else:
            # st.error(":red[Por favor, preencha todos os campos.]", icon="‼️")
            st.header(":red-background[Por favor, preencha todos os campos.]")

st.divider()
st.divider()
st.divider()
st.header("Exportar cadastros")

with open(CSV_FILE, "rb") as f:
    st.download_button(
        label="📄 Baixar CSV",
        data=f,
        file_name="cadastros_herbia.csv",
        mime="text/csv"
    )
