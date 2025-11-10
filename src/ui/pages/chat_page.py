import streamlit as st
import asyncio
import os
import dotenv

from src.agents.agent_config import run_agent_query, DEFAULT_MODELS_PRETTY_NAME
from google.adk.sessions import Session, InMemorySessionService
from google.adk.agents import LlmAgent

from typing import List

import uuid

# Renderiza a página de chat com o agente
def agent_chat_page(agent_list: List[LlmAgent]):
    """
    Renderiza a página de chat com o agente
    
    Args:
        agent_list (List[LlmAgent]): Lista de agentes disponíveis para seleção.
    """
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    # Mapeamento - Nome: Agente
    agents_by_name = {a.name: a for a in agent_list}
    agent_names = list(agents_by_name.keys())
    
    # Configuração da página
    st.set_page_config(
        page_title="LabLIA - Chat com Agente",
        page_icon="🤖",
        layout="wide"
    )

    st.title("🤖 LabLIA - Chat com Agente")
    st.markdown("Converse com o agente de IA inteligente")

    # Sidebar com informações
    with st.sidebar:
        st.write("---")
        st.header("Escolha de Agente")
        st.selectbox(
            "Selecione o agente com o qual deseja conversar:",
            options=agent_names,
            format_func=lambda x: x.title().replace("_", " "), # Formata o nome do agente para exibição
            index=0,
            key="selected_agent_name"
        )
        
        selected_agent = agents_by_name[st.session_state.selected_agent_name]
        
        st.header("Escolha um Modelo LLM")
        st.selectbox(
            "Selecione o modelo LLM para o agente:",
            options=DEFAULT_MODELS_PRETTY_NAME,
            index=0,
            key="selected_llm_model"
        )
        
        st.markdown("""
        **Status:** Online
        
        ---
        
        **Como usar:**
        1. Digite sua mensagem no campo abaixo
        2. Pressione Enter ou clique em enviar
        3. Aguarde a resposta do agente
        """)
        
        if st.button("🗑️ Limpar Conversa", type="secondary"):
            st.session_state.messages = []
            st.rerun()

    # Carrega variáveis de ambiente
    if os.path.exists('.env'):
        dotenv.load_dotenv(override=True)

    # Inicializa os serviços (uma vez por sessão)
    if 'session_service' not in st.session_state:
        st.session_state.session_service = InMemorySessionService()

    if 'session' not in st.session_state:
        try:
            # Criar e registrar sessão no session_service
            session = asyncio.run(
                st.session_state.session_service.create_session(
                    session_id=str(uuid.uuid4()),
                    app_name="agents",
                    user_id="user_1"
                )
            )
            st.session_state.session = session
        except Exception as e:
            st.error(f"Erro ao criar sessão: {e}")
            st.stop()

    # Inicializar histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibir histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if isinstance(message["content"], dict):
                # Conteúdo estruturado (com arquivo)
                if "file" in message["content"]:
                    file_type = message["content"].get("file_type", "")
                    file_name = message["content"].get("file_name", "Arquivo")
                    if file_type.startswith('image/'):
                        st.image(message["content"]["file"], caption=f"Imagem enviada: {file_name}", width=300)
                    elif file_type == 'application/pdf':
                        st.write(f"📄 PDF enviado: {file_name}")
                    else:
                        st.write(f"📎 Arquivo enviado: {file_name}")
                if "text" in message["content"] and message["content"]["text"]:
                    st.markdown(message["content"]["text"])
            else:
                # Conteúdo de texto simples
                st.markdown(message["content"])

    # Campo de entrada do chat
    if prompt := st.chat_input("Digite sua mensagem..."):
        # Preparar conteúdo da mensagem
        message_content = {"text": prompt.strip()}

        # Processar arquivo se enviado
        file_data = None
        file_type = None
        if st.session_state.uploaded_file is not None:
            file_data = st.session_state.uploaded_file.getvalue()
            file_type = st.session_state.uploaded_file.type.lower()
            message_content["file"] = file_data
            message_content["file_type"] = file_type
            message_content["file_name"] = st.session_state.uploaded_file.name

        # Adicionar mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": message_content})

        # Exibir mensagem do usuário
        with st.chat_message("user"):
            if file_data and file_type:
                if file_type.startswith('image/'):
                    st.image(file_data, caption="Imagem enviada", width=300)
                elif file_type == 'application/pdf':
                    st.write(f"📄 PDF enviado: {st.session_state.uploaded_file.name}")
                else:
                    st.write(f"📎 Arquivo enviado: {st.session_state.uploaded_file.name}")
            st.markdown(message_content["text"])
        
        # Placeholder para resposta do assistente
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    # Preparar parâmetros para o agente
                    agent_text = message_content["text"]
                    agent_files = [file_data] if file_data else None

                    # Executar query de forma assíncrona
                    response = asyncio.run(run_agent_query(
                        selected_agent,
                        st.session_state.session_service,
                        st.session_state.session,
                        agent_text,
                        st.session_state.selected_llm_model,
                        files=agent_files
                    ))

                    # Exibir resposta
                    st.markdown(response)

                    # Adicionar resposta ao histórico
                    st.session_state.messages.append({"role": "assistant", "content": response})

                except Exception as e:
                    error_msg = f"Erro ao processar mensagem: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

        # Limpar o arquivo após processamento (para permitir novo upload)
        st.session_state.uploaded_file = None

    uploaded_file = st.file_uploader(
        "📎 Enviar arquivo (opcional)",
        type=["png", "jpg", "jpeg", "gif", "webp", "pdf"],
        key="file_upload",
        help="Selecione uma imagem ou PDF para enviar junto com sua mensagem"
    )

    # Atualizar estado do arquivo
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file

    # Mostrar preview do arquivo selecionado
    if st.session_state.uploaded_file is not None:
        file_type = st.session_state.uploaded_file.type.lower()
        if file_type.startswith('image/'):
            st.image(st.session_state.uploaded_file, caption="Imagem selecionada", width=200)
        elif file_type == 'application/pdf':
            st.write(f"📄 PDF selecionado: {st.session_state.uploaded_file.name}")
        else:
            st.write(f"📎 Arquivo selecionado: {st.session_state.uploaded_file.name}")

    # st.write(st.session_state.session.events)