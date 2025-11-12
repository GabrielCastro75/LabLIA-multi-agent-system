# from .pydantic_schema import OutputSchema
from .pydantic_schema import CNHdata, RGdata
from google.adk.agents import LlmAgent, SequentialAgent
import textwrap

# Extração de Dados de Documentos

"""Agente responsável por gerar Saída dos dados para o usuário"""
# Instrução do usuário 
user_view_text_agent_inst = textwrap.dedent("""\
    Você é responsável por gerar uma descrição sobre os dados encontrados do documento.

    [CONTEXTO]
    DADOS DO DOCUMENTO:
    {document_data}

    [TAREFA]
    Informe os dados do documento em formato de tópicos, incluindo os dados pessoais e o tipo do documento.
    
    Responda usando APENAS os dados fornecidos""")

# Definição do agente
user_view_agent = LlmAgent(
    name="user_view_agent",
    model="gemini-2.5-flash",
    description="Descreve os dados encontrados do documento em formato legível ao usuário",
    instruction=user_view_text_agent_inst
)

"""Agente responsável por extrair dados de uma CNH"""
# Instrução do Agente
cnh_instruction = textwrap.dedent("""\
    Você é responsável por extrair os dados de uma Carteira Nacional de Habilitação
    
    Dadas as imagens do documento, extraia:
    - tipo_do_documento: Tipo do documento recebido (Carteira Nacional de habilitação - CNH, Registro Geral - RG, ...)
    - nome_completo: Nome completo da pessoa física
    - cpf: CPF da pessoa física presente no documento
    - data_de_nascimento: Data de nascimento da pessoa física presente no documento

    Responda seguindo o formato JSON especificado, usando como base apenas as imagens dadas""")

# Definição do Agente
cnh_agent = LlmAgent(
    name="carteira_nacional_de_habilitacao_cnh",
    model="gemini-2.5-flash",
    description="Extrai os dados de uma CNH",
    instruction=cnh_instruction,
    output_schema=CNHdata,
    output_key="document_data",
    disallow_transfer_to_parent=True, 
    disallow_transfer_to_peers=True
)

"""Agente responsável por extrair dados de um RG"""
# Instrução do Agente
rg_instruction = textwrap.dedent("""\
    Você é responsável por extrair os dados de uma Carteira de Identidade (RG)
    
    Dadas as imagens do documento, extraia:
    - tipo_do_documento: Tipo do documento recebido (Carteira Nacional de habilitação - CNH, Registro Geral - RG, ...)
    - nome_completo: Nome completo da pessoa física
    - cpf: CPF da pessoa física presente no documento
    - data_de_nascimento: Data de nascimento da pessoa física presente no documento

    Responda seguindo o formato JSON especificado, usando como base apenas as imagens dadas""")

# Definição do Agente
rg_agent = LlmAgent(
    name="carteira_de_identidade_rg",
    model="gemini-2.5-flash",
    description="Extrai os dados de uma Carteira de Identidade (RG)",
    instruction=rg_instruction,
    output_schema=RGdata,
    output_key="document_data",
    disallow_transfer_to_parent=True, 
    disallow_transfer_to_peers=True
)

# --- Insira aqui agentes extratores de dados adicionais ---

# Instrução do Agente

# Definição do Agente

# ---

"""Agente responsável por coordenar os SubAgentes"""
# Instrução do Agente
coordinator_instruction = textwrap.dedent("""\
    Você é especialista em coordenar Agentes responsáveis por extrair dados de um documento com foto.

    Dada a imagem do documento, escolha o agente que irá extrair os dados, conforme a seguinte descrição:
    - 'carteira_nacional_de_habilitacao_cnh': Extrai os dados de uma Carteira Nacional de Habilitação (CNH)
    - 'carteira_de_identidade_rg': Extrai os dados de uma Carteira de Identidade (RG)
    
    Após extração dos dados do documento use o agente 'user_view_agent' para exibir o resultado ao usuário.
    """)

# Definição do agente
coordinator = LlmAgent(
    name="extracao_dados_documentos",
    model="gemini-2.5-flash",
    description="Coordena agentes extratores de dados de documentos",
    instruction=coordinator_instruction,
    sub_agents=[ 
        cnh_agent,
        rg_agent,
        user_view_agent
        # Adicione os agentes aqui
    ]
)