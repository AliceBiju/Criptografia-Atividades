#!/usr/bin/env python3
"""Script de orquestração para executar todos os testes dos 12 Cadernos de Criptografia."""

import unittest
import sys
import time
from pathlib import Path


def main():
    root_dir = Path(__file__).resolve().parent
    cadernos = sorted([d for d in root_dir.iterdir() if d.is_dir() and d.name.startswith("caderno_")])

    print("=" * 75)
    print(" Execução Global de Testes Automatizados — 12 Cadernos de Criptografia")
    print("=" * 75)

    total_testes = 0
    total_erros = 0
    total_falhas = 0
    t0_global = time.perf_counter()
    relatorio = []

    for c in cadernos:
        loader = unittest.TestLoader()
        suite = loader.discover(start_dir=str(c), pattern="test_*.py")
        
        runner = unittest.TextTestRunner(verbosity=0, stream=open("nul" if sys.platform == "win32" else "/dev/null", "w"))
        t0_caderno = time.perf_counter()
        result = runner.run(suite)
        dt = time.perf_counter() - t0_caderno

        qtd = result.testsRun
        erros = len(result.errors)
        falhas = len(result.failures)
        ok = (erros == 0 and falhas == 0)

        total_testes += qtd
        total_erros += erros
        total_falhas += falhas

        relatorio.append({
            "pasta": c.name,
            "qtd": qtd,
            "ok": ok,
            "dt": dt
        })

    # Imprime tabela de resumo
    print(f"{'Caderno':<28} | {'Testes':<8} | {'Status':<12} | {'Tempo'}")
    print("-" * 75)
    for r in relatorio:
        status_str = "✅ PASSOU" if r["ok"] else "❌ FALHOU"
        print(f"{r['pasta']:<28} | {r['qtd']:<8} | {status_str:<12} | {r['dt']*1000:6.1f} ms")

    dt_global = time.perf_counter() - t0_global
    print("=" * 75)
    print(f"Total de testes executados: {total_testes}")
    print(f"Total de falhas           : {total_falhas}")
    print(f"Total de erros            : {total_erros}")
    print(f"Tempo total de execução   : {dt_global:.3f} s")
    print("=" * 75)

    if total_erros > 0 or total_falhas > 0:
        print("\n❌ Alguns testes falharam!")
        sys.exit(1)
    else:
        print("\n🎉 Todos os testes de todos os cadernos passaram com 100% de sucesso!")
        sys.exit(0)


if __name__ == "__main__":
    main()
