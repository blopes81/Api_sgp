from pydantic import BaseModel
from datetime import date
from typing import Optional
from decimal import Decimal


class ContribuinteSchema(BaseModel):
    id: int
    cpf: str
    nome: str
    data_nascimento: date
    municipio: str
    uf: str

    class Config:
        from_attributes = True


class DeclaracaoResumoSchema(BaseModel):
    id: int
    contribuinte_cpf: str
    contribuinte_nome: str
    ano_base: int
    tipo: str  # "COMPLETA" ou "SIMPLIFICADA"
    situacao: str  # "ENTREGUE", "EM_PROCESSAMENTO", "RETIFICADORA"
    data_entrega: Optional[date]
    numero_recibo: Optional[str]

    class Config:
        from_attributes = True


class ReceitaSchema(BaseModel):
    id: int
    declaracao_id: int
    descricao: str
    fonte_pagadora_cnpj: Optional[str]
    fonte_pagadora_nome: Optional[str]
    valor_rendimento: Decimal
    valor_ir_retido: Decimal

    class Config:
        from_attributes = True


class BemDireitoSchema(BaseModel):
    id: int
    declaracao_id: int
    codigo: str
    discriminacao: str
    situacao_ano_anterior: Decimal
    situacao_ano_atual: Decimal

    class Config:
        from_attributes = True


class DividaOnus(BaseModel):
    id: int
    declaracao_id: int
    codigo: str
    credor: str
    valor: Decimal

    class Config:
        from_attributes = True


class DeclaracaoDetalheSchema(BaseModel):
    id: int
    contribuinte_cpf: str
    contribuinte_nome: str
    ano_base: int
    tipo: str
    situacao: str
    data_entrega: Optional[date]
    numero_recibo: Optional[str]
    total_rendimentos_tributaveis: Decimal
    total_deducoes: Decimal
    base_calculo: Decimal
    imposto_devido: Decimal
    imposto_retido_fonte: Decimal
    imposto_a_pagar: Optional[Decimal]
    imposto_a_restituir: Optional[Decimal]
    receitas: list[ReceitaSchema] = []
    bens_direitos: list[BemDireitoSchema] = []

    class Config:
        from_attributes = True


class PaginacaoSchema(BaseModel):
    total: int
    pagina: int
    por_pagina: int
    paginas: int
