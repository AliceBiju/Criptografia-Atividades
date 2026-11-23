from typing import List, Tuple


def f(metade: int, subchave: int) -> int:
    """Função de rodada didática: soma com a subchave módulo 256."""
    return (metade + subchave) % 256


def rodada(esquerda: int, direita: int, subchave: int) -> Tuple[int, int]:
    """Aplica uma rodada da rede de Feistel direta: L' = R; R' = L ^ F(R, K)."""
    return (direita & 0xFF), ((esquerda ^ f(direita, subchave)) & 0xFF)


def rodada_inversa(esquerda: int, direita: int, subchave: int) -> Tuple[int, int]:
    """Desfaz uma rodada da rede de Feistel: R_antigo = L; L_antigo = R ^ F(L, K)."""
    return ((direita ^ f(esquerda, subchave)) & 0xFF), (esquerda & 0xFF)


def cifrar(bloco: int, subchaves: List[int]) -> int:
    """Cifra bloco de 16 bits aplicando as rodadas com subchaves."""
    if not (0 <= bloco <= 0xFFFF):
        raise ValueError(f"O bloco deve ter 16 bits (0 a 0xFFFF), recebido: {hex(bloco)}")
        
    esquerda = (bloco >> 8) & 0xFF
    direita = bloco & 0xFF
    
    for k in subchaves:
        esquerda, direita = rodada(esquerda, direita, k)
        
    return (esquerda << 8) | direita


def decifrar(bloco: int, subchaves: List[int]) -> int:
    """Decifra bloco de 16 bits percorrendo subchaves em ordem inversa."""
    if not (0 <= bloco <= 0xFFFF):
        raise ValueError(f"O bloco deve ter 16 bits (0 a 0xFFFF), recebido: {hex(bloco)}")
        
    esquerda = (bloco >> 8) & 0xFF
    direita = bloco & 0xFF
    
    for k in reversed(subchaves):
        esquerda, direita = rodada_inversa(esquerda, direita, k)
        
    return (esquerda << 8) | direita


def distancia_hamming(a: int, b: int) -> int:
    """Calcula a distância de Hamming entre dois inteiros."""
    return bin(a ^ b).count("1")


def medir_avalanche(bloco_original: int, subchaves: List[int], bit_a_inverter: int = 0) -> Tuple[int, int, float]:
    """Inverte um bit na entrada e calcula a distância de Hamming na saída."""
    bloco_modificado = bloco_original ^ (1 << bit_a_inverter)
    c_orig = cifrar(bloco_original, subchaves)
    c_mod = cifrar(bloco_modificado, subchaves)
    bits_mudados = distancia_hamming(c_orig, c_mod)
    porcentagem = (bits_mudados / 16) * 100
    return c_orig, c_mod, porcentagem
