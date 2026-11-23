import unittest
import secrets

try:
    from .fluxo_twotimepad import xor_bytes, demonstrar_two_time_pad, demonstrar_maleabilidade
except (ImportError, ValueError):
    from fluxo_twotimepad import xor_bytes, demonstrar_two_time_pad, demonstrar_maleabilidade


class TestAtividade04(unittest.TestCase):
    def test_xor_bytes_basico(self):
        a = b"\xaa\xbb"
        b = b"\x55\x44"
        self.assertEqual(xor_bytes(a, b), b"\xff\xff")

    def test_xor_bytes_multiplos_argumentos(self):
        a = b"\x01\x02"
        b = b"\x03\x04"
        c = b"\x05\x06"
        self.assertEqual(xor_bytes(a, b, c), b"\x07\x00")

    def test_xor_bytes_comprimentos_diferentes_lanca_excecao(self):
        with self.assertRaises(ValueError):
            xor_bytes(b"curto", b"comprido_demais")

    def test_two_time_pad_recuperacao(self):
        res = demonstrar_two_time_pad()
        self.assertEqual(res["recuperada"], b"pagar=9000")

    def test_independencia_do_fluxo_no_two_time_pad(self):
        m1 = b"mensagem_1"
        m2 = b"mensagem_2"
        for _ in range(3):
            fluxo = secrets.token_bytes(len(m1))
            c1 = xor_bytes(m1, fluxo)
            c2 = xor_bytes(m2, fluxo)
            self.assertEqual(xor_bytes(c1, c2), xor_bytes(m1, m2))
            self.assertEqual(xor_bytes(c1, c2, m1), m2)

    def test_fluxos_independentes_protegem_mensagens(self):
        m1 = b"mensagem_1"
        m2 = b"mensagem_2"
        s1 = secrets.token_bytes(len(m1))
        s2 = secrets.token_bytes(len(m2))
        c1 = xor_bytes(m1, s1)
        c2 = xor_bytes(m2, s2)
        self.assertNotEqual(xor_bytes(c1, c2), xor_bytes(m1, m2))

    def test_maleabilidade_xor(self):
        m = b"usuario_comum"
        fluxo = secrets.token_bytes(len(m))
        cifra = xor_bytes(m, fluxo)
        recuperado = demonstrar_maleabilidade(cifra, fluxo, posicao_byte=0, bit=0)
        bit_original = m[0] & 1
        bit_novo = recuperado[0] & 1
        self.assertEqual(bit_novo, bit_original ^ 1)
        self.assertEqual(recuperado[1:], m[1:])


if __name__ == "__main__":
    unittest.main()
