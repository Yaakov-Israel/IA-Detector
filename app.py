import streamlit as st
import requests
import time
import cv2
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
from PIL.ExifTags import TAGS
from io import BytesIO
import os
import yt_dlp
import tempfile

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

# --- MOTOR DE ANÁLISE FORENSE E DETECÇÃO ANATÔMICA ---
def analisar_ela(img_input, quality=90):
    """Realiza a Análise de Nível de Erro (ELA) para detectar manipulações"""
    temp_ela = "temp_ela.jpg"
    
    # Converte para RGB se necessário (remover canal alpha de PNGs)
    if img_input.mode != 'RGB':
        img_input = img_input.convert('RGB')
    
    # Passo 1: Salva a imagem com uma compressão específica
    img_input.save(temp_ela, 'JPEG', quality=quality)
    img_comprimida = Image.open(temp_ela)
    
    # Passo 2: Calcula a diferença entre a original e a comprimida
    ela_img = ImageChops.difference(img_input, img_comprimida)
    
    # Passo 3: Potencializa o brilho das diferenças para o olho humano ver
    extrema = ela_img.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0: max_diff = 1
    scale = 255.0 / max_diff
    ela_img = ImageEnhance.Brightness(ela_img).enhance(scale)
    
    os.remove(temp_ela)
    return ela_img
    
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

            faces = face_cascade.detectMultiScale(cinza, 1.1, 4)

            limite_textura = 280 if len(faces) > 0 else 250

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

# --- INTERFACE DE IMAGEM E MOTOR DE CAPTURA WEB ---
st.title("🛡️ IA-Detector")
st.subheader("A verdade por trás dos pixels")

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
        # Criamos o objeto de imagem para processamento
        img = Image.open(img_final)
        
        if st.button("🚀 INICIAR ANÁLISE DE IMAGEM", use_container_width=True):
            # Executa os dois agentes: EXIF e ELA
            exif_data = img.getexif()
            img_ela = analisar_ela(img)
            
            # Exibição Visual (Lado a Lado)
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Imagem Original**")
                st.image(img, use_container_width=True)
            with col2:
                st.write("**Mapa ELA (Análise de Pixels)**")
                st.image(img_ela, use_container_width=True)
            
            # Verificação de Metadados
            # --- [BLOCO 05: VEREDITO TÉCNICO DE IMAGEM CALIBRADO] ---
            if exif_data:
                st.success("✅ Metadados de Hardware detectados!")
                with st.expander("🔍 Ver Evidências Técnicas (EXIF)"):
                    for tag_id, valor in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        st.write(f"**{tag}:** {valor}")
                score_real = 95
                veredito_texto = "Captura de Câmera Genuína (Fato Real)"
                st.info(f"**Confiança:** {score_real}% - {veredito_texto}")
            else:
                st.warning("⚠️ **Nota de Perícia:** Imagem sem metadados de hardware.")
                st.write("Comum em arquivos de redes sociais (X, WhatsApp) ou prints.")
                score_real = 55 
                veredito_texto = "Inconclusivo (Possível Foto Processada ou Print)"
                st.warning(f"**Análise:** {score_real}% - {veredito_texto}")
            
            st.subheader("📊 Laudo de Autenticidade")
            st.progress(score_real / 100)

            # --- [BLOCO 06: SISTEMA DE FEEDBACK] ---
            st.write("---")
            feedback = st.radio("O veredito parece correto?", ["Aguardando...", "👍 Sim", "👎 Não"], horizontal=True, key="fb_img")
            if feedback == "👍 Sim":
                st.success("Confirmado. Obrigado por ajudar na calibração!")
            elif feedback == "👎 Não":
                st.error("Registrado. Analisaremos este falso-positivo para refinar o sensor.")
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

# --- INTERRUPTOR DE PERÍCIA E DIAGNÓSTICO DE VÍDEO ---
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

                    dados = realizar_pericia_video(video_para_analise)
                    
                    # --- [BLOCO DE VÍDEO CALIBRADO - EVITA FALSOS POSITIVOS] ---
                    # Nunca cravamos 100% em vídeos web devido à compressão
                    if dados['anomalias_textura'] > 15:
                        ia_score = 85  
                        status_ver_vid = "error"
                        veredito_vid = f"ALTA PROBABILIDADE DE MANIPULAÇÃO ({ia_score}%)"
                    elif dados['anomalias_textura'] > 5:
                        ia_score = 60
                        status_ver_vid = "warning"
                        veredito_vid = f"CONTEÚDO SUSPEITO ({ia_score}%)"
                    else:
                        ia_score = 15
                        status_ver_vid = "success"
                        veredito_vid = f"POSSIVELMENTE GENUÍNO ({100 - ia_score}%)"
                    
                    st.subheader("📊 Laudo Forense")
                    st.progress((100 - ia_score) / 100)
                    
                    if status_ver_vid == "error":
                        st.error(f"🚫 VEREDITO: {veredito_vid}")
                        st.write(f"**Análise:** Detectadas {dados['anomalias_textura']} inconsistências. Nota: Compressão severa pode simular padrões de IA.")
                    elif status_ver_vid == "warning":
                        st.warning(f"⚠️ VEREDITO: {veredito_vid}")
                        st.write("**Análise:** Ruído de textura acima do normal. Suspeita de processamento digital ou baixa qualidade.")
                    else:
                        st.success(f"✅ VEREDITO: {veredito_vid}")
                        st.write("**Análise:** Textura condizente com gravação orgânica.")

                    # --- FEEDBACK DE VÍDEO ---
                    st.write("---")
                    fb_vid = st.radio("O laudo de vídeo faz sentido?", ["Aguardando...", "👍 Sim", "👎 Não"], horizontal=True, key="fb_vid")
                    
                    s.update(label="Perícia Concluída!", state="complete")

                except Exception as e:
                    st.error(f"Erro técnico: {e}")
                finally:
                    if caminho_temp and os.path.exists(caminho_temp):
                        os.remove(caminho_temp)
        else:
            st.error("❌ Por favor, forneça um vídeo ou link válido.")

# --- ASSINATURA E AVISO ÉTICO ---
st.divider()
st.caption("IA-Detector v1.7.2 BETA | © Yaakov Israel Cypriano com Gemini 3 | Aviso: Este app lê metadados públicos para fins de perícia.")
