# LabLIA Multi-Agent System 🤖

Sistema multi-agente baseado em IA para processamento inteligente de documentos usando Google ADK (Agent Development Kit) e Streamlit.

## 📋 Sobre o Projeto

Este projeto implementa um sistema de agentes inteligentes capaz de:
- **Processar Notas Fiscais Eletrônicas (NFe)**: Extração automática de dados, cálculos de impostos (ICMS) e apresentação de resultados estruturados
- **Extrair dados de documentos**: Análise inteligente de imagens e PDFs para extração de informações estruturadas
- **Interface conversacional**: Chat interativo com agentes especializados via Streamlit

## 🚀 Funcionalidades

- ✅ Processamento sequencial de tarefas com `SequentialAgent`
- ✅ Extração de dados de imagens e PDFs
- ✅ Cálculos automáticos de impostos (ICMS)
- ✅ Interface web responsiva com Streamlit
- ✅ Suporte a múltiplos modelos LLM (Gemini 2.5 Flash, Gemini 2.0 Flash)
- ✅ Upload de arquivos (PNG, JPG, JPEG, GIF, WebP, PDF)

## 🛠️ Pré-requisitos

- Python 3.8 ou superior
- Conta Google Cloud com API Gemini habilitada
- Chave da API do Google AI Studio

## 📦 Instalação

### Método Rápido (Recomendado)
```bash
git clone https://github.com/GabrielCastro75/LabLIA-multi-agent-system.git
cd LabLIA-multi-agent-system
./start.sh
```

### Instalação Manual

#### 1. Clone o repositório
```bash
git clone https://github.com/GabrielCastro75/LabLIA-multi-agent-system.git
cd LabLIA-multi-agent-system
```

#### 2. Crie um ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

#### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### 1. Configurar API Key do Google

Crie um arquivo `.env` na raiz do projeto (use `.env.example` como referência):

```env
GOOGLE_API_KEY=sua_chave_api_aqui
```

### 2. Obter a chave da API

1. Acesse [Google AI Studio]
2. Crie uma nova chave de API
3. Copie a chave e adicione ao arquivo `.env`

## ▶️ Como Executar

### Aplicação Web (Interface Principal)
```bash
streamlit run app.py
```

A aplicação estará disponível em: http://localhost:8501

### Teste via Notebook
```bash
jupyter notebook run_agent_ex.ipynb
```

### Teste via Script Python
```bash
python src/agents/agent_config.py
```

## 🏗️ Estrutura do Projeto

```
LabLIA-multi-agent-system/
├── app.py                          # Aplicação principal Streamlit
├── src/
│   ├── agents/
│   │   ├── agent_config.py         # Configurações e utilitários dos agentes
│   │   ├── nfe_sequential_agent/   # Agente sequencial para processamento de NFe
│   │   │   ├── agent.py           # Definição do SequentialAgent
│   │   │   └── pydantic_schema.py # Schemas Pydantic para NFe
│   │   └── doc_data_extractor/     # Agente extrator de dados de documentos
│   │       ├── agent.py           # Definição do agente extrator
│   │       └── pydantic_schema.py # Schemas para extração de dados
│   └── ui/
│       └── pages/
│           └── chat_page.py        # Interface de chat com agentes
├── docs/                          # Arquivos de exemplo
│   └── notas_fiscais/            # Exemplos de NFe
├── .env.example                  # Exemplo de configuração de ambiente
├── requirements.txt              # Dependências do projeto
├── run_agent_ex.ipynb            # Notebook de exemplo
└── README.md                     # Este arquivo
```

## 🤖 Agentes Disponíveis

### 1. Agente Sequencial NFe (`root_agent`)
Processa Notas Fiscais Eletrônicas em sequência:
- **Extração de Dados**: Identifica chave de acesso, CNPJ, valor total, data de emissão
- **Cálculo de Impostos**: Calcula ICMS baseado nos dados extraídos
- **Apresentação**: Exibe resultados formatados com informações detalhadas

### 2. Agente Extrator de Dados (`extractor_agent`)
Extrai dados estruturados de documentos (imagens/PDFs).

### 3. Agente Coordenador (`coordinator`)
Coordena múltiplas tarefas de extração de dados.

## 📖 Como Usar

### Via Interface Web
1. Execute `streamlit run app.py`
2. Selecione um agente no menu lateral
3. Escolha o modelo LLM desejado
4. Faça upload de uma imagem/PDF (opcional)
5. Digite sua mensagem e pressione Enter

### Exemplo de Uso - Processamento de NFe
1. Faça upload de uma imagem de Nota Fiscal
2. Digite: "Processar esta nota fiscal"
3. O sistema irá:
   - Extrair automaticamente os dados da NFe
   - Calcular os impostos (ICMS)
   - Apresentar um relatório completo

## 🔧 Desenvolvimento

### Adicionando Novos Agentes
1. Crie uma nova pasta em `src/agents/`
2. Implemente o agente em `agent.py`
3. Defina schemas Pydantic em `pydantic_schema.py`
4. Importe e adicione à lista `AGENTS_LIST` em `app.py`

### Testando Agentes
Use o arquivo `run_agent_ex.ipynb` como referência para testar novos agentes.

## 📝 Notas Técnicas

- **Google ADK**: Framework usado para desenvolvimento de agentes
- **SequentialAgent**: Executa agentes em sequência, passando dados entre eles
- **Session State**: Gerenciamento de estado usando `InMemorySessionService`
- **Pydantic**: Validação e serialização de dados estruturados

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 🆘 Suporte

Para dúvidas ou problemas:
1. Verifique se todas as dependências estão instaladas
2. Confirme se a chave da API do Google está configurada corretamente
3. Execute os testes no notebook `run_agent_ex.ipynb`

---