import unittest

try:
    from .dh_subgrupo_elgamal import (
        validar,
        acordo_auditado,
        simular_ataque_mallory_encontro12,
        elgamal_cifrar,
        elgamal_decifrar,
        P, Q, G
    )
except (ImportError, ValueError):
    from dh_subgrupo_elgamal import (
        validar,
        acordo_auditado,
        simular_ataque_mallory_encontro12,
        elgamal_cifrar,
        elgamal_decifrar,
        P, Q, G
    )


class TestAtividade12(unittest.TestCase):
    def test_contratos_do_caderno(self):
        self.assertEqual(acordo_auditado(2, 5), (4, 9, 12, 12))
        self.assertTrue(validar(4))
        self.assertFalse(validar(5))
        self.assertFalse(validar(True))

    def test_validar_publicas_casos_positivos_e_negativos(self):
        self.assertFalse(validar(-1))
        self.assertFalse(validar(0))
        self.assertFalse(validar(1))
        self.assertTrue(validar(4))
        self.assertFalse(validar(5))
        self.assertFalse(validar(22))
        self.assertFalse(validar(23))
        self.assertFalse(validar(True))
        self.assertFalse(validar(2.0))

    def test_rejeicao_privadas_invalidas(self):
        for invalida in [0, 11, -1, True, 2.5]:
            with self.assertRaises(ValueError):
                acordo_auditado(invalida, 5)
            with self.assertRaises(ValueError):
                acordo_auditado(2, invalida)

    def test_todos_os_100_pares_de_privadas(self):
        contagem = 0
        for a in range(1, 11):
            for b in range(1, 11):
                A, B, s_a, s_b = acordo_auditado(a, b)
                self.assertEqual(s_a, s_b)
                contagem += 1
        self.assertEqual(contagem, 100)

    def test_conferencia_manual_tres_pares(self):
        self.assertEqual(acordo_auditado(2, 3), (4, 8, 18, 18))
        self.assertEqual(acordo_auditado(4, 3), (16, 8, 2, 2))
        self.assertEqual(acordo_auditado(1, 1), (2, 2, 2, 2))

    def test_simulacao_mallory_mitm(self):
        res = simular_ataque_mallory_encontro12()
        self.assertTrue(res["U_valido"])
        self.assertTrue(res["V_valido"])
        self.assertEqual(res["s_alice_mallory"], 4)
        self.assertEqual(res["s_bob_mallory"], 12)

    def test_elgamal_ida_e_volta(self):
        x = 3
        y = pow(G, x, P)
        m = 6
        k = 4
        c1, c2 = elgamal_cifrar(m, y, k)
        self.assertEqual((c1, c2), (16, 12))
        m_rec = elgamal_decifrar(c1, c2, x)
        self.assertEqual(m_rec, m)


if __name__ == "__main__":
    unittest.main()
