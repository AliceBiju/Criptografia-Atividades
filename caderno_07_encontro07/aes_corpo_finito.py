from typing import List


def xtime(valor: int) -> int:
    """Multiplica por x (0x02) em GF(2^8) com redução pelo polinômio 0x11B."""
    if not (0 <= valor <= 0xFF):
        raise ValueError(f"Valor fora do intervalo de byte (0x00 a 0xFF): {hex(valor)}")
    resultado = (valor << 1) & 0xFF
    if valor & 0x80:
        resultado ^= 0x1B
    return resultado


def gf_mul(a: int, b: int) -> int:
    """Multiplica dois elementos em GF(2^8) pelo método de deslocar e somar por XOR."""
    if not (0 <= a <= 0xFF and 0 <= b <= 0xFF):
        raise ValueError("Ambos os operandos devem ser bytes válidos (0x00 a 0xFF)")
    acumulador = 0
    parcela_atual = a
    for i in range(8):
        if (b >> i) & 1:
            acumulador ^= parcela_atual
        parcela_atual = xtime(parcela_atual)
    return acumulador


def mix_column(coluna: List[int]) -> List[int]:
    """Aplica MixColumns a uma coluna de 4 bytes do AES."""
    if len(coluna) != 4:
        raise ValueError("MixColumns requer exatamente uma coluna de 4 bytes")
    c0, c1, c2, c3 = coluna
    b0 = gf_mul(0x02, c0) ^ gf_mul(0x03, c1) ^ c2 ^ c3
    b1 = c0 ^ gf_mul(0x02, c1) ^ gf_mul(0x03, c2) ^ c3
    b2 = c0 ^ c1 ^ gf_mul(0x02, c2) ^ gf_mul(0x03, c3)
    b3 = gf_mul(0x03, c0) ^ c1 ^ c2 ^ gf_mul(0x02, c3)
    return [b0, b1, b2, b3]
