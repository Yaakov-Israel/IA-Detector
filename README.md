# 🛡️ IA-Detector (BETA)
### A verdade por trás dos pixels.

O **IA-Detector** é uma ferramenta de perícia digital experimental desenvolvida para identificar manipulações em imagens e vídeos. Nosso foco é o combate à desinformação e a preservação da verdade histórica, especialmente em contextos sensíveis como o trabalho do **Yad Vashem**.

---

## 🔍 O que o nosso "Pupilo" faz?

O sistema utiliza técnicas avançadas de análise forense digital, incluindo:

* **ELA (Error Level Analysis):** Identifica diferentes níveis de compressão na imagem para detectar montagens (ex: elementos inseridos via Canva ou Photoshop).
* **Análise de Metadados (EXIF):** Rastreia a "impressão digital" da câmera original.
* **Detecção de Micro-textura:** Analisa padrões de pixels para identificar conteúdos gerados por IAs (Sora, Kling, Runway, DALL-E, etc).
* **Consistência Temporal:** Análise de frames para identificação de Deepfakes em vídeo.

---

## 🚀 Status do Projeto: BETA

Atualmente, o projeto está em fase de **Stress Test** e aprendizado. 
* **Fotos "Cruas":** Alta precisão em capturas diretas de câmera.
* **Redes Sociais:** O sistema está sendo calibrado para diferenciar compressão do X/WhatsApp de manipulações maliciosas.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Interface:** Streamlit
* **Bibliotecas Forenses:** OpenCV, PIL (Pillow), NumPy.

---

## ⚖️ Compromisso Ético
Este projeto visa fortalecer a integridade da informação. Não armazenamos as imagens enviadas para garantir a privacidade dos usuários.
