from modos_cbc_ctr import e, d, cbc, dec_cbc, ctr

if __name__ == "__main__":
    print("=== Caderno 08: Atividade 11 executada com sucesso ===")
    assert cbc([6, 6, 6], 5) == [6, 3, 8]
    assert ctr([6, 6, 6], 2) == [13, 10, 11]
    print("Modos CBC e CTR didáticos validados com precisão.")
