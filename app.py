import os
import requests
import streamlit as st

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA & TEMA ESCURO WHITE-LABEL (HJ IA)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="HJ IA",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilização CSS e ocultação do Streamlit
st.markdown(
    """
    <style>
    /* Ocultar elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fundo Escuro */
    .stApp {
        background-color: #0D1117;
        color: #F0F6FC;
    }
    
    /* Botões Dourados */
    .stButton>button {
        background: linear-gradient(90deg, #FFD700 0%, #FF8C00 100%);
        color: #000000 !important;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        width: 100%;
        padding: 10px;
    }
    .stButton>button:hover {
        transform: scale(1.01);
        box-shadow: 0px 4px 12px rgba(255, 215, 0, 0.4);
    }
    
    /* Caixas de Paywall e Pagamento */
    .paywall-box {
        border: 2px solid #FFD700;
        background-color: #161B22;
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
    }
    .payment-card {
        background-color: #0D1117;
        border: 1px solid #30363D;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    
    /* Inputs de Texto */
    .stTextInput input, .stTextArea textarea {
        background-color: #161B22 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1px solid #30363D !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. DEFINIÇÃO DE SEGREDOS, PLANOS E DADOS DE PAGAMENTO
# -----------------------------------------------------------------------------
AIRTM_EMAIL = st.secrets.get("AIRTM_EMAIL", "teu-email-airtm@gmail.com")
PAYPAL_EMAIL = st.secrets.get("PAYPAL_EMAIL", "teu-email-paypal@gmail.com")
EXPRESS_PHONE = st.secrets.get("EXPRESS_PHONE", "9XX XXX XXX")
EXPRESS_IBAN = st.secrets.get("EXPRESS_IBAN", "AO06.0000.0000.0000.0000.0")
GROQ_API_KEY = st.secrets.get(
    "GROQ_API_KEY", os.environ.get("GROQ_API_KEY", "")
)

# Chaves VIP Válidas (Incluindo a tua chave pessoal)
CHAVES_VIP_VALIDAS = [
    "ERNESTO-ZEFERINO",  # Tua chave pessoal de criador
    "HERNANY-VIP",  # Chave baseada no teu apelido
    "HJVIP2026",
    "VIP-EXPRESS-AO",
    "VIP-AIRTM-5USD",
    "VIP-PAYPAL-5USD",
]

# Estado da sessão
if "creditos_texto" not in st.session_state:
  st.session_state.creditos_texto = 10  # 10 mensagens grátis

if "creditos_imagem" not in st.session_state:
  st.session_state.creditos_imagem = 2  # 2 imagens grátis

if "chave_vip_ativa" not in st.session_state:
  st.session_state.chave_vip_ativa = ""

if "historico_chat" not in st.session_state:
  st.session_state.historico_chat = []

# -----------------------------------------------------------------------------
# 3. BARRA LATERAL (SIDEBAR) & AUTENTICAÇÃO VIP
# -----------------------------------------------------------------------------
st.sidebar.title("⚡ HJ IA")

chave_input = st.sidebar.text_input(
    "🔑 Código VIP / Ativação:",
    type="password",
    value=st.session_state.chave_vip_ativa,
    placeholder="Insira o seu código...",
)

if chave_input.strip() in CHAVES_VIP_VALIDAS:
  st.session_state.chave_vip_ativa = chave_input.strip()
  e_premium = True
else:
  e_premium = False

# Seleção de modelos por nível de acesso
if e_premium:
  st.sidebar.success("🌟 **Plano Premium Ativo** (Ilimitado)")
  modelos_disponiveis = [
      "🧠 Raciocínio Complexo (DeepSeek R1)",
      "🎯 3.1 Pro (70B Parâmetros)",
      "⚡ 3.6 Flash (Rápido)",
      "🔹 3.5 Flash (Leve)",
  ]
else:
  st.sidebar.warning("⚡ **Plano Gratuito**")
  st.sidebar.write(
      f"💬 Perguntas Restantes: `{st.session_state.creditos_texto}`"
  )
  st.sidebar.write(
      f"🎨 Imagens Restantes: `{st.session_state.creditos_imagem}`"
  )
  modelos_disponiveis = ["🔹 3.5 Flash (Leve)", "⚡ 3.6 Flash (Rápido)"]

modelo_selecionado = st.sidebar.selectbox(
    "Modelo de IA Ativo:", modelos_disponiveis
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
### 🔓 Desbloquear Premium ($5 USD / Mês)
Acesso **Ilimitado** a todas as IAs e gerador de imagens HD.

💳 **Pagamentos Aceites:**
- **Airtm ($5):** `{AIRTM_EMAIL}`
- **PayPal ($5):** `{PAYPAL_EMAIL}`
- **🇦🇴 Express:** `{EXPRESS_PHONE}`
""")

