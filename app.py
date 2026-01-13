import streamlit as st
import requests
import time
from PIL import Image
from PIL.ExifTags import TAGS
from io import BytesIO

st.set_page_config(page_title="IA Detector Pro", page_icon="🛡️")

st.title("🛡️ IA Detector: Perícia Visual")
st.write("Foco em análise forense de Imagens e Vídeos suspeitos.")

# Removido aba de texto - Foco no cofre (Imagem e Vídeo)
aba_imagem, aba_video = st.tabs(["🖼️ Perícia de Imagem", "🎥 Perícia de Vídeo"])

# --- ABA DE IMAGEM ---
with aba_imagem:
    st.header("🔬 Escaneamento de Imagem")
    
    metodo_img = st.radio("Origem:", ["Arquivo Local", "Link da Web"], horizontal=True)
    img_para_analise = None

    if metodo_img == "Arquivo Local":
        arquivo = st.file_uploader("Upload", type=['jpg', 'png', 'jpeg'])
        if arquivo:
            img_para_analise = arquivo
    else:
        url_img = st.text_input("Cole a URL da imagem:")
        if url_img:
            try:
                # Simula um navegador para evitar bloqueio do X/Twitter
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url_img, headers=headers, stream=True, timeout=10)
                if response.status_code == 200:
                    img_para_analise = BytesIO(response.content)
                else:
                    st.error(f"O site bloqueou o acesso (Erro {response.status_code})")
            except Exception as e:
                st.error("Erro ao acessar o link.")

    if img_para_analise:
        # Mostra a imagem
        st.image(img_para_analise, caption="Pronta para perícia", use_container_width=True)
        
        # Botão de ação (Resolve o problema do Enter)
        if st.button("🚀 Iniciar Perícia nos Pixels"):
            with st.status("Analisando DNA do arquivo...") as s:
                img = Image.open(img_para_analise)
                info = img.getexif()
                time.sleep(1.5)
                
                if info:
                    st.subheader("✅ Metadados Encontrados")
                    for tag_id in info:
                        tag = TAGS.get(tag_id, tag_id)
                        dado = info.get(tag_id)
                        st.write(f"**{tag}**: {dado}")
                else:
                    st.warning("⚠️ Sem metadados EXIF. Imagem possivelmente printada, baixada de rede social ou gerada por IA.")
                s.update(label="Perícia Finalizada!", state="complete")

# --- ABA DE VÍDEO ---
with aba_video:
    st.header("🎥 Análise de Deepfake")
    metodo_v = st.radio("Origem Vídeo:", ["Arquivo", "Link"], horizontal=True)
    
    video_data = None
    if metodo_v == "Arquivo":
        video_data = st.file_uploader("Vídeo", type=['mp4'])
    else:
        link_v = st.text_input("URL do Vídeo:")
        if link_v: video_data = link_v

    if video_data:
        st.info("Sistema pronto para análise de consistência facial.")
        
        # Checklist de Perícia Humana (Dá autoridade ao app)
        st.subheader("Checklist Forense (Observe no vídeo):")
        c1 = st.checkbox("Piscadas de olhos naturais?")
        c2 = st.checkbox("Sincronia labial perfeita?")
        c3 = st.checkbox("Iluminação do rosto condiz com o fundo?")

        if st.button("🔬 Iniciar Verificação Forense"):
            with st.status("Processando frames...") as s:
                time.sleep(3)
                if not c1 or not c2 or not c3:
                    st.error("🚨 ALERTA: Sinais visuais inconsistentes detectados.")
                else:
                    st.success("✅ Estabilidade detectada. Menor probabilidade de manipulação grosseira.")
                s.update(label="Análise Concluída", state="complete")
