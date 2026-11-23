from fluxo_twotimepad import (
    xor_bytes,
    demonstrar_two_time_pad,
    demonstrar_maleabilidade
)

if __name__ == "__main__":
    print("=== Caderno 04: Atividade 11 executada com sucesso ===")
    res = demonstrar_two_time_pad()
    print(f"M2 recuperada: {res['recuperada'].decode()}")
