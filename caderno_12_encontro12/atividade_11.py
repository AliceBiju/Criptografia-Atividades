from dh_subgrupo_elgamal import (
    validar,
    acordo_auditado,
    simular_ataque_mallory_encontro12,
    elgamal_cifrar,
    elgamal_decifrar
)

if __name__ == "__main__":
    print("=== Caderno 12: Atividade 11 executada com sucesso ===")
    assert acordo_auditado(2, 5) == (4, 9, 12, 12)
    print("Acordo auditado satisfeito.")
