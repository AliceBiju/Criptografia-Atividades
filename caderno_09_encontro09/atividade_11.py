from registro_aead import (
    ReceptorAEAD,
    montar_aad,
    montar_nonce,
    executar_atividade
)

if __name__ == "__main__":
    print("=== Caderno 09: Atividade 11 executada com sucesso ===")
    res = executar_atividade()
    print(f"Mensagem recuperada via AEAD: {res['recuperada'].decode()}")
