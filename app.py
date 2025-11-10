import streamlit as st

# Importe os agentes 
from src.agents.nfe_sequential_agent.agent import root_agent, extractor_agent
# from src.agents.agente_exemplo.agent import agente_exemplo

from src.agents.doc_data_extractor.agent import coordinator

# Importe as páginas
from src.ui.pages.chat_page import agent_chat_page

PAGES_LIST = {
    "Chat com Agente": agent_chat_page,
    # "Nome da Página": pagina_exemplo
}

AGENTS_LIST = [
    root_agent,
    extractor_agent,
    coordinator,
    # agente_exemplo,
]

with st.sidebar:
    st.title("Navegação")
    selection = st.radio("Ir para", list(PAGES_LIST.keys()))
    
page = PAGES_LIST[selection]

if 'agent_list' in page.__code__.co_varnames:
    page(AGENTS_LIST)
else:
    page()
