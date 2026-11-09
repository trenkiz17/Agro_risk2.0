"""Execute: cd backend; python -m unittest discover -s tests -p test_analise_avancada.py"""
import unittest
from services.analise_avancada_service import validar_parametros


class AnaliseAvancadaValidacaoTests(unittest.TestCase):
    def test_tres_cenarios_ordenados(self):
        valores = validar_parametros({
            "produtividade_baixa_sc_ha": 20,
            "produtividade_media_sc_ha": 30,
            "produtividade_alta_sc_ha": 40,
            "area_util_percentual": 80,
        })
        self.assertEqual(30, valores["produtividade_media_sc_ha"])
        self.assertEqual(80, valores["area_util_percentual"])

    def test_ciclo_incompleto_bloqueado(self):
        with self.assertRaises(ValueError):
            validar_parametros({"ciclo_min_dias": 100})

    def test_ciclo_invertido_bloqueado(self):
        with self.assertRaises(ValueError):
            validar_parametros({"ciclo_min_dias": 150, "ciclo_max_dias": 100})

    def test_produtividade_incompleta_bloqueada(self):
        with self.assertRaises(ValueError):
            validar_parametros({"produtividade_baixa_sc_ha": 10})

    def test_campos_desconhecidos_bloqueados(self):
        with self.assertRaises(ValueError):
            validar_parametros({"usuario_id": 12})

    def test_injecao_textual_na_fonte_rejeita_tamanho(self):
        with self.assertRaises(ValueError):
            validar_parametros({"fonte_parametros": "a" * 351})


if __name__ == "__main__":
    unittest.main()
