import unittest
import secrets

try:
    from .sha256_vs_hmac import sha256, criar_hmac, verificar_hmac, simular_cenario
except (ImportError, ValueError):
    from sha256_vs_hmac import sha256, criar_hmac, verificar_hmac, simular_cenario


class TestAtividade01(unittest.TestCase):
    def test_sha256_comprimento_e_determinismo(self):
        msg = b"teste_criptografia"
        h1 = sha256(msg)
        h2 = sha256(msg)
        self.assertEqual(len(h1), 32)
        self.assertEqual(h1, h2)

    def test_sha256_recalculo_por_atacante(self):
        original = b"destino=ana;valor=100"
        alterada = b"destino=ana;valor=900"
        hash_original = sha256(original)
        hash_alterada = sha256(alterada)
        self.assertNotEqual(hash_original, hash_alterada)
        self.assertEqual(hash_alterada, sha256(alterada))

    def test_hmac_legitimo_aceito(self):
        chave = secrets.token_bytes(32)
        msg = b"destino=ana;valor=100"
        tag = criar_hmac(chave, msg)
        self.assertEqual(len(tag), 32)
        self.assertTrue(verificar_hmac(chave, msg, tag))

    def test_hmac_rejeita_mensagem_adulterada(self):
        chave = secrets.token_bytes(32)
        original = b"destino=ana;valor=100"
        alterada = b"destino=ana;valor=900"
        tag = criar_hmac(chave, original)
        self.assertFalse(verificar_hmac(chave, alterada, tag))

    def test_hmac_rejeita_chave_adulterada(self):
        chave_legitima = secrets.token_bytes(32)
        chave_atacante = secrets.token_bytes(32)
        msg = b"destino=ana;valor=900"
        tag_atacante = criar_hmac(chave_atacante, msg)
        self.assertFalse(verificar_hmac(chave_legitima, msg, tag_atacante))

    def test_simular_cenario_completo(self):
        res = simular_cenario()
        self.assertTrue(res["hmac_legitimo_aceito"])
        self.assertFalse(res["hmac_atacante_aceito"])


if __name__ == "__main__":
    unittest.main()
