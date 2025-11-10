from pydantic import BaseModel, Field
from typing import List

class Produto(BaseModel):
    codigo: str = Field(description="Código do Produto")
    descricao: str = Field(description="Descrição do Produto")
    preco_unidade: float = Field(description="Preço da unidade do produto")
    quantidade: int = Field(description="Quantidade de unidades do Produto")
    preco_total: str = Field(description="Preço Total")

class NotaFiscalData(BaseModel):
    destinatario_nome: str = Field(description="Nome do destinatário/remetendo")
    valor_total: str = Field(description="Valor total da nota")
    valor_ICMS: str = Field(description="Valor do ICMS")
    produtos: List[Produto]

class ImpostoProduto(BaseModel):
    codigo: str = Field(description="Código do Produto")
    valor_icms: float = Field(description="Valor do ICMS do Produto")

class NFeTax(BaseModel):
    porcentagem_icms: float = Field(description="Porcentagem do ICMS sobre a NFe")
    imposto_produtos: List[ImpostoProduto] = Field(description="Lista de Valores sobre os impostos dos produtos") 