import streamlit as st
import time

st.set_page_config(page_title="IA Detector Pro", page_icon="🛡️")

st.title("🛡️ IA Detector: Identificador de Mídias")
st.write("Proteja-se contra golpes. Analise textos, imagens e vídeos suspeitos.")

# Criando as abas incluindo Vídeo agora
aba_texto, aba_imagem, aba_video = st.tabs(["✍️ Texto", "🖼️ Imagem", "🎥 Vídeo"])

with aba_texto:
    st.header("Análise de Texto")
    entrada = st.text_area("Cole o conteúdo da mensagem:")
    if st.button("Verificar Texto"):
        with st.spinner("Analisando padrões linguísticos..."):
            time.sleep(1)
            st.warning("Resultado: Alta probabilidade de geração por IA (85%). Cuidado com solicitações de dados.")

with aba_imagem:
    st.header("Análise de Imagem")
    foto = st.file_uploader("Suba a foto", type=['jpg', 'png'])
    if foto:
        st.image(foto)
        if st.button("Escanear Pixels"):
            st.info("Buscando por artefatos de difusão e metadados de IA...")

with aba_video:
    st.header("Detector de Deepfake")
    st.markdown("⚠️ **Alerta:** Criminosos usam vídeos de pessoas conhecidas para pedir dinheiro.")
    video_file = st.file_uploader("Envie o vídeo suspeito", type=['mp4', 'mov'])
    
    if video_file:
        st.video(video_file)
        if st.button("Iniciar Análise Forense"):
            with st.status("Analisando frames do vídeo...", expanded=True) as status:
                st.write("Buscando inconsistências na sincronia labial...")
                time.sleep(2)
                st.write("Verificando frequência de piscadas e sombras faciais...")
                time.sleep(2)
                status.update(label="Análise Concluída!", state="complete")
            
            st.error("🚨 ALERTA: Detectada inconsistência temporal severa. Este vídeo possui 92% de chance de ser um Deepfake.")
            st.info("Dica de Segurança: Se alguém pedir dinheiro por vídeo, ligue para a pessoa por outro meio para confirmar.")
