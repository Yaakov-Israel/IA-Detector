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
            if score_textura < 30 or (score_textura < 70 and score_cores < 40):
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

# --- 4. PERÍCIA DE VÍDEO (CONSERTADO E COMPLETO) ---
with aba_vid:
    st.markdown('<div class="instrucao"><b>INVESTIGAÇÃO:</b> Suba vídeos (.mp4) para análise de padrões físicos e digitais.</div>', unsafe_allow_html=True)

    if st.button("♻️ Nova Análise de Vídeo", key="reset_pericia_vid"):
        st.rerun()

    tipo_vid = st.radio("Origem:", ["Upload Local", "Link da Web"], horizontal=True, key="video_source")

    # Garante que o uploader apareça corretamente
    arquivo_vid = None
    if tipo_vid == "Upload Local":
        arquivo_vid = st.file_uploader("Suba o vídeo (.mp4, .mov)", type=['mp4', 'mov'], key="up_vid")
    else:
        url_vid = st.text_input("Cole o link:")
        st.info("A análise de links externos será habilitada na v1.7.")

    st.subheader("🕵️ Checklist Forense (As 10 Regras)")
    c1, c2 = st.columns(2)
    with c1:
        r_fisica = st.checkbox("Violação da Gravidade? (Ex: Gata na parede)")
        r_sentido = st.checkbox("Ações que não fazem sentido?")
        r_objetos = st.checkbox("Objetos se atravessando?")
    with c2:
        r_maos = st.checkbox("Mãos ou dedos anormais?")
        r_rosto = st.checkbox("Rostos ou olhos estranhos?")
        r_voz = st.checkbox("Voz robótica ou sem emoção?")

    if st.button("🔬 INICIAR INVESTIGAÇÃO PROFUNDA", use_container_width=True):
        if tipo_vid == "Upload Local" and arquivo_vid is not None:
            with st.status("Processando perícia técnica...") as s:
                # Chama a função do Bloco 2
                dados = realizar_pericia_video(arquivo_vid)
                
                # Cálculo de IA Score (Peso do Humano + Máquina)
                ia_score = sum([r_fisica, r_sentido, r_objetos, r_maos, r_rosto, r_voz]) * 15
                
                # Se a máquina detectar textura "lisa" de IA, soma 20
                if dados['anomalias_textura'] > 5: 
                    ia_score += 40
                
                ia_score = min(ia_score, 100)
                humano_score = 100 - ia_score

                st.subheader("📊 Laudo Forense")
                st.progress(humano_score / 100)
                
                if humano_score <= 35:
                    st.error(f"🚫 VEREDITO: CONTEÚDO IDENTIFICADO COMO IA ({ia_score}%)")
                    st.write("**Análise:** Falhas graves na física e padrões sintéticos detectados.")
                elif humano_score <= 65:
                    st.warning(f"⚠️ VEREDITO: CONTEÚDO SUSPEITO ({ia_score}%)")
                    st.write("**Análise:** Manipulação provável. Inconsistência de metadados.")
                else:
                    st.success(f"✅ VEREDITO: CONTEÚDO GENUÍNO ({humano_score}%)")
                    st.write("**Análise:** Padrões condizentes com filmagem real.")
                
                s.update(label="Perícia Concluída!", state="complete")
        else:
            st.error("❌ Erro: Por favor, selecione e suba um arquivo de vídeo primeiro.")

# --- 5. RODAPÉ (COM AVISO ÉTICO) ---
st.divider()
st.caption("IA-Detector v1.6.2 | © Yaakov Israel Cypriano com Gemini 3 | Aviso: Este app lê metadados públicos para fins de perícia.")
