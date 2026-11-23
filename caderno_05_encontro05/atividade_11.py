from feistel_reversivel import (
    f,
    rodada,
    rodada_inversa,
    cifrar,
    decifrar,
    distancia_hamming,
    medir_avalanche
)

if __name__ == "__main__":
    print("=== Caderno 05: Atividade 11 executada com sucesso ===")
    chaves = [3, 17, 91, 201]
    for b in [0x0000, 0x1234, 0xFFFF]:
        assert decifrar(cifrar(b, chaves), chaves) == b
    print("Ida e volta conferida.")
