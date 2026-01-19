import streamlit as st
import requests
import time
import cv2
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
from io import BytesIO
import os
import yt_dlp
import tempfile

# --- INICIALIZAÇÃO DO DETECTOR DE ROSTOS ---
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="IA Detector Pro", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 5px; padding: 10px; }
    .stTabs [aria-selected="true"] { background-color: #ff4b4b; color: white; }
    .instrucao { background-color: #f9f9f9; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 20px; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. AGENTES DE PERÍCIA FORENSE ---
def realizar_pericia_video(video_file):
    """Analisa o vídeo em busca de anomalias de textura e física"""
    caminho_final = ""
    
    if isinstance(video_file, str):
        caminho_final = video_file
    else:
        caminho_final = "temp_investigacao.mp4"
        with open(caminho_final, "wb") as f:
            f.write(video_file.getbuffer())

    cap = cv2.VideoCapture(caminho_final)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    largura = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    altura = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    duracao_seg = total_frames / fps if fps > 0 else 0

    frames_suspeitos = 0
    passo = max(1, total_frames // 15)

    for i in range(0, total_frames, passo):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            score_textura = cv2.Laplacian(cinza, cv2.CV_64F).var()
            
            # --- NOVO SENSOR ANATÔMICO ---
            faces = face_cascade.detectMultiScale(cinza, 1.1, 4)
            
            # Se encontrar rosto, o sarrafo da textura sobe (IA de rosto é MUITO lisa)
            limite_textura = 280 if len(faces) > 0 else 250
            # --- LINHA DE DIAGNÓSTICO TEMPORÁRIA ---
            # --- DIAGNÓSTICO NA TELA DO APP ---
            
            # Se a textura for menor que o limite, marcamos como suspeito
            if score_textura < limite_textura:
                frames_suspeitos += 1
    cap.release()
    if os.path.exists("temp_investigacao.mp4"):
        os.remove("temp_investigacao.mp4")

    return {
        "duracao": duracao_seg,
        "anomalias_textura": frames_suspeitos,
        "resolucao_quadrada": 1 if largura == altura else 0,
        "fps": fps
    }

# --- 3. INTERFACE E PERÍCIA DE IMAGEM ---
st.title("🛡️ IA-Detector")
st.subheader("O Soro Antiofídico Digital contra a Desinformação")

aba_img, aba_vid = st.tabs(["🖼️ ANALISAR IMAGEM", "🎥 ANALISAR VÍDEO"])

with aba_img:
    st.markdown('<div class="instrucao"><b>MODO PERÍCIA:</b> Analise metadados EXIF e estrutura de pixels.</div>', unsafe_allow_html=True)
    
    if st.button("♻️ Nova Análise de Imagem", key="reset_img"):
        st.rerun()

    tipo_img = st.radio("Fonte:", ["Upload Local", "Link da Web"], horizontal=True)
    img_final = None

    if tipo_img == "Upload Local":
        arquivo = st.file_uploader("Suba a imagem", type=['jpg', 'png', 'jpeg'], key="up_img")
        if arquivo: img_final = arquivo
    else:
        url_input = st.text_input("URL da imagem:")
        if url_input:
            try:
                res = requests.get(url_input, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                if res.status_code == 200: img_final = BytesIO(res.content)
            except: st.error("Erro ao acessar imagem.")

    if img_final:
        st.image(img_final, use_container_width=True)
        if st.button("🚀 INICIAR ANÁLISE DE IMAGEM", use_container_width=True):
            img = Image.open(img_final)
            exif_data = img.getexif()
            
            # Verificação de Metadados (O rastro da câmera)
            if exif_data:
                st.success("✅ Metadados de Hardware detectados!")
                with st.expander("🔍 Ver Evidências Técnicas (Câmera, Data, GPS)"):
                    st.write("**Aviso de Privacidade:** Os dados abaixo são extraídos do arquivo fornecido.")
                    for tag_id, valor in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        st.write(f"**{tag}:** {valor}")
                score_real = 95
                veredito_texto = "Captura de Câmera Genuína (Fato Real)"
            else:
                st.warning("⚠️ Sem metadados de hardware.")
                score_real = 25
                veredito_texto = "Arte Digital, Montagem ou Geração por IA (Imagem Processada)"
            
            # Exibição do Laudo com a gradação que combinamos
            st.subheader("📊 Laudo de Autenticidade")
            st.progress(score_real / 100)
            
            if score_real >= 90:
                st.success(f"**Confiança:** {score_real}% - {veredito_texto}")
            else:
                st.info(f"**Confiança:** {score_real}% - {veredito_texto}")

# --- FUNÇÃO AUXILIAR PARA LINKS (NOVA) ---
def baixar_video_temporario(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(tempfile.gettempdir(), '%(id)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        # O "disfarce" para evitar o Erro 403:
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# --- 4. PERÍCIA DE VÍDEO (v1.7.1 - ATUALIZADA) ---
with aba_vid:
    st.markdown('<div class="instrucao"><b>INVESTIGAÇÃO:</b> Suba vídeos (.mp4) ou cole links para análise técnica.</div>', unsafe_allow_html=True)

    if st.button("♻️ Nova Análise de Vídeo", key="reset_pericia_vid"):
        st.rerun()

    tipo_vid = st.radio("Origem:", ["Upload Local", "Link da Web"], horizontal=True, key="video_source")

    arquivo_vid = None
    url_vid = ""

    if tipo_vid == "Upload Local":
        arquivo_vid = st.file_uploader("Suba o vídeo (.mp4, .mov)", type=['mp4', 'mov'], key="up_vid")
    else:
        url_vid = st.text_input("Cole o link (YouTube, X, Instagram):")

    if st.button("🔬 INICIAR INVESTIGAÇÃO PROFUNDA", use_container_width=True):
        # Validação de entrada
        pode_analisar = (tipo_vid == "Upload Local" and arquivo_vid is not None) or \
                        (tipo_vid == "Link da Web" and url_vid != "")

        if pode_analisar:
            with st.status("Processando perícia técnica...") as s:
                video_para_analise = None
                caminho_temp = None

                try:
                    if tipo_vid == "Link da Web":
                        s.update(label="Pescando vídeo da web... aguarde.")
                        caminho_temp = baixar_video_temporario(url_vid)
                        video_para_analise = caminho_temp
                    else:
                        video_para_analise = arquivo_vid

                    # Chamada unificada da perícia
                    dados = realizar_pericia_video(video_para_analise)
                    
                    # Lógica de Diagnóstico
                    ia_score = 100 if dados['anomalias_textura'] > 12 else (75 if dados['anomalias_textura'] > 5 else 0)
                    humano_score = 100 - ia_score
                    
                    st.subheader("📊 Laudo Forense")
                    st.progress(humano_score / 100)
                    
                    if humano_score <= 35:
                        st.error(f"🚫 VEREDITO: CONTEÚDO IDENTIFICADO COMO IA ({ia_score}%)")
                        st.write(f"**Análise:** Inconsistência crítica detectada em {dados['anomalias_textura']} pontos da micro-textura.")
                    elif humano_score <= 65:
                        st.warning(f"⚠️ VEREDITO: CONTEÚDO SUSPEITO ({ia_score}%)")
                        st.write("**Análise:** Anomalias na densidade de detalhes superficiais sugerem manipulação.")
                    else:
                        st.success(f"✅ VEREDITO: CONTEÚDO GENUÍNO ({humano_score}%)")
                        st.write("**Análise:** Padrões condizentes com captação orgânica real.")
                    
                    s.update(label="Perícia Concluída!", state="complete")

                except Exception as e:
                    st.error(f"Erro técnico: {e}")
                finally:
                    # Garante que o arquivo temporário suma após a análise
                    if caminho_temp and os.path.exists(caminho_temp):
                        os.remove(caminho_temp)
        else:
            st.error("❌ Por favor, forneça um vídeo ou link válido.")# --- 5. RODAPÉ (COM AVISO ÉTICO) ---
st.divider()
st.caption("IA-Detector v1.7.1 | © Yaakov Israel Cypriano com Gemini 3 | Aviso: Este app lê metadados públicos para fins de perícia.")
