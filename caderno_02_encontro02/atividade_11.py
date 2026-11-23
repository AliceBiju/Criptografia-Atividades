from inverso_modular_xor import (
    euclides_estendido,
    inverso_modular,
    xor_bytes,
    experimentar_aleatoriedade,
    resolver_desafio
)

if __name__ == "__main__":
    print("=== Caderno 02: Atividade 11 executada com sucesso ===")
    print(f"Inverso de 7 mod 26: {inverso_modular(7, 26)}")
    print(f"Desafio 17x = 1 mod 43: x = {resolver_desafio()}")