# Crédito do Criador na Barra Lateral
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
<div style="text-align: center; color: #8B949E; font-size: 12px;">
    <p><b>HJ IA</b> © 2026<br>Todos os direitos reservados.</p>
    <p>Desenvolvido por <b>Ernesto Zeferino (hernany Jr)</b></p>
</div>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 4. INTEGRAÇÃO GROQ API & TELA DE PAYWALL
# -----------------------------------------------------------------------------


def chamar_groq(prompt_sistema, prompt_usuario):
  if not GROQ_API_KEY:
    return "⚠️ Erro: Chave GROQ_API_KEY não configurada nos Secrets do Streamlit."

  mapa_modelos = {
      "🔹 3.5 Flash (Leve)": "llama-3.1-8b-instant",
      "⚡ 3.6 Flash (Rápido)": "mixtral-8x7b-32768",
      "🎯 3.1 Pro (70B Parâmetros)": "llama-3.1-70b-versatile",
      "🧠 Raciocínio Complexo (DeepSeek R1)": "deepseek-r1-distill-llama-70b",
  }

  model_id = mapa_modelos.get(modelo_selecionado, "llama-3.1-8b-instant")
  headers = {
      "Authorization": f"Bearer {GROQ_API_KEY}",
      "Content-Type": "application/json",
  }
  payload = {
      "model": model_id,
      "messages": [
          {"role": "system", "content": prompt_sistema},
          {"role": "user", "content": prompt_usuario},
      ],
      "temperature": 0.6 if "Raciocínio" in modelo_selecionado else 0.7,
  }

  try:
    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        json=payload,
        headers=headers,
        timeout=40,
    )
    if res.status_code == 200:
      return res.json()["choices"][0]["message"]["content"]
    else:
      return f"❌ Erro no Servidor Groq ({res.status_code}): {res.text}"
  except Exception as e:
    return f"❌ Erro de Ligação: {str(e)}"


def exibir_paywall(recurso="texto"):
  tipo = "perguntas" if recurso == "texto" else "gerações de imagem"
  st.error(
      f"🚫 **Atingiu o limite de {tipo} do seu Plano Gratuito!**", icon="🔒"
  )

  st.markdown(
      f"""
      <div class="paywall-box">
          <h3>🚀 Adquira o Plano Premium ($5.00 USD)</h3>
          <p>Obtenha acesso ilimitado e imediato a todos os recursos da HJ IA.</p>
          
          <h4>💳 Métodos de Pagamento:</h4>
          <div class="payment-card">
              <b>🌐 Airtm ($5.00 USD)</b><br>
              Email: <code>{AIRTM_EMAIL}</code>
          </div>
          <div class="payment-card">
              <b>🅿️ PayPal ($5.00 USD)</b><br>
              Email: <code>{PAYPAL_EMAIL}</code>
          </div>
          <div class="payment-card">
              <b>🇦🇴 Multicaixa Express (Angola)</b><br>
              Telemóvel: <code>{EXPRESS_PHONE}</code><br>
              IBAN: <code>{EXPRESS_IBAN}</code>
          </div>
          <p>Após o pagamento, envie o comprovativo para receber o seu <b>Código VIP</b>.</p>
      </div>
      """,
      unsafe_allow_html=True,
  )

  st.markdown("---")
  chave_tentada = st.text_input(
      "🔑 Insira aqui o Código VIP recebido:",
      type="password",
      key=f"pw_{recurso}",
  )
  if st.button("Ativar Agora", key=f"btn_{recurso}"):
    if chave_tentada.strip() in CHAVES_VIP_VALIDAS:
      st.session_state.chave_vip_ativa = chave_tentada.strip()
      st.success("🎉 Plano Premium ativado!")
      st.rerun()
    else:
      st.error("❌ Código VIP inválido.")


# -----------------------------------------------------------------------------
# 5. RECURSOS E ABAS DA APLICAÇÃO
# -----------------------------------------------------------------------------
st.title("⚡ HJ IA")

aba_chat, aba_negocios, aba_musica, aba_imagem = st.tabs([
    "💬 Chat & Tutor",
    "💼 Consultoria Executiva",
    "🎵 Estúdio Musical",
    "🎨 Estúdio Visual HD",
])

