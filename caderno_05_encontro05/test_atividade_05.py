import unittest

try:
    from .feistel_reversivel import (
        f,
        rodada,
        rodada_inversa,
        cifrar,
        decifrar,
        distancia_hamming,
        medir_avalanche
    )
except (ImportError, ValueError):
    from feistel_reversivel import (
        f,
        rodada,
        rodada_inversa,
        cifrar,
        decifrar,
        distancia_hamming,
        medir_avalanche
    )


class TestAtividade05(unittest.TestCase):
    def setUp(self):
        self.chaves = [3, 17, 91, 201]

    def test_ida_e_volta_blocos_do_enunciado(self):
        for bloco in [0x0000, 0x1234, 0xFFFF]:
            cifrado = cifrar(bloco, self.chaves)
            self.assertEqual(decifrar(cifrado, self.chaves), bloco)

    def test_saida_permanece_em_16_bits(self):
        for b in [0x0001, 0x8000, 0xAAAA, 0x5555]:
            c = cifrar(b, self.chaves)
            self.assertTrue(0 <= c <= 0xFFFF)

    def test_decifracao_falha_se_ordem_chaves_nao_invertida(self):
        bloco = 0x1234
        cifrado = cifrar(bloco, self.chaves)
        esquerda = (cifrado >> 8) & 0xFF
        direita = cifrado & 0xFF
        for k in self.chaves:
            esquerda, direita = rodada_inversa(esquerda, direita, k)
        resultado_incorreto = (esquerda << 8) | direita
        self.assertNotEqual(resultado_incorreto, bloco)

    def test_validacao_limite_bloco(self):
        with self.assertRaises(ValueError):
            cifrar(0x10000, self.chaves)
        with self.assertRaises(ValueError):
            cifrar(-1, self.chaves)

    def test_distancia_hamming(self):
        self.assertEqual(distancia_hamming(0b1010, 0b1001), 2)
        self.assertEqual(distancia_hamming(0x0000, 0xFFFF), 16)

    def test_efeito_avalanche_executa(self):
        c1, c2, pct = medir_avalanche(0x1234, self.chaves, bit_a_inverter=1)
        self.assertTrue(0 <= pct <= 100)


if __name__ == "__main__":
    unittest.main()
