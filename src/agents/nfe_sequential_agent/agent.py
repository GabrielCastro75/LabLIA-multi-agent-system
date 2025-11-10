# from .pydantic_schema import OutputSchema
from .pydantic_schema import NotaFiscalData, NFeTax
from google.adk.agents import LlmAgent, SequentialAgent
import textwrap

# Calculo de ICMS em Nota Fiscal

"""Agente responsável por verificar se o documento é uma Nota Fiscal"""

# Instrução do Agente
validator_instruction = textwrap.dedent("""\
    Insira o seu prompt aqui""")

# Definição do Agente - Crie o agente validador
# validator_agent = LlmAgent()

"""Agente Extrator de Informações da NFe"""
# Instrução do Agente
extractor_instruction = textwrap.dedent("""\
    Você é especialista na extração de dados de uma Nota Fiscal.
    
    Dada a imagem de uma Nota Fiscal, você deverá extrair:
    - destinatario_nome: Nome do destinatário.
    - valor_total: Valor total da Nota Fiscal.
    - valor_ICMS: Valor total do ICMS da Nota.
    - produtos: Lista de produtos contidos na nota
    
    Retorne sua resposta no formato JSON especificado, usando apenas os dados das imagens.""")

# Definição do Agente
extractor_agent = LlmAgent(
    name='extrator_de_dados_NFe',
    model="gemini-2.5-flash",
    description="Extrai os dados de uma Nota Fiscal Eletronica",
    instruction=extractor_instruction,
    output_schema=NotaFiscalData,
    output_key="nota_fiscal_data",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

"""Agente Calculador de Impostos da NFe"""
# Instrução do Agente
calculator_instruction = textwrap.dedent("""\
    Você é um especialista no cálculo de impostos relacionados a uma Nota Fiscal Eletrônica (NFe).
    
    [CONTEXTO]
    Dados da Nota Fiscal:
    ```json
    {nota_fiscal_data}
    ```
    
    [TAREFA]
    Calcule o imposto contido nos produtos/serviços da NFe seguindo as seguintes etapas:
    1 - Calcule a porcentagem do ICMS sobre o valor total da nota.
    2 - Calcule o valor do ICMS sobre cada produto usando a porcentagem do ICMS calculada na etapa 1.
    
    Para cada produto indique:
    1 - codigo: Código do Produto
    2 - valor_icms: O valor do ICMS
    
    Responda usando o esquema JSON especificado, e utilizando APENAS o contexto dado.""")

# Definição do Agente
nfe_calculator_agent = LlmAgent(
    name='calculador_de_imposto_nfe',
    model="gemini-2.5-flash",
    description="Calcula o Imposto (ICMS) atribuido a uma Nota Fiscal Eletrônica",
    instruction=calculator_instruction,
    output_schema=NFeTax,
    output_key="icms_result",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

"""Agente responsável pela exibição do resultado para o usuário"""
# Instrução do Agente
result_instruction = textwrap.dedent("""\
    Você é responsável por exibir o resultado do cálculo do ICMS de uma Nota Fiscal Eletrônica.
    
    [CONTEXTO]
    **DADOS DA NOTA FISCAL ELETRÔNICA:**
    ```json
    {nota_fiscal_data}
    ```
    
    **RESULTADO DO CÁLCULO DOS IMPOSTOS**:
    ```json
    {icms_result}
    ```
    
    [TAREFA]
    Gere um texto descritivo e informativo da Nota Fiscal Eletrônica, contendo:
    - Nome do destinatário
    - Valor Total da Nota
    - Valor do ICMS
    - Porcentagem do ICMS
    
    Para cada produto/serviço, indique:
    - Código identificador
    - Descrição
    - Valor Total do Produto
    - Valor Total do ICMS""")

# Definição do Agente
result_agent = LlmAgent(
    name='exibidor_de_resultado_NFe',
    model="gemini-2.5-flash",
    description="Exibe o resultado do cálculo de ICMS de uma NFe",
    instruction=result_instruction
)

"""Agente Sequencial - Cria Pipeline sequencial de agentes"""
# Cria Pipeline sequencial (extração dos dados -> cálculo de impostos)
root_agent = SequentialAgent(
    name="calculador_de_ICMS_NFe", sub_agents=[extractor_agent, nfe_calculator_agent, result_agent]
)