# --- ABA 1: CHAT GERAL ---
with aba_chat:
  st.header("💬 Chat & Assistente Académico")
  st.caption(f"Modelo ativo: **{modelo_selecionado}**")

  for msg in st.session_state.historico_chat:
    with st.chat_message(msg["role"]):
      st.markdown(msg["content"])

  prompt = st.chat_input("Pergunta algo à HJ IA...")
  if prompt:
    st.session_state.historico_chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    if e_premium or st.session_state.creditos_texto > 0:
      if not e_premium:
        st.session_state.creditos_texto -= 1

      with st.chat_message("assistant"):
        with st.spinner("A pensar..."):
          resposta = chamar_groq(
              "Você é a HJ IA, um assistente inteligente, prestativo e altamente capacitado.",
              prompt,
          )
          st.markdown(resposta)
          st.session_state.historico_chat.append(
              {"role": "assistant", "content": resposta}
          )
    else:
      exibir_paywall("texto")

# --- ABA 2: CONSULTORIA EXECUTIVA ---
with aba_negocios:
  st.header("💼 Consultoria Executiva de Negócios")
  st.write("Receba análises sobre gestão, plano de negócios, finanças e vendas.")

  prompt_biz = st.text_area(
      "Descreva o seu projeto ou dúvida comercial:", height=120
  )
  if st.button("Gerar Análise de Negócio"):
    if prompt_biz:
      if e_premium or st.session_state.creditos_texto > 0:
        if not e_premium:
          st.session_state.creditos_texto -= 1
        with st.spinner("A analisar o mercado..."):
          res_biz = chamar_groq(
              "Você é um consultor executivo sênior especialista em negócios, empreendedorismo e gestão comercial.",
              prompt_biz,
          )
          st.markdown(res_biz)
      else:
        exibir_paywall("texto")

# --- ABA 3: ESTÚDIO MUSICAL ---
with aba_musica:
  st.header("🎵 Estúdio Musical & Compositor")
  st.write("Crie letras de música completas com estrutura profissional.")

  col_estilo, col_tema = st.columns(2)
  with col_estilo:
    estilo = st.selectbox(
        "Gênero Musical:",
        [
            "Rap / Trap",
            "Afro House",
            "Semba / Kizomba",
            "R&B / Soul",
            "Gospel",
            "Pop",
        ],
    )
  with col_tema:
    tema = st.text_input("Tema da Canção:", placeholder="Ex: Superação, Sucesso...")

  if st.button("Compor Letra"):
    if tema:
      if e_premium or st.session_state.creditos_texto > 0:
        if not e_premium:
          st.session_state.creditos_texto -= 1
        with st.spinner("A criar os versos..."):
          prompt_m = f"Escreva uma letra de música completa no estilo {estilo} sobre o tema '{tema}'. Inclua Verso 1, Refrão, Verso 2 e Outro."
          res_m = chamar_groq(
              "Você é um compositor e produtor musical premiado.", prompt_m
          )
          st.markdown(res_m)
      else:
        exibir_paywall("texto")

# --- ABA 4: ESTÚDIO VISUAL HD ---
with aba_imagem:
  st.header("🎨 Estúdio Visual HD")
  st.write("Gere imagens HD exclusivas a partir de descrições em texto.")

  prompt_img = st.text_input(
      "Descreva a imagem que pretende criar:",
      placeholder="Ex: Um carro desportivo futurista nas ruas de Luanda à noite",
  )

  if st.button("Gerar Imagem HD"):
    if prompt_img:
      if e_premium or st.session_state.creditos_imagem > 0:
        if not e_premium:
          st.session_state.creditos_imagem -= 1

        with st.spinner("A desenhar imagem..."):
          url_img = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt_img)}?width=768&height=768&nologo=true"
          st.image(
              url_img, caption=f"HJ IA Art: {prompt_img}", use_column_width=True
          )
      else:
        exibir_paywall("imagem")

# -----------------------------------------------------------------------------
# 6. DIREITOS AUTORAIS E AVISO LEGAL (FOOTER)
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; color: #8B949E; font-size: 12px; padding: 10px;">
    <p>⚠️ <b>Aviso Legal:</b> A HJ IA é um sistema baseado em inteligência artificial. As respostas geradas são informativas e não substituem aconselhamento profissional especializado.</p>
    <p>© 2026 <b>HJ IA</b>. Todos os direitos reservados. | Criado por <b>Ernesto Zeferino (hernany Jr)</b></p>
</div>
""",
    unsafe_allow_html=True,
)
