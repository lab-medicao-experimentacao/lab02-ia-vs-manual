#!/usr/bin/env python3
"""Análise estrutural RQ3 (complexidade, duplicação, LOC) — Issue #33.

Compara as métricas estruturais entre tratamentos conforme doc/protocolo-estatistico.md:
  - agrega os 3 trials de cada participante × tratamento pela mediana (§2);
  - aplica Wilcoxon pareado bilateral (hipótese não direcional, α = 0,05) sobre os
    pares por participante (§6), descartando pares com diferença zero (zero_method
    "wilcox") e reportando quantos foram descartados;
  - reporta a mediana das diferenças (com-ia − sem-ia) e o rank-biserial pareado
    como tamanho de efeito;
  - complementa com a leitura por kata (mediana de cada tratamento em cada kata).

Censurados entram normalmente (§3); interrupted/running são excluídos.

Saídas:
  - results/rq3.csv         (uma linha por métrica: teste e resumo)
  - results/rq3_pares.csv   (pares por participante × métrica)
  - tabelas no stdout
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.stats import rankdata, wilcoxon

from dataset import DEFAULT_CSV, ROOT, load

ALPHA = 0.05
TREATMENTS = ["sem-ia", "com-ia"]
METRICS = [
    ("RQ3a", "complexity_avg", "Complexidade ciclomática média/método"),
    ("RQ3b", "duplication_percent", "Duplicação de linhas (%)"),
    ("RQ3c", "loc_total", "LOC (controle)"),
]


def eligible(df):
    """Trials válidos para RQ3: com métricas e sem ocorrência técnica."""
    return df[df["has_metrics"] & df["status"].isin(["completed", "censored"])]


def participant_pairs(df, column):
    """Mediana por participante × tratamento, em formato largo (um par por linha)."""
    wide = (
        df.groupby(["participant", "treatment"], observed=True)[column]
        .agg(["median", "count"])
        .unstack("treatment")
    )
    pairs = pd.DataFrame(
        {
            "sem_ia": wide[("median", "sem-ia")],
            "com_ia": wide[("median", "com-ia")],
            "n_sem_ia": wide[("count", "sem-ia")],
            "n_com_ia": wide[("count", "com-ia")],
        }
    ).dropna(subset=["sem_ia", "com_ia"])
    pairs["diff"] = pairs["com_ia"] - pairs["sem_ia"]
    return pairs.reset_index()


def rank_biserial(diffs):
    """Rank-biserial pareado: (W+ − W−) / (W+ + W−), sobre diferenças não nulas."""
    ranks = rankdata(np.abs(diffs))
    total = ranks.sum()
    return float((ranks[diffs > 0].sum() - ranks[diffs < 0].sum()) / total)


def test_metric(pairs):
    diffs = pairs["diff"].to_numpy(dtype=float)
    nonzero = diffs[diffs != 0]
    result = {
        "n_pairs": int(diffs.size),
        "n_zero_diffs": int(diffs.size - nonzero.size),
        "n_effective": int(nonzero.size),
        "median_diff": float(np.median(diffs)) if diffs.size else np.nan,
        "statistic": np.nan,
        "p_value": np.nan,
        "rank_biserial": np.nan,
        "note": "",
    }
    if nonzero.size == 0:
        result["note"] = "todas as diferenças são zero: teste não aplicável"
        return result
    test = wilcoxon(nonzero, alternative="two-sided", method="exact")
    result.update(
        statistic=float(test.statistic),
        p_value=float(test.pvalue),
        rank_biserial=rank_biserial(nonzero),
        note="significativo" if test.pvalue < ALPHA else "não significativo",
    )
    return result


def by_kata(df):
    """Mediana de cada métrica por kata × tratamento (leitura complementar)."""
    columns = [c for _, c, _ in METRICS]
    table = df.groupby(["kata", "treatment"], observed=True)[columns].median().unstack("treatment")
    table.columns = [f"{col}_{t}" for col, t in table.columns]
    return table


def fmt(value):
    if pd.isna(value):
        return "—"
    if float(value).is_integer():
        return f"{int(value)}"
    return f"{value:.2f}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--output", type=Path, default=ROOT / "results/rq3.csv")
    parser.add_argument("--pairs", type=Path, default=ROOT / "results/rq3_pares.csv")
    args = parser.parse_args()

    df = load(args.csv)
    data = eligible(df)
    excluded = len(df) - len(data)

    print("=" * 78)
    print("RQ3 — ESTRUTURA DO CÓDIGO: com-ia vs. sem-ia (Issue #33)")
    print("=" * 78)
    print(
        f"{len(data)} trials elegíveis de {len(df)} (excluídos: {excluded}) | "
        f"Wilcoxon pareado bilateral, α = {ALPHA} | scipy {scipy.__version__}"
    )

    summary_rows, pair_rows = [], []
    for rq, column, label in METRICS:
        pairs = participant_pairs(data, column)
        result = test_metric(pairs)
        summary_rows.append({"rq": rq, "metric": label, "column": column, **result})
        for _, p in pairs.iterrows():
            pair_rows.append({"rq": rq, "column": column, **p.to_dict()})

        print()
        print(f"[{rq}] {label}")
        print(f"  {'participante':<16}{'sem-ia':>10}{'com-ia':>10}{'dif.':>10}")
        for _, p in pairs.iterrows():
            print(
                f"  {p['participant']:<16}{fmt(p['sem_ia']):>10}"
                f"{fmt(p['com_ia']):>10}{fmt(p['diff']):>10}"
            )
        print(
            f"  pares: {result['n_pairs']} (diferença zero descartados: "
            f"{result['n_zero_diffs']}) | mediana das dif.: {fmt(result['median_diff'])} | "
            f"W = {fmt(result['statistic'])} | p = {fmt(result['p_value'])} | "
            f"r_rb = {fmt(result['rank_biserial'])} | {result['note']}"
        )

    print()
    print("Mediana por kata × tratamento:")
    print(by_kata(data).to_string(float_format=lambda v: f"{v:.2f}"))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(summary_rows).to_csv(args.output, index=False)
    pd.DataFrame(pair_rows).to_csv(args.pairs, index=False)
    print()
    print(f"Tabelas salvas em: {args.output} e {args.pairs}")


if __name__ == "__main__":
    main()
