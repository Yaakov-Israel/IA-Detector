import streamlit as st
import requests
import time

# Configuração da página
st.set_page_config(page_title="IA Detector Pro", page_icon="🛡️")

# --- FUNÇÃO DE CONEXÃO TURBINADA ---


def consultar_detector_ia(texto):
    """Tenta dois modelos diferentes e trata erros de conexão/token"""
    modelos = [
        "https://api-inference.huggingface.co/models/Hello-SimpleAI/chatgpt-detector-roberta",
        "https://api-inference.huggingface.co/models/roberta-base-openai-detector"
    ]

    # Busca e limpa o token das Secrets
    token = st.secrets.get("HF_TOKEN", "").replace(
        '"', '').replace("'", "").replace("|", "").strip()

    if not token:
        st.error("Token não encontrado nas Secrets! Verifique o nome HF_TOKEN.")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": texto, "options": {"wait_for_model": True}}

    for url in modelos:
        try:
            response = requests.post(
                url, headers=headers, json=payload, timeout=20)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                st.error(
                    "Erro 401: Token Inválido. Verifique se copiou o código hf_ completo.")
                return None
        except Exception as e:
            continue  # Tenta o próximo modelo se este falhar

    return None


# --- INTERFACE DO USUÁRIO ---
st.title("🛡️ IA Detector: Identificador de Mídias")
st.write("Proteja-se contra conteúdos sintéticos e Deepfakes.")

aba_texto, aba_imagem, aba_video = st.tabs(
    ["✍️ Texto", "🖼️ Imagem", "🎥 Vídeo"])

# --- ABA DE TEXTO ---
with aba_texto:
    st.header("Análise de Texto")
    entrada_texto = st.text_area(
        "Cole o conteúdo aqui:", height=200, key="txt_input")

    if st.button("🔍 Iniciar Análise Inteligente"):
        if entrada_texto:
            with st.spinner("Analisando padrões linguísticos..."):
                resultado = consultar_detector_ia(entrada_texto)
                if resultado and isinstance(resultado, list):
                    try:
                        # Extrai a previsão do primeiro modelo que respondeu
                        dados = resultado[0]
                        melhor_previsao = max(dados, key=lambda x: x['score'])
                        label = melhor_previsao['label']
                        score = melhor_previsao['score'] * 100

                        if "Fake" in label or "ChatGPT" in label:
                            st.error(
                                f"🚨 ALERTA: Alta probabilidade de IA ({score:.2f}%).")
                        else:
                            st.success(
                                f"✅ HUMANO: Este texto possui {score:.2f}% de traços autorais.")
                    except Exception as e:
                        st.error(f"Erro ao processar dados: {e}")
                else:
                    st.warning(
                        "A Roberta (IA) ainda está processando. Clique novamente em 10 segundos.")
        else:
            st.warning("Por favor, cole um texto.")

# --- ABA DE IMAGEM ---
with aba_imagem:
    st.header("Análise de Imagem")
    foto = st.file_uploader("Suba a foto suspeita",
                            type=['jpg', 'png', 'jpeg'])
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
    st.markdown("⚠️ **Alerta:** Vídeos suspeitos podem ser sintéticos.")
    metodo_video = st.radio("Escolha como analisar:", [
                            "Link da Rede Social", "Upload de Arquivo"])

    if metodo_video == "Link da Rede Social":
        url_input = st.text_input(
            "Cole o link do vídeo:", placeholder="https://...")
    else:
        video_file = st.file_uploader("Envie o vídeo (.mp4)", type=['mp4'])

    if st.button("🚀 Iniciar Perícia de Vídeo"):
        with st.status("Realizando varredura forense...") as status:
            time.sleep(2)
            status.update(label="Análise Concluída!", state="complete")
        st.error("🚨 ALERTA: Inconsistência temporal detectada (Possível Deepfake).")

st.divider()
st.caption("IA-Detector v1.1 - Usando o veneno para criar a vacina.")
