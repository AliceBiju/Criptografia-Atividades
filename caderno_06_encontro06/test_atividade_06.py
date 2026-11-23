import unittest

try:
    from .estimador_forca_bruta import tempo_medio, em_anos, em_horas, CENARIOS
except (ImportError, ValueError):
    from estimador_forca_bruta import tempo_medio, em_anos, em_horas, CENARIOS


class TestAtividade06(unittest.TestCase):
    def test_contrato_inicial_tempo_medio_des56(self):
        self.assertEqual(tempo_medio(56, 1e12), (2 ** 55) / 1e12)

    def test_tempo_des_aproximadamente_10_horas(self):
        segundos = tempo_medio(56, 1e12, maquinas=1)
        horas = em_horas(segundos)
        self.assertAlmostEqual(horas, 10.0, delta=0.1)

    def test_dobrar_maquinas_divide_tempo_por_dois(self):
        t1 = tempo_medio(56, 1e12, maquinas=1)
        t2 = tempo_medio(56, 1e12, maquinas=2)
        self.assertAlmostEqual(t2, t1 / 2, places=7)

    def test_adicionar_um_bit_dobra_o_tempo(self):
        t56 = tempo_medio(56, 1e12)
        t57 = tempo_medio(57, 1e12)
        self.assertAlmostEqual(t57, t56 * 2, places=7)

    def test_razao_entre_aes128_e_des56_eh_2_elevado_a_72(self):
        t_aes = tempo_medio(128, 1e12)
        t_des = tempo_medio(56, 1e12)
        self.assertEqual(t_aes / t_des, 2 ** 72)

    def test_validacao_entradas_invalidas(self):
        with self.assertRaises(ValueError):
            tempo_medio(0, 1e12)
        with self.assertRaises(ValueError):
            tempo_medio(56, 0)
        with self.assertRaises(ValueError):
            tempo_medio(56, 1e12, maquinas=0)


if __name__ == "__main__":
    unittest.main()
