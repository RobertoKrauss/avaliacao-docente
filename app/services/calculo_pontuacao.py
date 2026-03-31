from dataclasses import dataclass
from typing import Optional


@dataclass
class Regra:
    tipo_formula: str
    valor_base: Optional[float] = None
    divisor_unidade: Optional[float] = None
    pontuacao_maxima: Optional[float] = None
    exige_valor_manual: int = 0


def _aplicar_teto(valor: float, teto: Optional[float]) -> float:
    if teto is None:
        return max(valor, 0)
    return max(min(valor, teto), 0)


def calcular_pontuacao(
    regra: Regra,
    quantidade: Optional[float] = None,
    carga_horaria: Optional[float] = None,
    valor_manual: Optional[float] = None,
) -> float:
    """
    Calcula a pontuação estimada conforme os tipos de fórmula do spec.
    - fixo: usa valor_base
    - por_unidade: quantidade * valor_base
    - por_hora: (carga_horaria / divisor_unidade) * valor_base
    - intervalo/manual: exige valor_manual informado pelo usuário
    """
    tipo = regra.tipo_formula
    base = regra.valor_base or 0
    resultado = 0.0

    if tipo == "fixo":
        resultado = base
    elif tipo == "por_unidade":
        resultado = (quantidade or 0) * base
    elif tipo == "por_hora":
        divisor = regra.divisor_unidade or 1
        horas = carga_horaria or 0
        resultado = (horas / divisor) * base
    elif tipo in ("intervalo", "manual"):
        if valor_manual is None:
            raise ValueError("Valor manual é obrigatório para regras do tipo manual/intervalo.")
        resultado = valor_manual
    else:
        raise ValueError(f"Tipo de fórmula não suportado: {tipo}")

    return _aplicar_teto(resultado, regra.pontuacao_maxima)
