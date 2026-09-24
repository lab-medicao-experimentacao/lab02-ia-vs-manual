#!/usr/bin/env python3
"""Identificação e tratamento de outliers antes dos testes estatísticos — Issue #64.

O Passo 4 da sprint exige revisar os dados e identificar outliers antes de aplicar os
testes. Este script aplica a **regra de Tukey (1.5×IQR)** por métrica × tratamento —
mesma regra da estatística descritiva (scripts/descriptive_stats.py, Issue #31) e coerente
com o protocolo (doc/protocolo-estatistico.md §5) — sobre os trials individuais das três
questões de pesquisa.

Métricas e elegibilidade (idênticas ao protocolo §3-§4):
  - RQ1 (tempo):    time_to_green_seconds — apenas trials `completed`.
  - RQ2 (defeitos): failed — trials com avaliação final válida (total > 0).
  - RQ3 (estrutura): complexity_avg, duplication_percent, loc_total — trials com métricas.

Política de tratamento (protocolo §5, decisoes.md §7): **nenhum outlier é descartado
automaticamente**. Este script apenas os sinaliza para inspeção; a decisão de manter ou
excluir é registrada aqui e justificada, mantendo os testes reproduzíveis.

Saída:
  - results/outliers.csv  (uma linha por outlier identificado)
  - tabela no stdout com as cercas por métrica × tratamento e a recomendação.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from dataset import DEFAULT_CSV, ROOT, load

TREATMENTS = ["sem-ia", "com-ia"]
# (rótulo RQ, coluna, rótulo legível, regra de elegibilidade)
METRICS = [
    ("RQ1", "time_to_green_seconds", "Tempo até verde (s)", "completed_only"),
    ("RQ2", "failed", "Testes falhando (nº)", "valid_tests"),
    ("RQ3a", "complexity_avg", "Complexidade ciclomática média/método", "has_metrics"),
    ("RQ3b", "duplication_percent", "Duplicação de linhas (%)", "has_metrics"),
    ("RQ3c", "loc_total", "LOC (controle)", "has_metrics"),
]


def eligible(df, rule):
    if rule == "completed_only":
        return df[df["status"] == "completed"]
    if rule == "valid_tests":
        return df[df["total"].notna() & (df["total"] > 0)]
    if rule == "has_metrics":
        return df[df["has_metrics"]]
    raise ValueError(f"Regra desconhecida: {rule}")


def tukey_fences(values):
    """Q1, Q3, IQR e cercas de Tukey (1.5×IQR)."""
    q1 = float(np.nanpercentile(values, 25))
    q3 = float(np.nanpercentile(values, 75))
    iqr = q3 - q1
    return q1, q3, iqr, q1 - 1.5 * iqr, q3 + 1.5 * iqr


def fmt(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "—"
    if float(value).is_integer():
        return f"{int(value)}"
    return f"{value:.2f}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--output", type=Path, default=ROOT / "results/outliers.csv")
    args = parser.parse_args()

    df = load(args.csv)

    print("=" * 78)
    print("IDENTIFICAÇÃO DE OUTLIERS (regra de Tukey, 1.5×IQR) — Issue #64")
    print("=" * 78)
    print(
        f"{len(df)} trials | por métrica × tratamento | "
        "sem descarte automático (protocolo §5)"
    )

    fence_rows = []
    outlier_rows = []
    for rq, column, label, rule in METRICS:
        base = eligible(df, rule)
        print()
        print(f"[{rq}] {label}")
        print(
            f"  {'tratamento':<10}{'n':>3}{'Q1':>10}{'Q3':>10}"
            f"{'IQR':>10}{'cerca inf.':>12}{'cerca sup.':>12}{'outliers':>10}"
        )
        for treatment in TREATMENTS:
            group = base[base["treatment"] == treatment]
            series = pd.to_numeric(group[column], errors="coerce").dropna()
            n = int(series.size)
            if n == 0:
                print(f"  {treatment:<10}{0:>3}{'—':>10}{'—':>10}{'—':>10}{'—':>12}{'—':>12}{0:>10}")
                continue
            values = series.to_numpy(dtype=float)
            q1, q3, iqr, lower, upper = tukey_fences(values)
            mask = (values < lower) | (values > upper)
            fence_rows.append(
                {
                    "rq": rq, "metric": label, "column": column, "treatment": treatment,
                    "n": n, "q1": q1, "q3": q3, "iqr": iqr,
                    "lower_fence": lower, "upper_fence": upper, "n_outliers": int(mask.sum()),
                }
            )
            print(
                f"  {treatment:<10}{n:>3}{fmt(q1):>10}{fmt(q3):>10}{fmt(iqr):>10}"
                f"{fmt(lower):>12}{fmt(upper):>12}{int(mask.sum()):>10}"
            )
            for idx, is_out in zip(series.index, mask):
                if is_out:
                    row = group.loc[idx]
                    outlier_rows.append(
                        {
                            "rq": rq, "metric": label, "column": column,
                            "treatment": treatment, "participant": row["participant"],
                            "kata": row["kata"], "trial_id": row["trial_id"],
                            "value": float(series.loc[idx]),
                            "lower_fence": lower, "upper_fence": upper,
                        }
                    )

    print()
    if outlier_rows:
        print(f"OUTLIERS IDENTIFICADOS ({len(outlier_rows)}):")
        for o in outlier_rows:
            side = "acima" if o["value"] > o["upper_fence"] else "abaixo"
            print(
                f"  [{o['rq']}] {o['metric']} · {o['treatment']}: "
                f"{o['participant']}/{o['kata']} = {fmt(o['value'])} "
                f"({side} da cerca [{fmt(o['lower_fence'])}, {fmt(o['upper_fence'])}])"
            )
    else:
        print("Nenhum outlier identificado pela regra de Tukey.")

    print()
    print("Tratamento adotado: manter todos os trials (sem descarte automático,")
    print("protocolo §5 / decisoes.md §7). Os outliers acima são inspecionados na")
    print("leitura dos resultados; qualquer exclusão futura deve ser justificada aqui.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        outlier_rows,
        columns=[
            "rq", "metric", "column", "treatment", "participant", "kata",
            "trial_id", "value", "lower_fence", "upper_fence",
        ],
    ).to_csv(args.output, index=False)
    print()
    print(f"Tabela salva em: {args.output}")


if __name__ == "__main__":
    main()
