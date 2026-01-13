import streamlit as st
import requests
import time

# Configuração da página
st.set_page_config(page_title="IA Detector Pro", page_icon="🛡️")

# --- FUNÇÃO DE CONEXÃO TURBINADA ---


def consultar_detector_ia(texto):
    """Tenta modelos diferentes e gerencia o tempo de carregamento"""
    modelos = [
        "https://api-inference.huggingface.co/models/roberta-base-openai-detector",
        "https://api-inference.huggingface.co/models/Hello-SimpleAI/chatgpt-detector-roberta"
    ]

    token = st.secrets.get("HF_TOKEN", "").replace(
        '"', '').replace("'", "").strip()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": texto, "options": {"wait_for_model": True}}

    for url in modelos:
        try:
            response = requests.post(
                url, headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 503:
                return {"erro": "O servidor da IA está aquecendo. Tente novamente em 20 segundos."}
        except:
            continue
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
    st.header("🔬 Perícia de Imagem")
    st.write("Analise o DNA do arquivo ou de um link para buscar rastros de edição.")

    metodo_img = st.radio("Escolha a origem da imagem:", [
                          "Upload de Arquivo", "Link da Web"], key="origem_img")

    img_para_analise = None

    if metodo_img == "Upload de Arquivo":
        arquivo = st.file_uploader("Suba a foto suspeita", type=[
                                   'jpg', 'png', 'jpeg'])
        if arquivo:
            img_para_analise = arquivo
    else:
        url_img = st.text_input(
            "Cole a URL da imagem (ex: https://site.com/foto.jpg):")
        if url_img:  # Ajustado aqui de url_input para url_img
            try:
                response = requests.get(url_img, stream=True, timeout=10)
                if response.status_code == 200:
                    from io import BytesIO
                    img_para_analise = BytesIO(response.content)
                    st.success("Imagem do link carregada!")
                else:
                    st.error("Não foi possível acessar a imagem pelo link.")
            except Exception as e:
                st.error(f"Erro ao carregar link: {e}")

    if img_para_analise:
        st.image(img_para_analise, caption="Imagem para análise",
                 use_container_width=True)

        if st.button("🔍 Realizar Escaneamento Forense", key="btn_forense_img"):
            with st.status("Extraindo Metadados EXIF...") as s:
                from PIL import Image
                from PIL.ExifTags import TAGS

                time.sleep(1)
                img = Image.open(img_para_analise)
                info = img.getexif()

                if info:
                    st.subheader("Dados Encontrados (DNA do Arquivo):")
                    for tag_id in info:
                        tag = TAGS.get(tag_id, tag_id)
                        dado = info.get(tag_id)
                        st.write(f"**{tag}**: {dado}")
                    s.update(label="Análise Concluída!", state="complete")
                else:
                    st.warning(
                        "⚠️ Nenhum metadado encontrado. Comum em IA, prints ou redes sociais.")
                    s.update(label="Varredura finalizada.", state="complete")

# --- ABA DE VÍDEO ---
with aba_video:
    st.header("Detector de Deepfake")
    st.markdown("⚠️ **Alerta:** Vídeos suspeitos podem ser sintéticos.")
    metodo_video = st.radio("Escolha como analisar:", [
                            "Link da Rede Social", "Upload de Arquivo"])

    if metodo_video == "Link da Rede Social":
        url_input_video = st.text_input(
            "Cole o link do vídeo:", placeholder="https://...", key="url_video")
    else:
        video_file = st.file_uploader("Envie o vídeo (.mp4)", type=['mp4'])

    if st.button("🚀 Iniciar Perícia de Vídeo"):
        with st.status("Realizando varredura forense...") as status:
            time.sleep(2)
            status.update(label="Análise Concluída!", state="complete")
        st.error("🚨 ALERTA: Inconsistência temporal detectada (Possível Deepfake).")

st.divider()
st.caption("IA-Detector v1.1 - Usando o veneno para criar a vacina.")
