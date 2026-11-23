import secrets
from typing import Tuple


def euclides_estendido(a: int, b: int) -> Tuple[int, int, int]:
    """Calcula o Algoritmo de Euclides Estendido entre a e b.
    
    Retorna a tupla (mdc, x, y) tal que: a * x + b * y = mdc
    """
    if b == 0:
        return (a, 1, 0)
    mdc, x1, y1 = euclides_estendido(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (mdc, x, y)


def inverso_modular(a: int, n: int) -> int:
    """Calcula o inverso multiplicativo de a módulo n.
    
    Rejeita com ValueError se a e n não forem coprimos (mdc != 1) ou n <= 1.
    """
    if n <= 1:
        raise ValueError(f"O módulo deve ser maior que 1, recebido: {n}")
    
    mdc, x, _ = euclides_estendido(a, n)
    if mdc != 1:
        raise ValueError(f"O número {a} não possui inverso multiplicativo módulo {n} (mdc={mdc})")
    
    return x % n


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """Aplica XOR bit a bit entre duas sequências de bytes de mesmo tamanho."""
    if len(a) != len(b):
        raise ValueError(f"Sequências devem ter tamanhos iguais: len(a)={len(a)}, len(b)={len(b)}")
    return bytes(x ^ y for x, y in zip(a, b))


def experimentar_aleatoriedade(quantidade: int = 1000, tamanho_bytes: int = 12) -> bool:
    """Gera 'quantidade' de nonces usando secrets.token_bytes e verifica repetições."""
    conjunto_nonces = set()
    for _ in range(quantidade):
        n = secrets.token_bytes(tamanho_bytes)
        conjunto_nonces.add(n)
    return len(conjunto_nonces) == quantidade


def resolver_desafio() -> int:
    """Resolve o desafio: encontrar x em 17x = 1 (mod 43)."""
    return inverso_modular(17, 43)
