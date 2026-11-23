from rsa_modular_oaep_pss import (
    preparar,
    transformar,
    demonstrar_maleabilidade_rsa_bruto,
    demonstrar_rsa_biblioteca
)

if __name__ == "__main__":
    print("=== Caderno 11: Atividade 11 executada com sucesso ===")
    n, d = preparar(7, 13, 5)
    print(f"RSA didático gerado com n={n}, d={d}")
