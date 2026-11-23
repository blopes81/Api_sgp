from fastapi import APIRouter, HTTPException, Depends, Query
from app.core.security import verify_api_key
from app.schemas.irp import ContribuinteSchema, PaginacaoSchema
from app.models.mock_data import CONTRIBUINTES
import math

router = APIRouter(prefix="/contribuintes", tags=["Contribuintes"])


@router.get("", response_model=dict, dependencies=[Depends(verify_api_key)])
async def listar_contribuintes(
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(10, ge=1, le=100),
    nome: str = Query(None, description="Filtrar por nome (parcial)"),
    uf: str = Query(None, description="Filtrar por UF"),
):
    """Lista todos os contribuintes cadastrados no SGP."""
    dados = CONTRIBUINTES

    if nome:
        dados = [c for c in dados if nome.lower() in c["nome"].lower()]
    if uf:
        dados = [c for c in dados if c["uf"].upper() == uf.upper()]

    total = len(dados)
    inicio = (pagina - 1) * por_pagina
    fim = inicio + por_pagina

    return {
        "dados": [ContribuinteSchema(**c) for c in dados[inicio:fim]],
        "paginacao": PaginacaoSchema(
            total=total,
            pagina=pagina,
            por_pagina=por_pagina,
            paginas=math.ceil(total / por_pagina) if total else 1,
        ),
    }


@router.get("/{cpf}", response_model=ContribuinteSchema, dependencies=[Depends(verify_api_key)])
async def buscar_contribuinte_por_cpf(cpf: str):
    """Busca um contribuinte pelo CPF."""
    contribuinte = next((c for c in CONTRIBUINTES if c["cpf"] == cpf), None)
    if not contribuinte:
        raise HTTPException(status_code=404, detail="Contribuinte não encontrado")
    return ContribuinteSchema(**contribuinte)
