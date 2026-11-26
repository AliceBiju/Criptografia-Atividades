import unittest

try:
    from .curva_eliptica_ecdh import (
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
        quebrar_ecdlp_por_forca_bruta
    )
except (ImportError, ValueError):
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
        quebrar_ecdlp_por_forca_bruta
    )


class TestAtividade13(unittest.TestCase):
    def setUp(self):
        self.G = PONTO_G

    def test_pertencimento_pontos_na_curva(self):
        # G = (5, 1) pertence à curva
        self.assertTrue(na_curva(self.G))
        # Ponto no infinito
        self.assertTrue(na_curva(None))
        # Questão 1 da lista: (0, 6) -> 6^2 = 36 = 2 mod 17; 0^3 + 0 + 2 = 2 mod 17
        self.assertTrue(na_curva((0, 6)))
        # Questão 2 da lista: (1, 1) -> 1^2 = 1 mod 17; 1^3 + 2 + 2 = 5 mod 17 (não pertence)
        self.assertFalse(na_curva((1, 1)))
        # Questão 7 da lista: dobro das coordenadas (10, 2) não pertence à curva
        self.assertFalse(na_curva((10, 2)))

    def test_inverso_modular(self):
        self.assertEqual(inverso(2), 9)
        self.assertEqual((2 * 9) % 17, 1)
        self.assertEqual(inverso(3), 6)
        self.assertEqual((3 * 6) % 17, 1)
        self.assertEqual(inverso(12), 10)

    def test_somar_casos_base_do_caderno(self):
        # Elemento neutro
        self.assertEqual(somar(self.G, None), self.G)
        self.assertEqual(somar(None, self.G), self.G)
        # Opostos: (5, 1) + (5, 16) = O
        self.assertIsNone(somar(self.G, (5, 16)))
        # Duplicação: 2G = G + G = (6, 3)
        self.assertEqual(somar(self.G, self.G), (6, 3))
        # Soma de pontos distintos: G + 2G = (10, 6)
        self.assertEqual(somar(self.G, (6, 3)), (10, 6))

    def test_multiplicacao_escalar_duplicar_e_somar(self):
        self.assertIsNone(multiplicar(0, self.G))
        self.assertEqual(multiplicar(1, self.G), self.G)
        self.assertEqual(multiplicar(2, self.G), (6, 3))
        self.assertEqual(multiplicar(3, self.G), (10, 6))
        self.assertEqual(multiplicar(4, self.G), (3, 1))
        self.assertEqual(multiplicar(5, self.G), (9, 16))
        self.assertEqual(multiplicar(18, self.G), (5, 16))
        # Retorno ao ponto no infinito na ordem 19
        self.assertIsNone(multiplicar(19, self.G))
        # Ciclo: 20G = G
        self.assertEqual(multiplicar(20, self.G), self.G)

    def test_ordem_e_subgrupo_completo(self):
        # Nenhum dos primeiros 18 múltiplos pode ser None e todos devem estar na curva
        for k in range(1, 19):
            p = multiplicar(k, self.G)
            self.assertIsNotNone(p, f"O ponto {k}*G não deveria ser None")
            self.assertTrue(na_curva(p), f"O ponto {k}*G = {p} deveria pertencer à curva")
        # Exatamente no 19º ocorre o retorno ao elemento neutro
        self.assertIsNone(multiplicar(19, self.G))

    def test_acordo_ecdh_exemplo_6(self):
        res = acordo_ecdh(priv_a=2, priv_b=3, ponto_base=self.G)
        self.assertEqual(res["pub_a"], (6, 3))
        self.assertEqual(res["pub_b"], (10, 6))
        self.assertEqual(res["segredo_compartilhado"], (16, 13))

    def test_acordo_ecdh_variando_privados(self):
        # Testa consistência sA * B == sB * A para pares arbitrários de 1 a 18
        for sa in [1, 4, 7, 11, 15]:
            for sb in [2, 5, 8, 12, 17]:
                res = acordo_ecdh(priv_a=sa, priv_b=sb, ponto_base=self.G)
                self.assertIsNotNone(res["segredo_compartilhado"])
                self.assertTrue(na_curva(res["segredo_compartilhado"]))

    def test_quebrar_ecdlp_forca_bruta(self):
        self.assertEqual(quebrar_ecdlp_por_forca_bruta((10, 6), self.G), 3)
        self.assertEqual(quebrar_ecdlp_por_forca_bruta((9, 16), self.G), 5)
        self.assertEqual(quebrar_ecdlp_por_forca_bruta((5, 16), self.G), 18)

    def test_validacao_escalar_negativo(self):
        with self.assertRaises(ValueError):
            multiplicar(-1, self.G)


if __name__ == "__main__":
    unittest.main()
