"""
calculadora.py
~~~~~~~~~~~~~~
Calculadora científica de linha de comando.

Operações básicas : + - * /
Operações extras  : ** (potência), // (divisão inteira), % (módulo)
Funções           : sqrt, cbrt, abs, log, log2, log10, fatorial
Constantes        : pi, e, tau, inf

Uso:
    python calculadora.py              # modo interativo
    python calculadora.py "2 + 3 * 4"  # expressão direta
    python calculadora.py --ajuda
"""

from __future__ import annotations

import math
import operator
import re
import sys
from decimal import Decimal, InvalidOperation
from typing import Union

# ── Cores ANSI ────────────────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
DIM    = "\033[2m"
BLUE   = "\033[94m"

Number = Union[int, float]


# ── Motor de cálculo ──────────────────────────────────────────────────────────

class CalculadoraError(Exception):
    """Erro específico da calculadora com mensagem amigável."""


CONSTANTES: dict[str, float] = {
    "pi":  math.pi,
    "e":   math.e,
    "tau": math.tau,
    "inf": math.inf,
}

FUNCOES: dict[str, callable] = {
    "sqrt":     math.sqrt,
    "cbrt":     lambda x: math.copysign(abs(x) ** (1 / 3), x),
    "abs":      abs,
    "log":      math.log,
    "log2":     math.log2,
    "log10":    math.log10,
    "sin":      math.sin,
    "cos":      math.cos,
    "tan":      math.tan,
    "asin":     math.asin,
    "acos":     math.acos,
    "atan":     math.atan,
    "graus":    math.degrees,
    "rad":      math.radians,
    "fatorial": math.factorial,
    "ceil":     math.ceil,
    "floor":    math.floor,
    "round":    round,
}


def avaliar(expressao: str) -> Number:
    """Avalia uma expressão matemática de forma segura.

    Suporta operadores aritméticos padrão, funções matemáticas e constantes.
    Não usa `eval()` diretamente sobre strings não-tratadas.

    Args:
        expressao: String com a expressão, ex.: "2 + 3 * (4 - 1)"

    Returns:
        Resultado numérico (int ou float).

    Raises:
        CalculadoraError: Para divisão por zero, domínio inválido, sintaxe incorreta.
    """
    expressao = expressao.strip()
    if not expressao:
        raise CalculadoraError("Expressão vazia.")

    # Substituir constantes e normalizar
    expr = expressao.lower()
    for nome, valor in CONSTANTES.items():
        expr = re.sub(rf'\b{nome}\b', str(valor), expr)

    # Substituir funções por versões seguras
    namespace = {**FUNCOES, "__builtins__": {}}

    try:
        # Validação: apenas caracteres permitidos
        if re.search(r'[^0-9\s\+\-\*\/\(\)\.\,\^\%a-z\_]', expr):
            raise CalculadoraError(f"Caractere não permitido na expressão.")

        # Substituir ^ por ** (notação alternativa de potência)
        expr = expr.replace("^", "**")

        resultado = eval(expr, namespace)  # noqa: S307 — namespace restrito

        if isinstance(resultado, complex):
            raise CalculadoraError("O resultado é um número complexo (domínio inválido).")
        if math.isnan(resultado):
            raise CalculadoraError("O resultado é NaN (operação indefinida).")

        # Retornar int quando possível
        if isinstance(resultado, float) and resultado.is_integer():
            return int(resultado)
        return resultado

    except ZeroDivisionError:
        raise CalculadoraError("Divisão por zero não é permitida.")
    except ValueError as e:
        raise CalculadoraError(f"Domínio matemático inválido: {e}")
    except SyntaxError:
        raise CalculadoraError(f"Sintaxe inválida: '{expressao}'")
    except CalculadoraError:
        raise
    except Exception as e:
        raise CalculadoraError(f"Erro ao calcular: {e}")


def formatar_resultado(valor: Number) -> str:
    """Formata o número com separador de milhar e precisão adequada."""
    if isinstance(valor, int):
        return f"{valor:,}".replace(",", ".")
    # Float: até 10 casas, remove zeros à direita
    formatted = f"{valor:.10f}".rstrip("0").rstrip(".")
    # Separador de milhar na parte inteira
    partes = formatted.split(".")
    partes[0] = f"{int(partes[0]):,}".replace(",", "_")
    return ".".join(partes).replace("_", ".")


# ── Interface de linha de comando ─────────────────────────────────────────────

BANNER = f"""
{BOLD}{CYAN}
  ╔══════════════════════════════════════╗
  ║       C A L C U L A D O R A  🔢      ║
  ║         Python — modo terminal       ║
  ╚══════════════════════════════════════╝
{RESET}"""

