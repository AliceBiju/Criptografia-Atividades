from cesar_frequencia import (
    cesar,
    decifrar,
    candidatas,
    ordenar_candidatas,
    cifrar_composta,
    decifrar_composta
)

if __name__ == "__main__":
    print("=== Caderno 03: Atividade 11 executada com sucesso ===")
    frase = "ATAQUE AO AMANHECER"
    cifrado = cesar(frase, 7)
    print(f"Cifrado: {cifrado}")
    print(f"Decifrado: {decifrar(cifrado, 7)}")
