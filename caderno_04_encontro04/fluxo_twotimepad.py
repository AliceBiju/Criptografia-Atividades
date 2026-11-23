from functools import reduce


def xor_bytes(*valores: bytes) -> bytes:
    """Aplica XOR bit a bit entre duas ou mais sequências de bytes de mesmo tamanho."""
    if not valores:
        return b""
    tamanho = len(valores[0])
    for v in valores:
        if len(v) != tamanho:
            raise ValueError(f"Sequências com comprimentos divergentes: esperado {tamanho}, obtido {len(v)}")
    return bytes(reduce(lambda a, b: a ^ b, coluna) for coluna in zip(*valores))


def demonstrar_two_time_pad():
    """Demonstra que reutilizar o fluxo S cancela a chave: C1 ^ C2 = M1 ^ M2."""
    m1 = b"pagar=1000"
    m2 = b"pagar=9000"
    fluxo_reutilizado = bytes.fromhex("00112233445566778899")

    c1 = xor_bytes(m1, fluxo_reutilizado)
    c2 = xor_bytes(m2, fluxo_reutilizado)

    xor_cifras = xor_bytes(c1, c2)
    xor_mensagens = xor_bytes(m1, m2)
    assert xor_cifras == xor_mensagens

    recuperada = xor_bytes(c1, c2, m1)
    assert recuperada == m2

    return {
        "m1": m1,
        "m2": m2,
        "c1_hex": c1.hex(),
        "c2_hex": c2.hex(),
        "xor_cifras_hex": xor_cifras.hex(),
        "recuperada": recuperada
    }


def demonstrar_maleabilidade(cifra: bytes, fluxo: bytes, posicao_byte: int = 6, bit: int = 2) -> bytes:
    """Demonstra que inverter bit na cifra inverte o mesmo bit no texto claro."""
    delta = bytearray(len(cifra))
    delta[posicao_byte] = 1 << bit
    cifra_modificada = xor_bytes(cifra, bytes(delta))
    return xor_bytes(cifra_modificada, fluxo)
