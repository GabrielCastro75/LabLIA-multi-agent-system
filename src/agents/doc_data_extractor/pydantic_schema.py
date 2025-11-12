from pydantic import BaseModel, Field
from typing import List

class CNHdata(BaseModel):
    tipo_do_documento: str = Field(description="Tipo do documento (CNH, RG, ...)")
    nome_completo: str = Field(description="Nome Completo presente no documento")
    cpf: str = Field(description="CPF da pessoa física presente no documento")
    data_de_nascimento: str = Field(description="Data de nascimento da pessoa física presente no documento")

class RGdata(BaseModel):
    tipo_do_documento: str = Field(description="Tipo do documento (CNH, RG, ...)")
    nome_completo: str = Field(description="Nome Completo presente no documento")
    cpf: str = Field(description="CPF da pessoa física presente no documento")
    data_de_nascimento: str = Field(description="Data de nascimento da pessoa física presente no documento")
    filiacao: List[str] = Field(description="Filiação da pessoa física presente no documento")