AJUDA = f"""
{BOLD}Operadores:{RESET}
  {CYAN}+  -  *  /{RESET}          Adição, subtração, multiplicação, divisão
  {CYAN}**  ^{RESET}               Potência        ex: {DIM}2**10{RESET} ou {DIM}2^10{RESET}
  {CYAN}//{RESET}                  Divisão inteira ex: {DIM}17 // 3{RESET}
  {CYAN}%{RESET}                   Módulo          ex: {DIM}17 % 3{RESET}
  {CYAN}( ){RESET}                 Agrupamento     ex: {DIM}(2 + 3) * 4{RESET}

{BOLD}Funções:{RESET}
  {CYAN}sqrt(x){RESET}             Raiz quadrada
  {CYAN}cbrt(x){RESET}             Raiz cúbica
  {CYAN}abs(x){RESET}              Valor absoluto
  {CYAN}log(x){RESET}              Logaritmo natural
  {CYAN}log2(x)  log10(x){RESET}   Logaritmo base 2 / 10
  {CYAN}sin(x)   cos(x)   tan(x){RESET}   Trigonometria (em radianos)
  {CYAN}graus(x){RESET}            Converte rad → graus
  {CYAN}rad(x){RESET}              Converte graus → rad
  {CYAN}fatorial(n){RESET}         Fatorial
  {CYAN}ceil(x)  floor(x){RESET}   Teto / piso
  {CYAN}round(x, n){RESET}         Arredondamento com n casas

{BOLD}Constantes:{RESET}
  {CYAN}pi  e  tau  inf{RESET}

{BOLD}Comandos:{RESET}
  {CYAN}historico{RESET}           Mostra os últimos cálculos
  {CYAN}limpar{RESET}              Limpa o histórico
  {CYAN}ajuda{RESET}               Mostra esta tela
  {CYAN}sair  q  exit{RESET}       Encerra o programa

{BOLD}Exemplos:{RESET}
  {DIM}2 + 3 * (4 - 1){RESET}     → 11
  {DIM}sqrt(144){RESET}            → 12
  {DIM}2^10{RESET}                 → 1024
  {DIM}log(e){RESET}               → 1
  {DIM}sin(pi / 2){RESET}          → 1
  {DIM}fatorial(10){RESET}         → 3628800
"""


def exibir_historico(historico: list[tuple[str, str]]) -> None:
    if not historico:
        print(f"{YELLOW}  Histórico vazio.{RESET}")
        return
    print(f"\n{BOLD}  Histórico ({len(historico)} entrada(s)):{RESET}")
    for i, (expr, res) in enumerate(historico, 1):
        print(f"  {DIM}{i:>2}.{RESET}  {expr}  {DIM}={RESET}  {GREEN}{res}{RESET}")
    print()


def run_interativo() -> None:
    """Loop principal do modo interativo."""
    print(BANNER)
    print(f"  {DIM}Digite uma expressão ou 'ajuda' para ver os comandos.{RESET}\n")

    historico: list[tuple[str, str]] = []

    while True:
        try:
            entrada = input(f"{BOLD}{CYAN}  calc>{RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{GREEN}  Até logo! 👋{RESET}\n")
            break

        if not entrada:
            continue

        cmd = entrada.lower()

        if cmd in ("sair", "q", "exit", "quit"):
            print(f"\n{GREEN}  Até logo! 👋{RESET}\n")
            break

        if cmd == "ajuda":
            print(AJUDA)
            continue

        if cmd == "historico":
            exibir_historico(historico)
            continue

        if cmd == "limpar":
            historico.clear()
            print(f"{YELLOW}  Histórico limpo.{RESET}")
            continue

        try:
            resultado = avaliar(entrada)
            resultado_fmt = formatar_resultado(resultado)
            print(f"\n  {DIM}{entrada}{RESET}")
            print(f"  {BOLD}{GREEN}= {resultado_fmt}{RESET}\n")
            historico.append((entrada, resultado_fmt))
            # Manter apenas os últimos 20
            if len(historico) > 20:
                historico.pop(0)

        except CalculadoraError as e:
            print(f"\n  {RED}⚠  {e}{RESET}\n")


def run_expressao_direta(expressao: str) -> None:
    """Executa uma expressão passada via argumento CLI e imprime o resultado."""
    try:
        resultado = avaliar(expressao)
        print(formatar_resultado(resultado))
    except CalculadoraError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    args = sys.argv[1:]

    if not args:
        run_interativo()
        return

    if args[0] in ("--ajuda", "-h", "--help"):
        print(AJUDA)
        return

    # Expressão direta: python calculadora.py "2 + 3"
    expressao = " ".join(args)
    run_expressao_direta(expressao)


if __name__ == "__main__":
    main()
