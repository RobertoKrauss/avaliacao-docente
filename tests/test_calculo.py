import unittest

from app.services.calculo_pontuacao import Regra, calcular_pontuacao


class TestCalculoPontuacao(unittest.TestCase):
    def test_fixo(self):
        r = Regra(tipo_formula="fixo", valor_base=10)
        self.assertEqual(calcular_pontuacao(r), 10)

    def test_por_unidade(self):
        r = Regra(tipo_formula="por_unidade", valor_base=5)
        self.assertEqual(calcular_pontuacao(r, quantidade=3), 15)

    def test_por_hora(self):
        r = Regra(tipo_formula="por_hora", valor_base=5, divisor_unidade=10)
        self.assertEqual(calcular_pontuacao(r, carga_horaria=20), 10)

    def test_manual_requires_value(self):
        r = Regra(tipo_formula="manual")
        with self.assertRaises(ValueError):
            calcular_pontuacao(r)
        self.assertEqual(calcular_pontuacao(r, valor_manual=7), 7)

    def test_teto(self):
        r = Regra(tipo_formula="por_unidade", valor_base=10, pontuacao_maxima=15)
        self.assertEqual(calcular_pontuacao(r, quantidade=2), 15)


if __name__ == "__main__":
    unittest.main()
