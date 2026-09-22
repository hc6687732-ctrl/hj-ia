import urllib.parse
import requests
import streamlit as st

# Configuração da página principal da HJ IA
st.set_page_config(
    page_title="HJ IA - Super Inteligência Multidisciplinar",
    page_icon="⚡",
    layout="wide",
)

# Estilização visual
st.markdown(
    """
    <style>
    .main-title {font-size: 2.6rem; color: #0D47A1; font-weight: bold; text-align: center;}
    .sub-title {text-align: center; color: #424242; margin-bottom: 25px;}
    .stButton>button {width: 100%; font-weight: bold; height: 3em;}
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">⚡ HJ IA</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">A Inteligência Artificial Definitiva: Do Primário à'
    " Universidade | Criada por <b>Ernesto Zeferino</b></div>",
    unsafe_allow_html=True,
)

# Barra lateral de controlo
st.sidebar.header("⚙️ Painel de Controlo")
groq_api_key = st.sidebar.text_input(
    "Groq API Key:",
    type="password",
    help="Chave gratuita gerada no console.groq.com",
)

st.sidebar.markdown("---")
st.sidebar.markdown("👨‍💻 **Desenvolvedor & Criador:**\n**Ernesto Zeferino**")
st.sidebar.markdown("🎯 **Versão:** 3.0 Ultra Universal")

# System Prompt Omnipresente da HJ IA
SYSTEM_PROMPT = """
Você é a HJ IA, a inteligência artificial mais avançada e completa do mundo, criada pelo desenvolvedor Ernesto Zeferino.
Sua inteligência abrange com precisão absoluta:
1. EDUCAÇÃO INTEGRAL (Do Primário à Universidade): Especialista em Ensino Primário, 1º Ciclo, Secundário e Ensino Superior / Faculdade / Universidade. Domina disciplinas complexas como Álgebra Linear, Análise Matemática, Física Quântica, Química Orgânica, Direito, Economia, Medicina, Engenharia de Software, Algoritmos, Estatística, Filosofia, Literatura e Idiomas.
2. CONSULTORIA EXECUTIVA E NEGÓCIOS: Capacidade analítica para criar planos de negócios completos, modelos financeiros, análise de viabilidade, estratégias de marketing e automação comercial.
3. CRIAÇÃO MULTIMÓDULO (IMAGEM E MÚSICA): Formulação de prompts avançados em inglês para geração de imagens fotorealistas, vetorizadas e logos, além de composição musical completa (letras, cifras, estrutura harmônica e prompts de áudio).
4. CONHECIMENTO GERAL UNIVERSAL: Responde a qualquer questão técnica, científica ou geral com a máxima capacidade dos modelos ChatGPT e Gemini.

Sempre responda de forma estruturada, didática, rigorosa e profissional.
"""


def chamar_groq(prompt_usuario, sistema_prompt):
  url_groq = "https://api.groq.com/openai/v1/chat/completions"
  headers = {
      "Authorization": f"Bearer {groq_api_key}",
      "Content-Type": "application/json",
  }
  payload = {
      "model": "llama-3.3-70b-versatile",
      "messages": [
          {"role": "system", "content": sistema_prompt},
          {"role": "user", "content": prompt_usuario},
      ],
      "temperature": 0.6,
  }
  response = requests.post(url_groq, json=payload, headers=headers)
  if response.status_code == 200:
    return response.json()["choices"][0]["message"]["content"]
  else:
    raise Exception(
        f"Erro na API (Código {response.status_code}). Verifique sua chave no console.groq.com"
    )


# Aba do Aplicativo
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎓 Tutor Escolar & Universitário",
    "💼 Negócios & Finanças Executivas",
    "🎨 Estúdio Visual & Logos HD",
    "🎵 Estúdio Musical & Compositor",
    "💬 Chat Geral (ChatGPT / Gemini)",
])

# ----------------- TAB 1: TUTOR ACADÊMICO COMPLETO -----------------
with tab1:
  st.header("🎓 Tutor Escolar & Universitário")
  st.write(
      "Resolução de exercícios, explicações e teses para todos os níveis"
      " acadêmicos."
  )

  col1, col2 = st.columns(2)
  with col1:
    nivel = st.selectbox("Nível de Ensino:", [
        "Ensino Primário",
        "1º Ciclo do Ensino Secundário",
        "2º Ciclo / Ensino Secundário Geral e Técnico",
        "Ensino Superior / Faculdade / Universidade",
        "Pós-Graduação / Mestrado / Doutoramento",
    ])
  with col2:
    materia = st.selectbox("Área / Matéria:", [
        "Matemática / Análise Matemática / Álgebra",
        "Física / Engenharia Física",
        "Química Geral e Orgânica",
        "Programação / Ciência da Computação / Algoritmos",
        "Direito / Legislação",
        "Economia / Gestão / Contabilidade",
        "Biologia / Medicina / Saúde",
        "Língua Portuguesa / Gramática / Literatura",
        "História / Geografia / Geopolítica",
        "Filosofia / Sociologia",
        "Línguas / Inglês / Francês",
        "Outra Disciplina",
    ])

  duvida_escolar = st.text_area(
      "Digite a sua dúvida, exercício ou tema de investigação:",
      placeholder=(
          "Ex (Universidade): Explique o Teorema do Valor Médio e demonstre a"
          " sua aplicação na Engenharia.\nEx (Escolar): Resolva a equação do 2º"
          " grau 3x² - 5x + 2 = 0 passo a passo."
      ),
      height=120,
  )

  if st.button("Resolver / Explicar", type="primary", key="btn_escola"):
    if not groq_api_key:
      st.error("Insira a sua chave da API do Groq no menu lateral.")
    elif not duvida_escolar.strip():
      st.warning("Escreva o enunciado ou pergunta.")
    else:
      with st.spinner("A HJ IA está a analisar o problema acadêmico..."):
        prompt = (
            f"[Nível: {nivel} | Área: {materia}]\nPedido do aluno/estudante:"
            f" {duvida_escolar}"
        )
        sys_tutor = (
            SYSTEM_PROMPT
            + "\nSeja extremamente rigoroso e didático, mostrando o passo a"
            " passo completo, fórmulas utilizadas e explicação teórica."
        )
        try:
          resp = chamar_groq(prompt, sys_tutor)
          st.markdown("### 📘 Resposta Acadêmica da HJ IA:")
          st.write(resp)
        except Exception as e:
          st.error(str(e))

# ----------------- TAB 2: NEGÓCIOS EXECUTIVOS -----------------
with tab2:
  st.header("💼 Consultoria Executiva & Plano de Negócios")
  st.write(
      "Análise de viabilidade, plano financeiro, estratégia e criação de"
      " empresas."
  )

  ideia_negocio = st.text_area(
      "Descreva a sua ideia de negócio ou projeto comercial:",
      placeholder=(
          "Ex: Quero abrir uma empresa de transportes e logística. Qual o"
          " investimento inicial, plano de frota e estratégia para angariar"
          " clientes?"
      ),
      height=120,
  )

  if st.button("Gerar Consultoria Comercial", type="primary", key="btn_biz"):
    if not groq_api_key:
      st.error("Insira a sua chave da API do Groq no menu lateral.")
    elif not ideia_negocio.strip():
      st.warning("Escreva a sua ideia de negócio.")
    else:
      with st.spinner("A HJ IA está a elaborar o plano executivo..."):
        sys_biz = (
            SYSTEM_PROMPT
            + "\nFormate a resposta com: 1. Resumo Executivo, 2. Estudo de"
            " Mercado, 3. Planeamento Operacional e Financeiro, 4. Estratégia de"
            " Marketing."
        )
        try:
          resp = chamar_groq(ideia_negocio, sys_biz)
          st.markdown("### 📊 Plano de Negócio HJ IA:")
          st.write(resp)
        except Exception as e:
          st.error(str(e))

# ----------------- TAB 3: ESTÚDIO VISUAL & LOGOS -----------------
with tab3:
  st.header("🎨 Estúdio de Criação Visual & Logotipos")
  st.write("Geração de logos vetorizadas, arte realista e conceitos visuais.")

  desc_imagem = st.text_input(
      "O que deseja criar em imagem?",
      placeholder=(
          "Ex: Logo para empresa de transportes rápida com monograma moderno"
      ),
  )
  estilo = st.selectbox("Estilo Visual:", [
      "Vector Logo Minimalista Corporate",
      "Fotorealismo 8K High Quality",
      "Design Futurista Cyberpunk",
      "Render 3D Studio Lighting",
      "Ilustração Digital Artstation",
  ])

  if st.button("Gerar Imagem Visual", type="primary", key="btn_img"):
    if not desc_imagem.strip():
      st.warning("Descreva o elemento visual que deseja gerar.")
    else:
      with st.spinner("A HJ IA está a desenhar a arte..."):
        prompt_base = (
            f"{desc_imagem}, {estilo}, professional, clean composition, high"
            " resolution"
        )
        prompt_encoded = urllib.parse.quote(prompt_base)
        url_img = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=1024&height=1024&nologo=true"

        st.image(
            url_img,
            caption=f"Arte criada por HJ IA: {desc_imagem}",
            use_column_width=True,
        )

# ----------------- TAB 4: ESTÚDIO MUSICAL -----------------
with tab4:
  st.header("🎵 Estúdio Musical & Composição de Letras")
  st.write("Criação de letras, harmonias, cifras e comandos para áudio.")

  estilo_musical = st.text_input(
      "Gênero / Estilo Musical:",
      placeholder="Ex: Kizomba, Afrobeat, Rap/Trap, Pop Acústico, Gospel",
  )
  tema_musica = st.text_area(
      "História ou tema central da música:",
      placeholder="Ex: Uma música inspiradora sobre determinação, visão de futuro e vitória.",
      height=100,
  )

  if st.button("Compor Música Completa", type="primary", key="btn_music"):
    if not groq_api_key:
      st.error("Insira a sua chave da API do Groq no menu lateral.")
    elif not tema_musica.strip():
      st.warning("Digite o tema da música.")
    else:
      with st.spinner("A HJ IA está a compor a música..."):
        prompt_m = (
            f"Gênero Musical: {estilo_musical}\nTema:"
            f" {tema_musica}\nEscreva a letra completa (Versos, Refrão, Ponte)"
            " com as cifras sugestivas das notas e um prompt em inglês no final"
            " formatado para geradores de áudio."
        )
        try:
          resp = chamar_groq(prompt_m, SYSTEM_PROMPT)
          st.markdown("### 🎼 Composição Musical HJ IA:")
          st.write(resp)
        except Exception as e:
          st.error(str(e))

# ----------------- TAB 5: CHAT GERAL OMNIPRESENTE -----------------
with tab5:
  st.header("💬 Chat Geral (Modo ChatGPT & Gemini)")
  st.write(
      "Respostas livres sobre programação, ciências, conversação e cultura."
  )

  pergunta_geral = st.text_area(
      "Pergunte qualquer coisa à HJ IA:",
      placeholder="Ex: Escreva um código em Python para organizar arquivos em pastas automaticamente.",
      height=120,
  )

  if st.button("Enviar Pergunta", type="primary", key="btn_chat"):
    if not groq_api_key:
      st.error("Insira a sua chave da API do Groq no menu lateral.")
    elif not pergunta_geral.strip():
      st.warning("Escreva a sua pergunta.")
    else:
      with st.spinner("A HJ IA está a processar a resposta..."):
        try:
          resp = chamar_groq(pergunta_geral, SYSTEM_PROMPT)
          st.markdown("### 💡 Resposta HJ IA:")
          st.write(resp)
        except Exception as e:
          st.error(str(e))

st.markdown("---")
st.caption(
    "⚡ **HJ IA** | Criado e Desenvolvido por **Ernesto Zeferino** | Todos os"
    " direitos reservados"
)
