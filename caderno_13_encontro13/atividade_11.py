from curva_eliptica_ecdh import (
    P_MOD,
    A_CURVA,
    B_CURVA,
    PONTO_G,
    ORDEM_G,
    na_curva,
    inverso,
    somar,
    multiplicar,
    acordo_ecdh,
    quebrar_ecdlp_por_forca_bruta,
    listar_subgrupo_gerado
)

G = PONTO_G

if __name__ == "__main__":
    print("=== Caderno 13: Curvas Elípticas — Das Contas ao Acordo de Chaves ===")
    print("G pertence à curva?", na_curva(G))
    print("Inverso de 2 mod 17:", inverso(2))

    # Testes básicos da Atividade 11 do caderno
    assert somar(G, None) == G
    assert somar(G, (5, 16)) is None
    assert somar(G, G) == (6, 3)
    assert somar(G, (6, 3)) == (10, 6)
    assert multiplicar(5, G) == (9, 16)
    print("Testes básicos do código inicial aprovados com sucesso!")

    # Testes de ordem e fronteira
    assert multiplicar(0, G) is None
    assert multiplicar(1, G) == G
    assert multiplicar(19, G) is None
    assert multiplicar(20, G) == G
    print("Comportamento cíclico (0G=O, 1G=G, 19G=O, 20G=G) validado com sucesso!")

    # Enumeração dos múltiplos
    print("\n--- Subgrupo gerado por G=(5, 1) na curva y^2 = x^3 + 2x + 2 mod 17 ---")
    multiplos = listar_subgrupo_gerado(G, ORDEM_G)
    for k, ponto in multiplos:
        rotulo = "O (ponto no infinito)" if ponto is None else f"{ponto}"
        print(f"  {k:2d} * G = {rotulo}")
        assert na_curva(ponto), f"Ponto {ponto} não pertence à curva!"
    print(f"Todos os {ORDEM_G} pontos pertencem à curva e o primeiro retorno a O ocorre exatamente em k={ORDEM_G}.")

    # Acordo ECDH do Exemplo 6
    print("\n--- Reprodução do Exemplo 6: Acordo ECDH ---")
    res_ecdh = acordo_ecdh(priv_a=2, priv_b=3, ponto_base=G)
    print(f"Alice escolhe s_A = 2 -> Publica A = 2G = {res_ecdh['pub_a']}")
    print(f"Bob escolhe s_B = 3   -> Publica B = 3G = {res_ecdh['pub_b']}")
    print(f"Segredo compartilhado calculado em comum: {res_ecdh['segredo_compartilhado']}")
    assert res_ecdh['pub_a'] == (6, 3)
    assert res_ecdh['pub_b'] == (10, 6)
    assert res_ecdh['segredo_compartilhado'] == (16, 13)

    # Quebra de ECDLP por força bruta na curva didática pequena
    print("\n--- Quebra do ECDLP por Força Bruta ---")
    alvo_bob = (10, 6)
    chave_recuperada = quebrar_ecdlp_por_forca_bruta(alvo_bob, G, ORDEM_G)
    print(f"Dada a chave pública B = {alvo_bob}, o atacante encontrou o privado s_B = {chave_recuperada} em 3 passos!")
    assert chave_recuperada == 3
    print("Sucesso: todos os objetivos da Atividade 11 foram executados.")
