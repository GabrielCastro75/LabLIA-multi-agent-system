import logging
import dotenv
import os
import mimetypes

from typing import List

import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.genai import types
from google.adk.apps import App

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lista de LLMs suportados - Google AI Studio Free Tier
DEFAULT_MODELS_PRETTY_NAME = [
    "Gemini 2.5 Flash",
    "Gemini 2.0 Flash"
]

# Mapeamento de LLMs
DEFAULT_LLM_MODELS_PRETTY_NAME_MAP = {
    "Gemini 2.5 Flash": "gemini-2.5-flash",
    "Gemini 2.0 Flash": "gemini-2.0-flash"
}

def detect_file_mime_type(file_bytes: bytes, filename: str = None) -> str:
    """
    Detecta o tipo MIME de um arquivo baseado no conteúdo ou nome do arquivo.
    Suporta imagens e PDFs.

    Args:
        file_bytes: Bytes do arquivo
        filename: Nome do arquivo (opcional)

    Returns:
        str: Tipo MIME detectado ou 'application/octet-stream' como fallback
    """
    if filename:
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type:
            return mime_type

    # Detecção baseada no conteúdo
    if len(file_bytes) >= 8:
        # PDF: %PDF-
        if file_bytes[0:5] == b'%PDF-':
            return 'application/pdf'
        # JPEG: FF D8 FF
        elif file_bytes[0:3] == b'\xFF\xD8\xFF':
            return 'image/jpeg'
        # PNG: 89 50 4E 47
        elif file_bytes[0:4] == b'\x89\x50\x4E\x47':
            return 'image/png'
        # GIF: 47 49 46
        elif file_bytes[0:3] == b'\x47\x49\x46':
            return 'image/gif'
        # WebP: 52 49 46 46 (RIFF) seguido de WEBP
        elif len(file_bytes) >= 12 and file_bytes[0:4] == b'\x52\x49\x46\x46' and file_bytes[8:12] == b'\x57\x45\x42\x50':
            return 'image/webp'

    # Fallback
    return 'application/octet-stream'

# Executa uma chamada ao agente com base na entrada do usuário (Texto, Imagens e PDFs)
async def run_agent_query(agent: Agent, session_service: InMemorySessionService, session: Session, user_input: str, llm_model_pretty_name: str = "Gemini 2.5 Flash", files: List[bytes] = None):

    # Atualiza o modelo LLM do agente
    llm_model = DEFAULT_LLM_MODELS_PRETTY_NAME_MAP.get(llm_model_pretty_name, "gemini-2.5-flash")
    if hasattr(agent, 'model'):
        agent.model = llm_model

    runner = Runner(
        agent=agent,
        app_name=session.app_name,
        session_service=session_service
    )

    # logger.info(f"Sending message to agent: {user_input}")

    final_response_text = "Nenhuma resposta recebida do agente."

    # Preparar as partes da mensagem
    parts = []

    # Adicionar texto se existir
    if user_input.strip():
        parts.append(types.Part(text=user_input))

    # Adicionar arquivos se existirem (imagens e PDFs)
    if files:
        for file_bytes in files:
            # Detectar o tipo MIME do arquivo
            mime_type = detect_file_mime_type(file_bytes)

            # Verificar se é um tipo suportado
            if mime_type.startswith(('image/', 'application/pdf')):
                # Converter bytes do arquivo para o formato esperado pelo Google ADK
                parts.append(types.Part(
                    inline_data=types.Blob(
                        mime_type=mime_type,
                        data=file_bytes
                    )
                ))
            else:
                # Para outros tipos, converter para texto ou ignorar
                logger.warning(f"Tipo MIME não suportado: {mime_type}")

    user_message = types.Content(role="user", parts=parts)

    async for event in runner.run_async(
        session_id=session.id,
        user_id=session.user_id,
        new_message=user_message
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text

    # logger.info(f"Received response from agent: {final_response_text}")

    return final_response_text

if __name__ == "__main__":
    from src.agents.nfe_sequential_agent.agent import root_agent

    if os.path.exists('.env'):
        dotenv.load_dotenv(override=True)
    
    session_service = InMemorySessionService()

    session = asyncio.run(
        session_service.create_session(
            session_id="lab_lia",
            app_name="agents",
            user_id="user_1"
        )
    )

    user_input = "Olá, quem é você ?"

    response = asyncio.run(run_agent_query(root_agent, session_service, session, user_input))
    print(response)