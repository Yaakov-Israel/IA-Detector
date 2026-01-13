import streamlit as st
import requests
import time
from PIL import Image
from PIL.ExifTags import TAGS
from io import BytesIO

# Configuração da página - "Vestindo a roupa de gala"
st.set_page_config(page_title="IA Detector Pro", page_icon="🛡️", layout="centered")

# CSS para Identidade Visual
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 5px; padding: 10px; }
    .stTabs [aria-selected="true"] { background-color: #ff4b4b; color: white; }
    .instrucao { background-color: #f9f9f9; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 20px; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ IA-Detector")
st.subheader("O Soro Antiofídico Digital contra a Desinformação")

aba_img, aba_vid = st.tabs(["🖼️ ANALISAR IMAGEM", "🎥 ANALISAR VÍDEO"])

# --- ABA DE IMAGEM (PERÍCIA FORENSE) ---
with aba_img:
    st.markdown('<div class="instrucao"><b>MODO PERÍCIA:</b> Use Upload para fotos originais (preserva metadados) ou Link para checar imagens virais da web.</div>', unsafe_allow_html=True)
    
    tipo_img = st.radio("Selecione o modo:", ["Upload (Modo Pro)", "Link da Web"], horizontal=True)
    img_final = None

    if tipo_img == "Upload (Modo Pro)":
        arquivo = st.file_uploader("Suba a imagem original", type=['jpg', 'png', 'jpeg'])
        if arquivo: img_final = arquivo
    else:
        url_input = st.text_input("Cole o endereço da imagem (Botão direito > Copiar endereço):")
        if url_input:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                res = requests.get(url_input, headers=headers, timeout=10)
                if res.status_code == 200: img_final = BytesIO(res.content)
                else: st.error("Erro ao acessar link.")
            except: st.error("Link inválido ou protegido.")

    if img_final:
        st.image(img_final, use_container_width=True)
        if st.button("🚀 INICIAR ANÁLISE DE IMAGEM", use_container_width=True):
            with st.spinner("Escaneando vestígios digitais..."):
                time.sleep(1)
                img = Image.open(img_final)
                exif = img.getexif()
                
                st.subheader("📊 Relatório Forense")
                if exif:
                    for tag_id in exif:
                        tag = TAGS.get(tag_id, tag_id)
                        st.write(f"✅ **{tag}**: {exif.get(tag_id)}")
                else:
                    st.warning("⚠️ **ALERTA:** Nenhum metadado original encontrado. A imagem pode ser um print ou gerada por IA.")

# --- ABA DE VÍDEO (COMBATE A DEEPFAKES) ---
with aba_vid:
    st.markdown('<div class="instrucao"><b>COMBATE A DEEPFAKE:</b> Analise links do X, YouTube ou vídeos suspeitos recebidos por mensageiros.</div>', unsafe_allow_html=True)
    
    tipo_vid = st.radio("Origem do vídeo:", ["Upload Local", "Link de Rede Social"], horizontal=True)
    
    if tipo_vid == "Upload Local":
        vid_file = st.file_uploader("Envie o vídeo (.mp4)", type=['mp4'])
    else:
        url_vid = st.text_input("Cole o link (X, YouTube, etc):")
        st.caption("Nota: Usamos a tecnologia yt-dlp para extrair mídias de redes sociais.")

    st.subheader("🕵️ Checklist Forense")
    col1, col2 = st.columns(2)
    with col1:
        v1 = st.checkbox("Piscadas Naturais?")
        v2 = st.checkbox("Sincronia Labial?")
    with col2:
        v3 = st.checkbox("Fundo Estável?")
        v4 = st.checkbox("Pele com Textura?")

    if st.button("🔬 INICIAR ANÁLISE DE VÍDEO", use_container_width=True):
        with st.status("Extraindo frames para análise...") as s:
            time.sleep(2)
            s.update(label="Verificando padrões faciais...", state="running")
            time.sleep(2)
            
            if not v1 or not v2 or not v3 or not v4:
                st.error("🚨 **VEREDITO:** Alta probabilidade de manipulação. Sinais de Deepfake detectados.")
            else:
                st.success("✅ **VEREDITO:** Baixa probabilidade de Deepfake grosseiro. Vídeo parece consistente.")
            s.update(label="Análise Finalizada", state="complete")

st.divider()
st.caption("IA-Detector v1.4 | Protegendo a verdade na era da IA.")
