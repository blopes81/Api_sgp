from decimal import Decimal
from datetime import date

# Dados simulados - substituir pela conexão real com o banco do SGP
CONTRIBUINTES = [
    {
        "id": 1,
        "cpf": "123.456.789-00",
        "nome": "João da Silva",
        "data_nascimento": date(1980, 5, 15),
        "municipio": "São Paulo",
        "uf": "SP",
    },
    {
        "id": 2,
        "cpf": "987.654.321-00",
        "nome": "Maria Oliveira",
        "data_nascimento": date(1975, 11, 30),
        "municipio": "Rio de Janeiro",
        "uf": "RJ",
    },
]

DECLARACOES = [
    {
        "id": 1,
        "contribuinte_cpf": "123.456.789-00",
        "contribuinte_nome": "João da Silva",
        "ano_base": 2024,
        "tipo": "COMPLETA",
        "situacao": "ENTREGUE",
        "data_entrega": date(2025, 3, 20),
        "numero_recibo": "1.1.2025.1234567890-1",
        "total_rendimentos_tributaveis": Decimal("85000.00"),
        "total_deducoes": Decimal("20000.00"),
        "base_calculo": Decimal("65000.00"),
        "imposto_devido": Decimal("12000.00"),
        "imposto_retido_fonte": Decimal("10500.00"),
        "imposto_a_pagar": None,
        "imposto_a_restituir": Decimal("1500.00"),
    },
    {
        "id": 2,
        "contribuinte_cpf": "987.654.321-00",
        "contribuinte_nome": "Maria Oliveira",
        "ano_base": 2024,
        "tipo": "SIMPLIFICADA",
        "situacao": "ENTREGUE",
        "data_entrega": date(2025, 4, 10),
        "numero_recibo": "1.1.2025.9876543210-2",
        "total_rendimentos_tributaveis": Decimal("42000.00"),
        "total_deducoes": Decimal("8000.00"),
        "base_calculo": Decimal("34000.00"),
        "imposto_devido": Decimal("4200.00"),
        "imposto_retido_fonte": Decimal("3800.00"),
        "imposto_a_pagar": Decimal("400.00"),
        "imposto_a_restituir": None,
    },
]

RECEITAS = [
    {
        "id": 1,
        "declaracao_id": 1,
        "descricao": "Rendimentos do Trabalho Assalariado",
        "fonte_pagadora_cnpj": "11.222.333/0001-44",
        "fonte_pagadora_nome": "Empresa ABC Ltda",
        "valor_rendimento": Decimal("72000.00"),
        "valor_ir_retido": Decimal("9000.00"),
    },
    {
        "id": 2,
        "declaracao_id": 1,
        "descricao": "Rendimentos de Aluguéis",
        "fonte_pagadora_cnpj": None,
        "fonte_pagadora_nome": "Locatário Pessoa Física",
        "valor_rendimento": Decimal("13000.00"),
        "valor_ir_retido": Decimal("1500.00"),
    },
    {
        "id": 3,
        "declaracao_id": 2,
        "descricao": "Rendimentos do Trabalho Assalariado",
        "fonte_pagadora_cnpj": "55.666.777/0001-88",
        "fonte_pagadora_nome": "Comércio XYZ S.A.",
        "valor_rendimento": Decimal("42000.00"),
        "valor_ir_retido": Decimal("3800.00"),
    },
]

BENS_DIREITOS = [
    {
        "id": 1,
        "declaracao_id": 1,
        "codigo": "11",
        "discriminacao": "Apartamento situado na Rua das Flores, 123, São Paulo/SP",
        "situacao_ano_anterior": Decimal("350000.00"),
        "situacao_ano_atual": Decimal("350000.00"),
    },
    {
        "id": 2,
        "declaracao_id": 1,
        "codigo": "21",
        "discriminacao": "Veículo Honda Civic, Placa ABC-1234, ano 2022",
        "situacao_ano_anterior": Decimal("95000.00"),
        "situacao_ano_atual": Decimal("80000.00"),
    },
]
