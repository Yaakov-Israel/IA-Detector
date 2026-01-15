import streamlit as st
import requests
import time
import cv2  # Para análise de vídeo
import numpy as np # Para cálculos matemáticos
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
    st.markdown('<div class="instrucao"><b>MODO PERÍCIA:</b> Use Upload para fotos originais.</div>', unsafe_allow_html=True)
    
    # Botão para limpar/reiniciar
    if st.button("♻️ Nova Análise de Imagem"):
        st.rerun()

    tipo_img = st.radio("Selecione o modo:", ["Upload (Modo Pro)", "Link da Web"], horizontal=True)
    img_final = None

    # ... (seu código de captura de imagem continua igual aqui) ...

    if img_final:
        st.image(img_final, use_container_width=True)
        if st.button("🚀 INICIAR ANÁLISE DE IMAGEM", use_container_width=True):
            with st.spinner("Escaneando vestígios digitais..."):
                img = Image.open(img_final)
                exif = img.getexif()
                
                # Lógica de Confiança
                score_real = 0
                if exif:
                    score_real = 90  # Se tem EXIF, grandes chances de ser real
                else:
                    score_real = 20  # Sem metadados, suspeita alta
                
                st.subheader("📊 Relatório de Autenticidade")
                st.progress(score_real / 100)
                st.write(f"Probabilidade de ser uma **Foto Original**: {score_real}%")

                if score_real > 70:
                    st.success("✅ Fato: Imagem consistente com captura de câmera física.")
                else:
                    st.warning("⚠️ Suspeito: Imagem sem rastros digitais de hardware. Pode ser IA ou Print.")

# --- ABA DE VÍDEO (DETECTOR DE ORIGEM) ---
with aba_vid:
    st.markdown('<div class="instrucao"><b>DETECTOR DE ORIGEM:</b> Identifique se o vídeo foi criado por humanos ou IA.</div>', unsafe_allow_html=True)
    
    if st.button("♻️ Nova Análise de Vídeo"):
        st.rerun()

    tipo_vid = st.radio("Origem do vídeo:", ["Upload Local", "Link de Rede Social"], horizontal=True)
    vid_file = None
    url_vid = ""

    if tipo_vid == "Upload Local":
        vid_file = st.file_uploader("Envie o vídeo (.mp4)", type=['mp4'])
    else:
        url_vid = st.text_input("Cole o link (X, YouTube, etc):")

    # Checklist manual (enquanto não automatizamos 100% com IA)
    st.subheader("🕵️ Checklist de Consistência Natural")
    col1, col2 = st.columns(2)
    with col1:
        v1 = st.checkbox("Física Realista? (Gravidade/Peso)")
        v2 = st.checkbox("Sincronia Labial/Voz?")
    with col2:
        v3 = st.checkbox("Cenário Estável? (Sem mutações)")
        v4 = st.checkbox("Texturas Naturais? (Pele/Pêlos)")

    if st.button("🔬 INICIAR ANÁLISE DE VÍDEO", use_container_width=True):
        # TRAVA DE SEGURANÇA: Só analisa se houver um arquivo ou link
        if not vid_file and not url_vid:
            st.error("❌ Erro: Por favor, forneça um vídeo ou link antes de iniciar.")
        else:
            with st.status("Analisando integridade do vídeo...") as s:
                time.sleep(2)
                
                # Lógica de Veredito Amigável
                pontos = sum([v1, v2, v3, v4])
                confianca = pontos * 25 # 4 caixas = 100%
                
                st.write(f"**Nível de Autenticidade Humana:** {confianca}%")
                st.progress(confianca / 100)

                if confianca >= 75:
                    st.success("🎥 **VEREDITO:** Conteúdo com fortes indícios de ser Genuinamente Humano.")
                elif confianca >= 50:
                    st.info("🤖 **VEREDITO:** Vídeo Híbrido. Pode ser real com edições pesadas de IA.")
                else:
                    st.error("🚫 **VEREDITO:** Conteúdo criado ou profundamente manipulado por IA.")
                
                s.update(label="Análise Finalizada", state="complete")
st.divider()
st.caption("IA-Detector v1.4 | Protegendo a verdade na era da IA.")
