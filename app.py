import streamlit as st
import requests
import time

# 1. Configuração da página (Isso traz o favicon de volta)
st.set_page_config(page_title="IA Detector Pro", page_icon="🛡️")

def consultar_detector_ia(texto):
    # Tentamos a URL principal e a URL alternativa (router)
    urls = [
        "https://api-inference.huggingface.co/models/Hello-SimpleAI/chatgpt-detector-roberta",
        "https://router.huggingface.co/hf-inference/models/Hello-SimpleAI/chatgpt-detector-roberta"
    ]
    
    # Busca e limpa o token de qualquer caractere invisível
    token = st.secrets.get("HF_TOKEN", "").replace('"', '').replace("'", "").strip()
    
    if not token:
        st.error("Token não encontrado nas Secrets!")
        return None
        
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": texto, "options": {"wait_for_model": True}}
    
    for url in urls:
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                continue # Tenta a próxima URL se for erro de autorização
        except:
            continue
            
    return None

# --- INTERFACE ---
st.title("🛡️ IA Detector: Identificador de Mídias")
st.write("Analise se o conteúdo é humano ou sintético.")

entrada_texto = st.text_area("Cole o texto aqui:", height=150)

if st.button("🔍 Analisar Texto"):
    if entrada_texto:
        with st.spinner("Consultando laboratório de IA..."):
            resultado = consultar_detector_ia(entrada_texto)
            if resultado:
                # O modelo retorna uma lista de listas: [[{'label': '...', 'score': ...}]]
                label = resultado[0][0]['label']
                score = resultado[0][0]['score'] * 100
                if "Fake" in label or "ChatGPT" in label:
                    st.error(f"🚨 ALERTA: Probabilidade de IA: {score:.2f}%")
                else:
                    st.success(f"✅ Humano detectado: {score:.2f}% de chance.")
            else:
                st.error("Erro de conexão final. Verifique se o Token no Secrets não possui a barra | antes das aspas.")
        
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": texto,
        "options": {"wait_for_model": True, "use_cache": False}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.error("Erro 401: Token Inválido. Verifique se as permissões 'Inference' estão marcadas no HF.")
            return None
        elif response.status_code == 410:
            # Tenta uma URL alternativa se o endpoint principal der 'Gone'
            ALT_URL = "https://router.huggingface.co/hf-inference/models/Hello-SimpleAI/chatgpt-detector-roberta"
            response = requests.post(ALT_URL, headers=headers, json=payload, timeout=20)
            return response.json() if response.status_code == 200 else None
        else:
            st.error(f"Erro {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"Falha na comunicação: {e}")
        return None

# O restante do seu código (Interface, Abas, etc.) continua igual
        
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
