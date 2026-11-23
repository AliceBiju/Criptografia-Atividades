import unittest
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

try:
    from .registro_aead import ReceptorAEAD, montar_aad, montar_nonce, executar_atividade
except (ImportError, ValueError):
    from registro_aead import ReceptorAEAD, montar_aad, montar_nonce, executar_atividade


class TestAtividade09(unittest.TestCase):
    def setUp(self):
        self.chave = AESGCM.generate_key(bit_length=128)
        self.aes = AESGCM(self.chave)
        self.nonce = montar_nonce(7, 9)
        self.aad = montar_aad(1, 17, 9)
        self.msg = b"nota=8.5"
        self.pacote = self.aes.encrypt(self.nonce, self.msg, self.aad)

    def test_tamanho_e_recuperacao_correta(self):
        self.assertEqual(len(self.pacote), 24)
        recuperada = self.aes.decrypt(self.nonce, self.pacote, self.aad)
        self.assertEqual(recuperada, self.msg)

    def test_adulteracao_no_texto_cifrado_dispara_invalid_tag(self):
        mod = bytearray(self.pacote)
        mod[0] ^= 1
        with self.assertRaises(InvalidTag):
            self.aes.decrypt(self.nonce, bytes(mod), self.aad)

    def test_adulteracao_na_tag_dispara_invalid_tag(self):
        mod = bytearray(self.pacote)
        mod[-1] ^= 1
        with self.assertRaises(InvalidTag):
            self.aes.decrypt(self.nonce, bytes(mod), self.aad)

    def test_adulteracao_no_aad_dispara_invalid_tag(self):
        mod = bytearray(self.aad)
        mod[-1] ^= 1
        with self.assertRaises(InvalidTag):
            self.aes.decrypt(self.nonce, self.pacote, bytes(mod))

    def test_adulteracao_no_nonce_dispara_invalid_tag(self):
        mod = bytearray(self.nonce)
        mod[-1] ^= 1
        with self.assertRaises(InvalidTag):
            self.aes.decrypt(bytes(mod), self.pacote, self.aad)

    def test_chave_errada_dispara_invalid_tag(self):
        outra_chave = AESGCM.generate_key(bit_length=128)
        outro_aes = AESGCM(outra_chave)
        with self.assertRaises(InvalidTag):
            outro_aes.decrypt(self.nonce, self.pacote, self.aad)

    def test_politica_antirrepeticao(self):
        receptor = ReceptorAEAD(self.chave, usuario_esperado=17)
        self.assertEqual(receptor.processar_registro(self.nonce, self.pacote, self.aad), self.msg)
        with self.assertRaises(ValueError):
            receptor.processar_registro(self.nonce, self.pacote, self.aad)

    def test_politica_contexto_usuario(self):
        receptor_18 = ReceptorAEAD(self.chave, usuario_esperado=18)
        with self.assertRaises(PermissionError):
            receptor_18.processar_registro(self.nonce, self.pacote, self.aad)

    def test_executar_atividade_completa(self):
        res = executar_atividade()
        self.assertEqual(res["pacote_len"], 24)
        self.assertEqual(res["recuperada"], b"nota=8.5")


if __name__ == "__main__":
    unittest.main()
