import unittest

try:
    from .rsa_modular_oaep_pss import (
        preparar,
        transformar,
        demonstrar_maleabilidade_rsa_bruto,
        demonstrar_rsa_biblioteca
    )
except (ImportError, ValueError):
    from rsa_modular_oaep_pss import (
        preparar,
        transformar,
        demonstrar_maleabilidade_rsa_bruto,
        demonstrar_rsa_biblioteca
    )


class TestAtividade11(unittest.TestCase):
    def test_preparar_e_inverso_correto(self):
        n, d = preparar(7, 13, 5)
        self.assertEqual(n, 91)
        self.assertEqual(d, 29)
        self.assertEqual((5 * d) % 72, 1)

    def test_preparar_rejeita_expoente_nao_coprimo(self):
        with self.assertRaises(ValueError):
            preparar(5, 11, 10)

    def test_todos_os_representantes_de_0_a_n_menos_1(self):
        n, d = preparar(7, 13, 5)
        for m in range(n):
            c = transformar(m, 5, n)
            rec = transformar(c, d, n)
            self.assertEqual(rec, m)

    def test_transformar_rejeita_valores_fora_da_faixa(self):
        n, d = preparar(7, 13, 5)
        with self.assertRaises(ValueError):
            transformar(-1, 5, n)
        with self.assertRaises(ValueError):
            transformar(n, 5, n)
        with self.assertRaises(ValueError):
            transformar(n + 10, 5, n)

    def test_maleabilidade_rsa_bruto(self):
        res = demonstrar_maleabilidade_rsa_bruto(p=7, q=13, e=5, m=9, r=2)
        self.assertEqual(res["m_decifrado_alterado"], res["m_esperado"])
        self.assertEqual(res["m_esperado"], 18)

    def test_biblioteca_oaep_e_pss(self):
        res = demonstrar_rsa_biblioteca()
        self.assertTrue(res["capacidade_190_ok"])
        self.assertTrue(res["excedeu_191_rejeitado"])
        self.assertTrue(res["assinatura_verificada"])
        self.assertTrue(res["adulteracao_detectada"])


if __name__ == "__main__":
    unittest.main()
