import streamlit as st

# Configuração da página
st.set_page_config(page_title="IA Detector", page_icon="🛡️")

st.title("🛡️ IA Detector: Identificador de Mídias")
st.markdown("Verifique se o conteúdo foi criado por humanos ou máquinas.")

# Abas de navegação
aba_texto, aba_imagem = st.tabs(["✍️ Texto", "🖼️ Imagem"])

with aba_texto:
    st.header("Análise de Texto")
    entrada = st.text_area("Cole o texto suspeito aqui:", placeholder="Ex: Proposta de empréstimo...")
    if st.button("Verificar Texto"):
        # Lógica inicial de simulação
        st.warning("Análise: 85% de probabilidade de ser IA (Padrão robótico detectado).")

with aba_imagem:
    st.header("Análise de Imagem")
    foto = st.file_uploader("Suba uma imagem para analisar", type=['jpg', 'jpeg', 'png'])
    if foto:
        st.image(foto, caption="Imagem carregada")
        if st.button("Escanear Pixels"):
            st.info("Buscando por artefatos de compressão e ruído de difusão...")
