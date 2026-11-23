from typing import List


def e(x: int, k: int = 3) -> int:
    """Cifra de bloco didática de 4 bits: (x + k) mod 16."""
    return (x + k) % 16


def d(y: int, k: int = 3) -> int:
    """Decifração da cifra de 4 bits: (y - k) mod 16."""
    return (y - k) % 16


def cbc(blocos: List[int], iv: int) -> List[int]:
    """Cifra blocos em modo CBC: C_i = e(M_i ^ C_{i-1})."""
    if not (0 <= iv <= 15):
        raise ValueError(f"IV deve ter 4 bits (0 a 15), recebido: {iv}")
    cifrados = []
    anterior = iv
    for b in blocos:
        if not (0 <= b <= 15):
            raise ValueError(f"Bloco claro deve ter 4 bits (0 a 15), recebido: {b}")
        c = e(b ^ anterior)
        cifrados.append(c)
        anterior = c
    return cifrados


def dec_cbc(blocos: List[int], iv: int) -> List[int]:
    """Decifra blocos no modo CBC: M_i = d(C_i) ^ C_{i-1}."""
    if not (0 <= iv <= 15):
        raise ValueError(f"IV deve ter 4 bits (0 a 15), recebido: {iv}")
    claros = []
    anterior = iv
    for c in blocos:
        if not (0 <= c <= 15):
            raise ValueError(f"Bloco cifrado deve ter 4 bits (0 a 15), recebido: {c}")
        m = d(c) ^ anterior
        claros.append(m)
        anterior = c
    return claros


def ctr(blocos: List[int], nonce: int, inicio: int = 0) -> List[int]:
    """Cifra/decifra blocos no modo CTR com nonce e contador de 2 bits."""
    if not (0 <= nonce <= 3):
        raise ValueError(f"Nonce de 2 bits deve estar entre 0 e 3, recebido: {nonce}")
    if not (0 <= inicio <= 3):
        raise ValueError(f"Contador inicial deve estar entre 0 e 3, recebido: {inicio}")
    if inicio + len(blocos) > 4:
        raise ValueError(f"Esgotamento do contador de 2 bits: {inicio + len(blocos)} excede o limite de 4")

    resultado = []
    for offset, b in enumerate(blocos):
        if not (0 <= b <= 15):
            raise ValueError(f"Bloco deve ter 4 bits (0 a 15), recebido: {b}")
        contador = inicio + offset
        t = (nonce << 2) | contador
        fluxo = e(t)
        resultado.append(b ^ fluxo)
    return resultado
