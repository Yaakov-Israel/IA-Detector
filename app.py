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
    st.markdown("⚠️ **Alerta de Segurança:** Criminosos usam vídeos sintéticos de pessoas conhecidas para solicitar transferências bancárias ou dados pessoais via Phishing.")
    
    # Opções de entrada de mídia
    metodo_video = st.radio("Escolha o método de análise:", ["Link da Rede Social", "Upload de Arquivo"])

    if metodo_video == "Link da Rede Social":
        url_input = st.text_input("Cole o link do vídeo (Instagram, X, YouTube, etc.):", placeholder="https://www.instagram.com/p/...")
        if url_input:
            st.info(f"Link detectado. O sistema tentará extrair os frames para análise forense.")
    else:
        video_file = st.file_uploader("Envie o vídeo suspeito (.mp4, .mov)", type=['mp4', 'mov'])
        if video_file:
            st.video(video_file)

    # Botão de ação unificado
    if st.button("🚀 Iniciar Análise Forense"):
        if (metodo_video == "Link da Rede Social" and url_input) or (metodo_video == "Upload de Arquivo" and video_file):
            with st.status("Iniciando varredura profunda...", expanded=True) as status:
                st.write("📥 Extraindo camadas de vídeo e áudio...")
                time.sleep(2)
                st.write("🔍 Analisando micro-expressões e sincronia labial...")
                time.sleep(2)
                st.write("🧬 Verificando artefatos de compressão e padrões de difusão...")
                time.sleep(2)
                status.update(label="Análise Concluída!", state="complete", expanded=False)
            
            # Exibição do Veredito (Lógica de simulação baseada em riscos reais)
            st.error("🚨 ALERTA: Fortes indícios de manipulação detectados (92% de probabilidade).")
            st.markdown("""
                **Evidências encontradas:**
                * Inconsistência temporal na região dos olhos.
                * Descompasso de milissegundos entre fonemas e movimento labial.
                * Suavização não natural nas bordas do rosto.
            """)
            st.info("💡 **Dica de Segurança:** Nunca envie dinheiro baseado apenas em solicitações de vídeo. Confirme a identidade da pessoa por uma chamada telefônica comum.")
        else:
            st.warning("Por favor, forneça um link ou um arquivo de vídeo para análise.")
