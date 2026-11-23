import unittest

try:
    from .cesar_frequencia import (
        cesar,
        decifrar,
        candidatas,
        ordenar_candidatas,
        cifrar_composta,
        decifrar_composta
    )
except (ImportError, ValueError):
    from cesar_frequencia import (
        cesar,
        decifrar,
        candidatas,
        ordenar_candidatas,
        cifrar_composta,
        decifrar_composta
    )


class TestAtividade03(unittest.TestCase):
    def test_cifra_e_decifra_cesar(self):
        original = "ATAQUE AO AMANHECER"
        chave = 7
        cifrado = cesar(original, chave)
        self.assertEqual(decifrar(cifrado, chave), original)

    def test_preservacao_de_espacos_e_pontuacao(self):
        texto = "OLA, MUNDO! 123"
        cifrado = cesar(texto, 5)
        self.assertIn(",", cifrado)
        self.assertIn("!", cifrado)
        self.assertIn(" ", cifrado)
        self.assertIn("123", cifrado)
        self.assertEqual(decifrar(cifrado, 5), texto)

    def test_quantidade_de_candidatas(self):
        cifrado = cesar("MENSAGEM SECRETA", 10)
        possibilidades = candidatas(cifrado)
        self.assertEqual(len(possibilidades), 26)

    def test_ataque_por_pontuacao_identifica_chave_correta(self):
        texto_original = "ATAQUE AO AMANHECER"
        chave = 7
        cifrado = cesar(texto_original, chave)
        ranking = ordenar_candidatas(cifrado)
        melhor_candidata = ranking[0]
        self.assertEqual(melhor_candidata[0], chave)
        self.assertEqual(melhor_candidata[1], texto_original)

    def test_desafio_cifra_composta(self):
        palavras = ["CRIPTOGRAFIA", "SEGURANCA", "REDES", "EXERCICIO"]
        for p in palavras:
            cifrada = cifrar_composta(p, 4)
            decifrada = decifrar_composta(cifrada, 4)
            self.assertEqual(decifrada, p)


if __name__ == "__main__":
    unittest.main()
