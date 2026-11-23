import unittest

try:
    from .modos_cbc_ctr import e, d, cbc, dec_cbc, ctr
except (ImportError, ValueError):
    from modos_cbc_ctr import e, d, cbc, dec_cbc, ctr


class TestAtividade08(unittest.TestCase):
    def test_bijeção_cifra_didatica_todos_os_16_valores(self):
        for x in range(16):
            self.assertEqual(d(e(x)), x)

    def test_cbc_valores_do_caderno(self):
        msg = [6, 6, 6]
        c = cbc(msg, 5)
        self.assertEqual(c, [6, 3, 8])
        self.assertEqual(dec_cbc(c, 5), msg)

    def test_ctr_valores_do_caderno(self):
        msg = [6, 6, 6]
        c = ctr(msg, 2)
        self.assertEqual(c, [13, 10, 11])
        self.assertEqual(ctr(c, 2), msg)

    def test_ctr_esgotamento_contador_rejeita(self):
        with self.assertRaises(ValueError):
            ctr([1, 2, 3, 4, 5], nonce=1)

    def test_ctr_inicio_deslocado_rejeita_ao_ultrapassar(self):
        with self.assertRaises(ValueError):
            ctr([1, 2], nonce=0, inicio=3)

    def test_validacao_campos_invalidos_cbc_e_ctr(self):
        with self.assertRaises(ValueError):
            cbc([16], 0)
        with self.assertRaises(ValueError):
            cbc([0], 16)
        with self.assertRaises(ValueError):
            ctr([0], 4)
        with self.assertRaises(ValueError):
            ctr([0], 0, inicio=4)

    def test_maleabilidade_ctr_bit_a_bit(self):
        msg = [6]
        c = ctr(msg, nonce=1)
        c_mod = [c[0] ^ 1]
        m_mod = ctr(c_mod, nonce=1)
        self.assertEqual(m_mod[0], msg[0] ^ 1)


if __name__ == "__main__":
    unittest.main()
