from estimador_forca_bruta import (
    tempo_medio,
    em_anos,
    em_horas,
    CENARIOS,
    gerar_tabela_comparativa
)

if __name__ == "__main__":
    print("=== Caderno 06: Atividade 11 executada com sucesso ===")
    t = tempo_medio(56, 1e12)
    print(f"DES tempo médio (56 bits, 10^12/s): {t:.2f} s ({em_horas(t):.2f} h)")
