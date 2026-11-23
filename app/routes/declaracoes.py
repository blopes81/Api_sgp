from fastapi import APIRouter, HTTPException, Depends, Query
from app.core.security import verify_api_key
from app.schemas.irp import DeclaracaoResumoSchema, DeclaracaoDetalheSchema, PaginacaoSchema, ReceitaSchema, BemDireitoSchema
from app.models.mock_data import DECLARACOES, RECEITAS, BENS_DIREITOS
import math

router = APIRouter(prefix="/declaracoes", tags=["Declarações IRP"])


@router.get("", response_model=dict, dependencies=[Depends(verify_api_key)])
async def listar_declaracoes(
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=100),
    ano_base: int = Query(None, description="Filtrar por ano-base"),
    cpf: str = Query(None, description="Filtrar por CPF do contribuinte"),
    situacao: str = Query(None, description="ENTREGUE | EM_PROCESSAMENTO | RETIFICADORA"),
):
    """Lista declarações de IRP com filtros opcionais."""
    dados = DECLARACOES

    if ano_base:
        dados = [d for d in dados if d["ano_base"] == ano_base]
    if cpf:
        dados = [d for d in dados if d["contribuinte_cpf"] == cpf]
    if situacao:
        dados = [d for d in dados if d["situacao"].upper() == situacao.upper()]

    total = len(dados)
    inicio = (pagina - 1) * por_pagina
    fim = inicio + por_pagina

    return {
        "dados": [DeclaracaoResumoSchema(**d) for d in dados[inicio:fim]],
        "paginacao": PaginacaoSchema(
            total=total,
            pagina=pagina,
            por_pagina=por_pagina,
            paginas=math.ceil(total / por_pagina) if total else 1,
        ),
    }


@router.get("/{declaracao_id}", response_model=DeclaracaoDetalheSchema, dependencies=[Depends(verify_api_key)])
async def buscar_declaracao(declaracao_id: int):
    """Retorna os detalhes completos de uma declaração, incluindo receitas e bens."""
    declaracao = next((d for d in DECLARACOES if d["id"] == declaracao_id), None)
    if not declaracao:
        raise HTTPException(status_code=404, detail="Declaração não encontrada")

    receitas = [ReceitaSchema(**r) for r in RECEITAS if r["declaracao_id"] == declaracao_id]
    bens = [BemDireitoSchema(**b) for b in BENS_DIREITOS if b["declaracao_id"] == declaracao_id]

    return DeclaracaoDetalheSchema(**declaracao, receitas=receitas, bens_direitos=bens)


@router.get("/{declaracao_id}/receitas", response_model=list[ReceitaSchema], dependencies=[Depends(verify_api_key)])
async def listar_receitas_declaracao(declaracao_id: int):
    """Lista todas as receitas/rendimentos de uma declaração."""
    declaracao = next((d for d in DECLARACOES if d["id"] == declaracao_id), None)
    if not declaracao:
        raise HTTPException(status_code=404, detail="Declaração não encontrada")

    receitas = [r for r in RECEITAS if r["declaracao_id"] == declaracao_id]
    return [ReceitaSchema(**r) for r in receitas]


@router.get("/{declaracao_id}/bens", response_model=list[BemDireitoSchema], dependencies=[Depends(verify_api_key)])
async def listar_bens_declaracao(declaracao_id: int):
    """Lista todos os bens e direitos declarados."""
    declaracao = next((d for d in DECLARACOES if d["id"] == declaracao_id), None)
    if not declaracao:
        raise HTTPException(status_code=404, detail="Declaração não encontrada")

    bens = [b for b in BENS_DIREITOS if b["declaracao_id"] == declaracao_id]
    return [BemDireitoSchema(**b) for b in bens]
