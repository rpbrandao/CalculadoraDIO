"""Testes unitários para a calculadora."""

import math
import pytest
from calculadora import avaliar, formatar_resultado, CalculadoraError


# ── Operações básicas ─────────────────────────────────────────────────────────

class TestOperacoesBasicas:

    def test_soma(self):              assert avaliar("2 + 3") == 5
    def test_subtracao(self):         assert avaliar("10 - 4") == 6
    def test_multiplicacao(self):     assert avaliar("3 * 7") == 21
    def test_divisao(self):           assert avaliar("10 / 4") == 2.5
    def test_divisao_inteira(self):   assert avaliar("17 // 3") == 5
    def test_modulo(self):            assert avaliar("17 % 3") == 2
    def test_potencia(self):          assert avaliar("2 ** 10") == 1024
    def test_potencia_circunflexo(self): assert avaliar("2^8") == 256
    def test_parenteses(self):        assert avaliar("(2 + 3) * 4") == 20
    def test_expressao_complexa(self):
        assert avaliar("2 + 3 * 4 - 1") == 13


# ── Funções matemáticas ───────────────────────────────────────────────────────

class TestFuncoes:

    def test_sqrt(self):        assert avaliar("sqrt(144)") == 12
    def test_abs_negativo(self): assert avaliar("abs(-42)") == 42
    def test_log_e(self):       assert avaliar("log(e)") == pytest.approx(1.0)
    def test_log10(self):       assert avaliar("log10(1000)") == pytest.approx(3.0)
    def test_log2(self):        assert avaliar("log2(8)") == pytest.approx(3.0)
    def test_sin_pi_2(self):    assert avaliar("sin(pi/2)") == pytest.approx(1.0)
    def test_cos_pi(self):      assert avaliar("cos(pi)") == pytest.approx(-1.0)
    def test_fatorial(self):    assert avaliar("fatorial(10)") == 3628800
    def test_ceil(self):        assert avaliar("ceil(4.1)") == 5
    def test_floor(self):       assert avaliar("floor(4.9)") == 4


# ── Constantes ────────────────────────────────────────────────────────────────

class TestConstantes:

    def test_pi(self):   assert avaliar("pi") == pytest.approx(math.pi)
    def test_e(self):    assert avaliar("e")  == pytest.approx(math.e)
    def test_tau(self):  assert avaliar("tau") == pytest.approx(math.tau)


# ── Erros esperados ───────────────────────────────────────────────────────────

class TestErros:

    def test_divisao_por_zero(self):
        with pytest.raises(CalculadoraError, match="zero"):
            avaliar("10 / 0")

    def test_sqrt_negativo(self):
        with pytest.raises(CalculadoraError):
            avaliar("sqrt(-1)")

    def test_expressao_vazia(self):
        with pytest.raises(CalculadoraError, match="vazia"):
            avaliar("")

    def test_sintaxe_invalida(self):
        with pytest.raises(CalculadoraError):
            avaliar("2 +* 3")


# ── Formatação ────────────────────────────────────────────────────────────────

class TestFormatacao:

    def test_inteiro(self):       assert formatar_resultado(1000) == "1.000"
    def test_float(self):         assert "3,14159" in formatar_resultado(math.pi).replace(".", ",")
    def test_resultado_inteiro_de_float(self): assert formatar_resultado(4.0) == "4"
