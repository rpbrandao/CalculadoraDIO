# 🔢 Calculadora Python

Calculadora científica de linha de comando e interface web interativa.

## Funcionalidades

| Operação | Exemplo |
|----------|---------|
| Aritméticas básicas | `2 + 3 * (4 - 1)` |
| Potência | `2**10` ou `2^10` |
| Divisão inteira / módulo | `17 // 3` · `17 % 3` |
| Raiz quadrada / cúbica | `sqrt(144)` · `cbrt(27)` |
| Logaritmos | `log(e)` · `log2(8)` · `log10(1000)` |
| Trigonometria | `sin(pi/2)` · `cos(pi)` · `tan(pi/4)` |
| Fatorial | `fatorial(10)` |
| Constantes | `pi` · `e` · `tau` · `inf` |
| Histórico | comando `historico` |

## Como usar

```bash
# Modo interativo
python calculadora.py

# Expressão direta
python calculadora.py "sqrt(2) * pi"

# Ajuda
python calculadora.py --ajuda
```

## Testes

```bash
pip install pytest
pytest tests/ -v
```
