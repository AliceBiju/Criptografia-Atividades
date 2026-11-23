import unittest
import secrets

try:
    from .inverso_modular_xor import (
        euclides_estendido,
        inverso_modular,
        xor_bytes,
        experimentar_aleatoriedade,
        resolver_desafio
    )
except (ImportError, ValueError):
    from inverso_modular_xor import (
        euclides_estendido,
        inverso_modular,
        xor_bytes,
        experimentar_aleatoriedade,
        resolver_desafio
    )


class TestAtividade02(unittest.TestCase):
    def test_euclides_estendido(self):
        mdc, x, y = euclides_estendido(7, 26)
        self.assertEqual(mdc, 1)
        self.assertEqual(7 * x + 26 * y, 1)

    def test_inverso_modular_valido(self):
        inv = inverso_modular(7, 26)
        self.assertEqual(inv, 15)
        self.assertEqual((7 * inv) % 26, 1)

    def test_inverso_modular_invalido_rejeita(self):
        with self.assertRaises(ValueError):
            inverso_modular(6, 26)

    def test_inverso_modular_modulo_invalido(self):
        with self.assertRaises(ValueError):
            inverso_modular(5, 1)

    def test_xor_bytes_correto(self):
        a = bytes.fromhex("0f")
        b = bytes.fromhex("f0")
        self.assertEqual(xor_bytes(a, b).hex(), "ff")

    def test_xor_bytes_propriedade_reversivel(self):
        m = b"dados_secretos_12"
        k = secrets.token_bytes(len(m))
        c = xor_bytes(m, k)
        m_rec = xor_bytes(c, k)
        self.assertEqual(m, m_rec)

    def test_xor_bytes_tamanhos_diferentes_rejeita(self):
        a = b"123"
        b = b"1234"
        with self.assertRaises(ValueError):
            xor_bytes(a, b)

    def test_aleatoriedade_1000_nonces(self):
        self.assertTrue(experimentar_aleatoriedade(1000, 12))

    def test_desafio_17x_mod_43(self):
        x = resolver_desafio()
        self.assertEqual(x, 38)
        self.assertEqual((17 * x) % 43, 1)


if __name__ == "__main__":
    unittest.main()
