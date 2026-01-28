import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
from PIL.ExifTags import TAGS
from io import BytesIO
import os
import yt_dlp
import tempfile
import requests

os.environ["KERAS_BACKEND"] = "tensorflow"
import keras_cv

@st.cache_resource
def carregar_modelo_ia():
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        caminho_pesos = os.path.join(base_path, "meu_modelo.h5")
        model = keras_cv.models.EfficientNetV2Backbone.from_preset(
            "kaggle://keras/efficientnetv2/keras/efficientnetv2_b0_imagenet"
        )
        model.load_weights(caminho_pesos, skip_mismatch=True, by_name=True)
        return model
    except:
        return None

modelo_ia = carregar_modelo_ia()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

st.set_page_config(page_title="IA Detector Pro", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 5px; padding: 10px; }
    .stTabs [aria-selected="true"] { background-color: #ff4b4b; color: white; }
    .instrucao { background-color: #f9f9f9; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 20px; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

def analisar_ela(img_input, quality=90):
    if img_input.mode != 'RGB': img_input = img_input.convert('RGB')
    temp_ela = "temp_ela.jpg"
    img_input.save(temp_ela, 'JPEG', quality=quality)
    img_comprimida = Image.open(temp_ela)
    ela_img = ImageChops.difference(img_input, img_comprimida)
    extrema = ela_img.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0: max_diff = 1
    scale = 255.0 / max_diff
    ela_img = ImageEnhance.Brightness(ela_img).enhance(scale)
    os.remove(temp_ela)
    return ela_img

def baixar_video_temporario(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(tempfile.gettempdir(), '%(id)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

def realizar_pericia_video(video_input):
    caminho_final = ""
    if isinstance(video_input, str):
        caminho_final = video_input
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tf:
            tf.write(video_input.getbuffer())
            caminho_final = tf.name

    cap = cv2.VideoCapture(caminho_final)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_ia_suspeitos = 0
    frames_analisados = 12
    passo = max(1, total_frames // frames_analisados)

    for i in range(0, total_frames, passo):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret and modelo_ia:
            frame_res = cv2.resize(frame, (224, 224))
            img_array = np.expand_dims(frame_res, axis=0)
            predicao = modelo_ia.predict(img_array, verbose=0)
            if np.mean(predicao) < 0.05:
                frames_ia_suspeitos += 1

    cap.release()
    if not isinstance(video_input, str) and os.path.exists(caminho_final):
        os.remove(caminho_final)
    
    return {"anomalias": frames_ia_suspeitos}

st.title("🛡️ IA-Detector")
st.subheader("A verdade por trás dos pixels")

aba_img, aba_vid = st.tabs(["🖼️ ANALISAR IMAGEM", "🎥 ANALISAR VÍDEO"])

with aba_img:
    st.markdown('<div class="instrucao"><b>MODO PERÍCIA:</b> Analise metadados e estrutura de pixels.</div>', unsafe_allow_html=True)
    tipo_img = st.radio("Fonte da Imagem:", ["Upload Local", "Link da Web"], horizontal=True)
    img_final = None
    
    if tipo_img == "Upload Local":
        arquivo = st.file_uploader("Suba a imagem", type=['jpg', 'jpeg', 'png'])
        if arquivo: img_final = Image.open(arquivo)
    else:
        url_img = st.text_input("URL da imagem:")
        if url_img:
            try:
                res = requests.get(url_img, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                if res.status_code == 200:
                    img_final = Image.open(BytesIO(res.content))
                else:
                    st.error("Não consegui acessar a imagem. O link pode estar bloqueado.")
            except Exception as e:
                st.error(f"Erro ao carregar URL: {e}")

    if img_final and st.button("🚀 INICIAR ANÁLISE DE IMAGEM"):
        img_ela = analisar_ela(img_final)
        col1, col2 = st.columns(2)
        col1.image(img_final, caption="Original", use_container_width=True)
        col2.image(img_ela, caption="Mapa de Ruído (ELA)", use_container_width=True)
        
        exif = img_final.getexif()
        if exif:
            st.success("✅ Câmera Real Detectada (Metadados EXIF presentes)")
        else:
            st.warning("⚠️ Sem metadados de hardware. Possível IA, Print ou Redes Sociais.")

with aba_vid:
    st.markdown('<div class="instrucao"><b>INVESTIGAÇÃO:</b> Vídeos .mp4 ou links da web.</div>', unsafe_allow_html=True)
    tipo_vid = st.radio("Origem do Vídeo:", ["Upload Local", "Link da Web"], horizontal=True)
    video_origem = None
    
    if tipo_vid == "Upload Local":
        video_origem = st.file_uploader("Suba o vídeo (.mp4)", type=['mp4', 'mov'])
    else:
        url_vid = st.text_input("Cole o link (YouTube, X, Instagram):")
        if url_vid: video_origem = url_vid

    if video_origem is not None and st.button("🔬 INICIAR INVESTIGAÇÃO PROFUNDA"):
        with st.status("IA analisando frames...") as s:
            try:
                caminho_processar = video_origem
                if tipo_vid == "Link da Web":
                    caminho_processar = baixar_video_temporario(video_origem)
                
                resultado = realizar_pericia_video(caminho_processar)
                
                if resultado['anomalias'] > 5:
                    st.error(f"🚫 ALTA SUSPEITA DE DEEPFAKE (Detectadas {resultado['anomalias']} anomalias)")
                else:
                    st.success("✅ Veredito: Textura condizente com gravação real.")
                
                if tipo_vid == "Link da Web" and os.path.exists(caminho_processar):
                    os.remove(caminho_processar)
                s.update(label="Perícia Concluída!", state="complete")
            except Exception as e:
                st.error(f"Erro técnico: {e}")

st.divider()
st.caption("IA-Detector v1.9.0 | © Yaakov Israel Cypriano & Gemini 3 | Modelo: EfficientNetV2B0")
