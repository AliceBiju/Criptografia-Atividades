import unittest
import secrets
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

try:
    from .x25519_hkdf_mitm import derivar_chave, executar_acordo_legitimo, simular_ataque_intermediario_mallory
except (ImportError, ValueError):
    from x25519_hkdf_mitm import derivar_chave, executar_acordo_legitimo, simular_ataque_intermediario_mallory


class TestAtividade10(unittest.TestCase):
    def test_acordo_legitimo_completo(self):
        res = executar_acordo_legitimo()
        self.assertEqual(len(res["sa"]), 32)
        self.assertEqual(len(res["chave_derivada"]), 32)
        self.assertEqual(res["mensagem_recuperada"], b"nota=8.5")

    def test_exportacao_publica_32_bytes(self):
        priv = X25519PrivateKey.generate()
        pub = priv.public_key()
        pub_bytes = pub.public_bytes(Encoding.Raw, PublicFormat.Raw)
        self.assertEqual(len(pub_bytes), 32)

    def test_contexto_hkdf_diferente_produz_chaves_distintas(self):
        segredo = secrets.token_bytes(32)
        sal = secrets.token_bytes(16)
        chave_alice_bob = derivar_chave(segredo, sal, b"direcao-alice-para-bob")
        chave_bob_alice = derivar_chave(segredo, sal, b"direcao-bob-para-alice")
        self.assertNotEqual(chave_alice_bob, chave_bob_alice)

    def test_adulteracao_no_pacote_gera_invalid_tag(self):
        res = executar_acordo_legitimo()
        chave = res["chave_derivada"]
        nonce = res["nonce"]
        aad = res["aad"]
        pacote_corrompido = bytearray(res["pacote"])
        pacote_corrompido[0] ^= 1
        with self.assertRaises(InvalidTag):
            AESGCM(chave).decrypt(nonce, bytes(pacote_corrompido), aad)

    def test_simulacao_mallory_mitm(self):
        res = simular_ataque_intermediario_mallory()
        self.assertTrue(res["alice_mallory_chave_igual"])
        self.assertTrue(res["bob_mallory_chave_igual"])
        self.assertTrue(res["chaves_conexao_diferentes"])
        self.assertEqual(res["mensagem_espionada"], b"nota=8.5")


if __name__ == "__main__":
    unittest.main()
