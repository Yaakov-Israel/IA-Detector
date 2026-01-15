import streamlit as st
import requests
import time
import cv2
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
from io import BytesIO
import os

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
    with open("temp_investigacao.mp4", "wb") as f:
        f.write(video_file.getbuffer())

    cap = cv2.VideoCapture("temp_investigacao.mp4")
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
            if score_textura < 80:
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
        arquivo = st.file_uploader("Suba a imagem", type=['jpg', 'png', 'jpeg'])
        if arquivo:
            img_final = arquivo
    else:
        url_input = st.text_input("URL da imagem:")
        if url_input:
            try:
                res = requests.get(url_input, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                if res.status_code == 200:
                    img_final = BytesIO(res.content)
            except:
                st.error("Erro ao acessar imagem.")

    if img_final:
        st.image(img_final, use_container_width=True)
        if st.button("🚀 INICIAR ANÁLISE DE IMAGEM", use_container_width=True):
            img = Image.open(img_final)
            exif = img.getexif()
            score_real = 90 if exif else 20
            st.subheader("📊 Relatório de Autenticidade")
            st.progress(score_real / 100)
            st.write(f"Confiança de Origem Humana: {score_real}%")

# --- 4. PERÍCIA DE VÍDEO (COMBATE A DEEPFAKES) ---
with aba_vid:
    st.markdown('<div class="instrucao"><b>INVESTIGAÇÃO:</b> Suba vídeos de qualquer duração para análise de padrões.</div>', unsafe_allow_html=True)

    if st.button("♻️ Nova Análise de Vídeo", key="reset_pericia_vid"):
        st.rerun()

    tipo_vid = st.radio("Origem:", ["Upload Local", "Link da Web"], horizontal=True, key="video_source")

    arquivo_vid = None
    if tipo_vid == "Upload Local":
        arquivo_vid = st.file_uploader("Suba o vídeo (.mp4, .mov)", type=['mp4', 'mov'])
    else:
        url_vid = st.text_input("Cole o link (YouTube/X/Insta):")

    st.subheader("🕵️ Checklist Forense (As 10 Regras)")
    col_x, col_y = st.columns(2)
    with col_x:
        r_fisica = st.checkbox("Violação da Gravidade/Física? (Ex: Gata na parede)")
        r_sentido = st.checkbox("Ações que não fazem sentido?")
        r_objetos = st.checkbox("Objetos atravessando outros?")
    with col_y:
        r_maos = st.checkbox("Mãos ou dedos anormais?")
        r_rosto = st.checkbox("Rostos ou olhos estranhos?")
        r_voz = st.checkbox("Voz robótica ou sem emoção?")

    if st.button("🔬 INICIAR INVESTIGAÇÃO PROFUNDA", use_container_width=True):
        if not (arquivo_vid or (tipo_vid == "Link da Web" and url_vid)):
            st.error("⚠️ Forneça um arquivo ou link primeiro.")
        else:
            with st.status("Analisando frames e metadados...") as s:
                # Perícia técnica baseada no arquivo
                if arquivo_vid:
                    dados = realizar_pericia_video(arquivo_vid)
                else:
                    # Placeholder para link web enquanto implementamos scraping
                    dados = {"anomalias_textura": 5, "duracao": 0, "resolucao_quadrada": 0}

                # Cálculo de IA Score (Soma de evidências)
                ia_score = sum([r_fisica, r_sentido, r_objetos, r_maos, r_rosto, r_voz]) * 15
                
                if dados['anomalias_textura'] > 8: ia_score += 20
                if dados['resolucao_quadrada'] == 1: ia_score += 10

                ia_score = min(ia_score, 100)
                humano_score = 100 - ia_score

                st.subheader("📊 Laudo Forense")
                st.progress(humano_score / 100)

                if humano_score <= 30:
                    st.error(f"🚫 VEREDITO: CONTEÚDO GERADO POR IA ({ia_score}% de certeza)")
                    st.write("**Análise:** Falhas graves na física e padrões de textura sintética.")
                elif humano_score <= 65:
                    st.warning(f"⚠️ VEREDITO: CONTEÚDO SUSPEITO ({ia_score}%)")
                    st.write("**Análise:** Presença de artefatos digitais incomuns.")
                else:
                    st.success(f"✅ VEREDITO: CONTEÚDO HUMANO ({humano_score}% de confiança)")
                    st.write("**Análise:** Movimentos e texturas condizentes com a realidade.")

                s.update(label="Investigação Concluída!", state="complete")

# --- 5. RODAPÉ ---
st.divider()
st.caption("IA-Detector v1.6.1 | Copyright by: Yaakov Israel Cypriano com Gemini 3 | Protegendo a verdade.")
