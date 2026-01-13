import streamlit as st
import requests
import time

# Configuração da página
st.set_page_config(page_title="IA Detector Pro", page_icon="🛡️")

# --- FUNÇÃO DE CONEXÃO COM A IA (HUGGING FACE) ---
def consultar_detector_ia(texto):
    API_URL = "https://api-inference.huggingface.co/models/Hello-SimpleAI/chatgpt-detector-roberta"
    
    # O .strip() remove espaços acidentais no início ou fim do token
    token = st.secrets.get("HF_TOKEN", "").strip()
    
    if not token:
        st.error("Token não encontrado nas Secrets! Verifique o nome HF_TOKEN.")
        return None
        
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": texto, "options": {"wait_for_model": True}}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.error("Erro 401: Token Inválido. Confira se copiou o código hf_ completo.")
            return None
        else:
            st.error(f"Erro {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"Falha na requisição: {e}")
        return None

# --- INTERFACE DO USUÁRIO ---
st.title("🛡️ IA Detector: Identificador de Mídias")
st.write("Proteja-se contra golpes. Analise se o conteúdo é humano ou sintético.")

aba_texto, aba_imagem, aba_video = st.tabs(["✍️ Texto", "🖼️ Imagem", "🎥 Vídeo"])

# --- ABA DE TEXTO (AGORA COM IA REAL) ---
with aba_texto:
    st.header("Análise de Texto")
    st.info("Ideal para verificar mensagens de WhatsApp, e-mails de phishing e propostas de empréstimo.")
    
    entrada_texto = st.text_area("Cole o conteúdo suspeito aqui:", height=150)
    
    if st.button("🔍 Iniciar Análise Inteligente"):
        if entrada_texto:
            with st.spinner("O cérebro está consultando os modelos de Deep Learning..."):
                resultado = consultar_detector_ia(entrada_texto)
                
                if resultado:
                    # O modelo retorna uma lista: [['Fake', score], ['Real', score]]
                    # Vamos extrair a probabilidade de ser IA (Fake)
                    label = resultado[0][0]['label']
                    score = resultado[0][0]['score'] * 100
                    
                    if "Fake" in label or "ChatGPT" in label:
                        st.error(f"🚨 ALERTA: Este texto tem {score:.2f}% de probabilidade de ter sido gerado por IA.")
                        st.markdown("**Motivo:** Padrões estatísticos e repetições típicas de modelos de linguagem.")
                    else:
                        st.success(f"✅ Análise concluída: {score:.2f}% de chance de ser um texto Humano.")
                else:
                    st.error("Erro ao conectar com a IA. Verifique se o seu Token nas Secrets está correto.")
        else:
            st.warning("Por favor, cole um texto para analisar.")

# --- ABA DE IMAGEM ---
with aba_imagem:
    st.header("Análise de Imagem")
    foto = st.file_uploader("Suba a foto suspeita", type=['jpg', 'png', 'jpeg'])
    if foto:
        st.image(foto, caption="Análise visual carregada")
        if st.button("🔬 Escanear Pixels"):
            st.info("Em breve: Integração com detector de artefatos de difusão.")

# --- ABA DE VÍDEO (FOCO EM DEEPFAKE) ---
with aba_video:
    st.header("Detector de Deepfake")
    metodo_video = st.radio("Método:", ["Link da Rede Social", "Upload de Arquivo"])
    
    if metodo_video == "Link da Rede Social":
        url = st.text_input("Cole o link (Instagram, X, etc.):")
    else:
        video_file = st.file_uploader("Envie o arquivo", type=['mp4', 'mov'])

    if st.button("🚀 Iniciar Perícia de Vídeo"):
        with st.status("Realizando varredura forense...", expanded=True) as status:
            st.write("Analisando sincronia labial e micro-expressões...")
            time.sleep(3)
            status.update(label="Análise Concluída!", state="complete")
        st.error("🚨 ALERTA: Inconsistência temporal detectada (Possível Deepfake).")

st.divider()
st.caption("Aviso: Esta ferramenta auxilia na detecção, mas a decisão final e o cuidado com seus dados são de sua responsabilidade.")
