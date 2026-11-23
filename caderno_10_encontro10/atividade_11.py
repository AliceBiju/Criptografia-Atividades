from x25519_hkdf_mitm import (
    derivar_chave,
    executar_acordo_legitimo,
    simular_ataque_intermediario_mallory
)

if __name__ == "__main__":
    print("=== Caderno 10: Atividade 11 executada com sucesso ===")
    res = executar_acordo_legitimo()
    print(f"Acordo X25519 + HKDF + AESGCM: {res['mensagem_recuperada'].decode()}")
