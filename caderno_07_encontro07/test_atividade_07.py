import unittest

try:
    from .aes_corpo_finito import xtime, gf_mul, mix_column
except (ImportError, ValueError):
    from aes_corpo_finito import xtime, gf_mul, mix_column


class TestAtividade07(unittest.TestCase):
    def test_xtime_valores_de_referencia(self):
        self.assertEqual(xtime(0x57), 0xAE)
        self.assertEqual(xtime(0xAE), 0x47)
        self.assertEqual(xtime(0x47), 0x8E)
        self.assertEqual(xtime(0x8E), 0x07)

    def test_gf_mul_exemplo_caderno(self):
        self.assertEqual(gf_mul(0x57, 0x13), 0xFE)

    def test_gf_mul_propriedades_algebraicas_todos_os_bytes(self):
        for b in range(256):
            self.assertEqual(gf_mul(b, 0x00), 0x00)
            self.assertEqual(gf_mul(b, 0x01), b)
            self.assertEqual(gf_mul(b, 0x02), xtime(b))
            self.assertEqual(gf_mul(0x00, b), 0x00)
            self.assertEqual(gf_mul(0x01, b), b)

    def test_comutatividade_gf_mul(self):
        amostras = [0x57, 0x13, 0xD4, 0xBF, 0x03, 0x02]
        for x in amostras:
            for y in amostras:
                self.assertEqual(gf_mul(x, y), gf_mul(y, x))

    def test_mix_column_exemplo5_fips197(self):
        coluna = [0xD4, 0xBF, 0x5D, 0x30]
        resultado = mix_column(coluna)
        self.assertEqual(resultado, [0x04, 0x66, 0x81, 0xE5])

    def test_validacao_erros_fora_da_faixa(self):
        with self.assertRaises(ValueError):
            xtime(0x100)
        with self.assertRaises(ValueError):
            xtime(-1)
        with self.assertRaises(ValueError):
            gf_mul(0x57, 0x100)


if __name__ == "__main__":
    unittest.main()
