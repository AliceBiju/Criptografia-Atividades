from typing import List, Dict

SEGUNDOS_ANO = 365.25 * 24 * 60 * 60


def tempo_medio(bits_seguranca: int, testes_por_segundo: float, maquinas: int = 1) -> float:
    """Calcula o tempo médio em segundos para força bruta (metade do espaço: 2^(bits - 1))."""
    if bits_seguranca <= 0:
        raise ValueError(f"Bits de segurança deve ser positivo, recebido: {bits_seguranca}")
    if testes_por_segundo <= 0:
        raise ValueError(f"Taxa de testes deve ser positiva, recebido: {testes_por_segundo}")
    if maquinas <= 0:
        raise ValueError(f"Número de máquinas deve ser positivo, recebido: {maquinas}")

    tentativas_medias = 2 ** (bits_seguranca - 1)
    taxa_total = testes_por_segundo * maquinas
    return tentativas_medias / taxa_total


def em_anos(segundos: float) -> float:
    return segundos / SEGUNDOS_ANO


def em_horas(segundos: float) -> float:
    return segundos / 3600.0


CENARIOS = [
    ("DES (56 bits efetivos)", 56),
    ("3DES (força estimada)", 112),
    ("AES-128", 128),
    ("AES-256", 256),
]


def gerar_tabela_comparativa(taxa: float = 1e12, maquinas_lista: List[int] = None) -> List[Dict]:
    if maquinas_lista is None:
        maquinas_lista = [1, 10**3, 10**6, 10**9]
    linhas = []
    for nome, bits in CENARIOS:
        dados = {"nome": nome, "bits": bits, "resultados": {}}
        for m in maquinas_lista:
            seg = tempo_medio(bits, taxa, maquinas=m)
            dados["resultados"][m] = {
                "segundos": seg,
                "horas": em_horas(seg),
                "anos": em_anos(seg),
            }
        linhas.append(dados)
    return linhas
