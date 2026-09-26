import os
import streamlit as st
from groq import Groq

# 1. Configuração da Página e Tema Escuro Nativo (Gemini Style)
st.set_page_config(
    page_title="HJ IA — Flash Estendido",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização CSS para réplica fiel da interface (Dark Mode com Gradiente)
st.markdown("""
    <style>
    /* Fundo Escuro com Gradiente na Base */
    .stApp {
        background: radial-gradient(circle at bottom, #111d38 0%, #080a0f 65%, #000000 100%) !important;
        color: #FFFFFF !important;
    }
    
    /* Ocultar elementos padrão */
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Contentor Centralizado */
    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 30px;
        margin-bottom: 25px;
        text-align: center;
    }

    /* Estrela Central com Gradiente */
    .gemini-star {
        font-size: 3rem;
        background: -webkit-linear-gradient(45deg, #4285F4, #9B51E0, #EA4335, #FBBC05);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
        display: inline-block;
    }

    .hero-title {
        font-size: 1.8rem;
        font-weight: 500;
        color: #E3E3E3;
        margin-bottom: 20px;
        font-family: 'Google Sans', sans-serif, system-ui;
    }

    /* Estilização das Mensagens do Chat */
    .stChatMessage {
        background-color: #131722 !important;
        border-radius: 18px !important;
        border: 1px solid #222938 !important;
        margin-bottom: 12px !important;
    }

    /* Rodapé com Direitos Autorais */
    .copyright-footer {
        text-align: center;
        color: #6E7681;
        font-size: 0.8rem;
        padding-top: 15px;
        border-top: 1px solid #161B22;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Inicialização do Cliente Groq
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ **Erro de Configuração:** A chave `GROQ_API_KEY` não foi encontrada nos **Secrets** do Streamlit.")
    st.info("💡 Adicione a chave nas definições da aplicação no Streamlit Cloud em `Settings -> Secrets`.")
    st.stop()

client = Groq(api_key=api_key)

# 3. Gestão de Estado (Créditos, Criador e Modelo Ativo)
if "user_credits" not in st.session_state:
    st.session_state.user_credits = 5

if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

if "is_creator" not in st.session_state:
    st.session_state.is_creator = False  # Modo Criador / Admin

if "messages" not in st.session_state:
    st.session_state.messages = []

# CÓDIGOS DE ATIVAÇÃO
CODIGO_CLIENTE_VIP = "HJIA2026"
CODIGO_CRIADOR_MASTER = "ZEFERINO16"  # O seu código de Criador Ilimitado

# 4. Barra Superior — Seleção de Modelo
col_top1, col_top2 = st.columns([3, 1])
with col_top1:
    modelo_opcao = st.selectbox(
        "Modelo:",
        [
            "⚡ Flash (Leve & Rápido)",
            "🧠 Flash Estendido (Raciocínio Complexo)",
            "🚀 Pro (Avançado & Sem Limites)"
        ],
        index=1,
        label_visibility="collapsed"
    )

with col_top2:
    if st.session_state.is_creator:
        st.caption("👑 **CRIADOR (♾️)**")
    elif st.session_state.is_premium:
        st.caption("⭐ **PRO (Ilimitado)**")
    else:
        st.caption(f"🎟️ **{st.session_state.user_credits} Tokens**")

# Mapeamento do Modelo Selecionado
if "Flash Estendido" in modelo_opcao:
    model_id = "llama-3.3-70b-versatile"
    sys_prompt = "És a HJ IA (Flash Estendido), criada por Ernesto Zeferino (16 anos de idade). Responde com inteligência avançada e concisão."
elif "Pro" in modelo_opcao:
    model_id = "deepseek-r1-distill-llama-70b"
    sys_prompt = "És a HJ IA Pro, um modelo avançado para raciocínio complexo, matemática e programação."
else:
    model_id = "llama-3.1-8b-instant"
    sys_prompt = "És a HJ IA Flash, leve e rápida para respostas diretas."

# 5. Interface Central (Caso a conversa ainda esteja no início)
if len(st.session_state.messages) == 0:
    st.markdown("""
        <div class="hero-container">
            <div class="gemini-star">✦</div>
            <div class="hero-title">Qual precisa ser nosso foco?</div>
        </div>
    """, unsafe_allow_html=True)

# 6. Exibição do Histórico do Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. Abas Auxiliares (Expandíveis para Pagamentos, Ativação e Áudio)
with st.expander("🎙️ Gravar Voz / 💳 Ativação VIP & Criador"):
    tab_voice, tab_pay = st.tabs(["🎙️ Enviar Áudio", "💳 Licença & Código VIP"])
    
    # --- Áudio / Voz ---
    with tab_voice:
        st.write("Grave uma mensagem de voz para a HJ IA escutar e responder:")
        audio_file = st.audio_input("Toque no microfone para falar")
        
        if audio_file is not None and "last_audio" not in st.session_state:
            st.session_state.last_audio = audio_file.name
            with st.spinner("A transcrever a sua voz com o Whisper..."):
                try:
                    transcription = client.audio.transcriptions.create(
                        file=(audio_file.name, audio_file.read()),
                        model="whisper-large-v3",
                        prompt="Transcrição de voz em português"
                    )
                    prompt_audio = transcription.text
                    st.success(f"🗣️ **Voz identificada:** *\"{prompt_audio}\"*")
                    
                    st.session_state.messages.append({"role": "user", "content": f"🎤 [Áudio]: {prompt_audio}"})
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao processar áudio: {e}")

    # --- Pagamentos & Ativação de Criador ---
    with tab_pay:
        st.info("📌 **Acesso Ilimitado:** 2.000 Kz (Angola) | $5,00 USD (Internacional)")
        st.write("• **Multicaixa Express (Angola):** 2.000 Kz")
        st.write("• **Airtm / PayPal:** $5,00 USD")
        
        st.divider()
        codigo_input = st.text_input("Insira o Código de Ativação ou de Criador:", type="password")
        
        if st.button("Validar Código"):
            if codigo_input.strip() == CODIGO_CRIADOR_MASTER:
                st.session_state.is_creator = True
                st.session_state.is_premium = True
                st.success("👑 **Modo Criador Ativado!** Tem acesso a tokens ilimitados (♾️) e todas as funções PRO desbloqueadas.")
                st.rerun()
            elif codigo_input.strip() == CODIGO_CLIENTE_VIP:
                st.session_state.is_premium = True
                st.success("🎉 **Plano Pro Ativado!** Pode utilizar a HJ IA sem limites de tokens.")
                st.rerun()
            else:
                st.error("❌ Código inválido.")

# 8. Entrada de Texto e Controlo de Limites
pode_enviar = st.session_state.is_creator or st.session_state.is_premium or st.session_state.user_credits > 0

if not pode_enviar:
    st.warning("⚠️ Os teus tokens gratuitos acabaram[span_0](start_span)[span_0](end_span). Ative o Plano Pro ou introduza o código de Criador no menu superior.")
else:
    if user_input := st.chat_input("Peça ao HJ IA..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("A processar..."):
                try:
                    response = client.chat.completions.create(
                        model=model_id,
                        messages=[
                            {"role": "system", "content": sys_prompt},
                            *st.session_state.messages
                        ],
                        temperature=0.6,
                        max_tokens=1024,
                    )
                    reply = response.choices[0].message.content
                    st.write(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})

                    # Se não for nem Criador nem Premium, desconta 1 token
                    if not st.session_state.is_creator and not st.session_state.is_premium:
                        st.session_state.user_credits -= 1
                        st.rerun()

                except Exception as e:
                    st.error(f"Erro na resposta: {e}")

# 9. Direitos Autorais
st.markdown("""
    <div class="copyright-footer">
        © Direitos Autorais Reservados — Criada por <b>Ernesto Zeferino</b> (16 anos de idade)
    </div>
""", unsafe_allow_html=True)
