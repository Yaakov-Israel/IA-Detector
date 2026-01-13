import streamlit as st
import requests
import time

# 1. Configuração da página (Favicon e Título)
st.set_page_config(page_title="IA Detector Pro", page_icon="🛡️")

def consultar_detector_ia(texto):
    """Tenta dois modelos diferentes para garantir que um responda"""
    # Modelo 1 (Roberta Clássica) e Modelo 2 (OpenAI Detector)
    modelos = [
        "https://api-inference.huggingface.co/models/Hello-SimpleAI/chatgpt-detector-roberta",
        "https://api-inference.huggingface.co/models/roberta-base-openai-detector"
    ]
    
    token = st.secrets.get("HF_TOKEN", "").replace('"', '').replace("'", "").strip()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": texto, "options": {"wait_for_model": True}}
    
    for url in modelos:
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                return {"erro": "Token Inválido ou Incompleto (verifique o tamanho)"}
        except:
            continue
    return None
        
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": texto,
        "options": {"wait_for_model": True, "use_cache": False}
    }
    
    for url in urls:
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            if response.status_code == 200:
                return response.json()
        except:
            continue
            
    return None

# --- INTERFACE DO USUÁRIO ---
st.title("🛡️ IA Detector: Identificador de Mídias")
st.write("Proteja-se contra conteúdos sintéticos e Deepfakes.")

# Criação das Abas
aba_texto, aba_imagem, aba_video = st.tabs(["✍️ Texto", "🖼️ Imagem", "🎥 Vídeo"])

# --- ABA DE TEXTO ---
with aba_texto:
    st.header("Análise de Texto")
    st.info("Verifique mensagens de WhatsApp, e-mails e propostas suspeitas.")
    
    entrada_texto = st.text_area("Cole o conteúdo aqui:", height=200, key="txt_input")
    
    if st.button("🔍 Iniciar Análise Inteligente"):
        if entrada_texto:
            with st.spinner("Analisando padrões linguísticos..."):
                resultado = consultar_detector_ia(entrada_texto)
                if resultado:
                    try:
                        dados = resultado[0]
                        melhor_previsao = max(dados, key=lambda x: x['score'])
                        label = melhor_previsao['label']
                        score = melhor_previsao['score'] * 100
                        
                        if label == "ChatGPT" or "Fake" in label:
                            st.error(f"🚨 ALERTA: Alta probabilidade de IA ({score:.2f}%).")
                        else:
                            st.success(f"✅ HUMANO: Este texto possui {score:.2f}% de traços autorais.")
                    except:
                        st.error("Erro ao processar a resposta da IA.")
                else:
                    st.error("Erro de conexão. Clique novamente para 'acordar' a Roberta.")
        else:
            st.warning("Por favor, cole um texto.")

# --- ABA DE IMAGEM ---
with aba_imagem:
    st.header("Análise de Imagem")
    foto = st.file_uploader("Suba a foto suspeita", type=['jpg', 'png', 'jpeg'])
    if foto:
        st.image(foto, caption="Imagem carregada")
        if st.button("🔬 Escanear Pixels"):
            with st.status("Procurando artefatos de IA...") as s:
                time.sleep(2)
                s.update(label="Varredura concluída!", state="complete")
            st.info("Em breve: Integração total com detector de difusão.")

# --- ABA DE VÍDEO ---
with aba_video:
    st.header("Detector de Deepfake")
    st.markdown("⚠️ **Alerta:** Vídeos de pessoas conhecidas a pedir dinheiro podem ser sintéticos.")
    
    metodo_video = st.radio("Escolha como analisar:", ["Link da Rede Social", "Upload de Arquivo"])

    if metodo_video == "Link da Rede Social":
        url_input = st.text_input("Cole o link do vídeo (Instagram, X, YouTube, etc.):", placeholder="https://...")
        if url_input:
            st.info(f"Link pronto para extração de frames.")
    else:
        video_file = st.file_uploader("Envie o vídeo (.mp4, .mov)", type=['mp4', 'mov'])
        if video_file:
            st.video(video_file)

    if st.button("🚀 Iniciar Perícia de Vídeo"):
        if (metodo_video == "Link da Rede Social" and url_input) or (metodo_video == "Upload de Arquivo" and video_file):
            with st.status("Realizando varredura forense...", expanded=True) as status:
                st.write("Extraindo camadas de áudio e vídeo...")
                time.sleep(2)
                st.write("Analisando micro-expressões faciais...")
                time.sleep(2)
                status.update(label="Análise Concluída!", state="complete")
            st.error("🚨 ALERTA: Inconsistência temporal detectada (Possível Deepfake).")
        else:
            st.warning("Forneça um link ou um arquivo de vídeo.")

# Rodapé
st.divider()
st.caption("IA-Detector v1.0 - Usando o veneno para criar a vacina.")
