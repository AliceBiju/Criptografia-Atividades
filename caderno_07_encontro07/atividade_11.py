from aes_corpo_finito import xtime, gf_mul, mix_column

if __name__ == "__main__":
    print("=== Caderno 07: Atividade 11 executada com sucesso ===")
    assert xtime(0x57) == 0xAE
    assert gf_mul(0x57, 0x13) == 0xFE
    print("Aritmética do corpo finito do AES conferida.")
