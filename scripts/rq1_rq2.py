#!/usr/bin/env python3
"""Teste de Wilcoxon pareado para RQ1 (tempo) e RQ2 (defeitos) — Issue #32.

Compara os tratamentos conforme doc/protocolo-estatistico.md:
  - agrega os 3 trials de cada participante × tratamento pela mediana (§2);
  - aplica Wilcoxon pareado **unilateral** (hipóteses direcionais, α = 0,05) sobre os
    pares por participante (§6), pois H1 é que a IA **reduz** tempo (RQ1) e defeitos (RQ2);
  - a diferença é (com-ia − sem-ia); `alternative="less"` testa se essa diferença é
    negativa, isto é, se com-ia < sem-ia (IA reduz);
  - descarta pares com diferença zero (método "wilcox") e reporta quantos;
  - reporta mediana das diferenças e rank-biserial pareado como tamanho de efeito;
  - complementa com a leitura por kata.

Tratamento de censura (§3): RQ1 usa apenas trials `completed` (censurados não têm tempo
de conclusão e são contados à parte); RQ2 usa trials com avaliação final válida, mesmo
censurados. interrupted/running são excluídos.

Saídas:
  - results/rq1_rq2.csv        (uma linha por RQ: teste e resumo)
  - results/rq1_rq2_pares.csv  (pares por participante × RQ)
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
# (rótulo RQ, coluna, rótulo legível, regra de elegibilidade)
METRICS = [
    ("RQ1", "time_to_green_seconds", "Tempo até verde (s)", "completed_only"),
    ("RQ2", "failed", "Testes falhando (nº)", "valid_tests"),
]


def eligible(df, rule):
    """Filtra trials válidos para a métrica (protocolo §3)."""
    base = df[df["status"].isin(["completed", "censored"])]
    if rule == "completed_only":
        return base[base["status"] == "completed"]
    if rule == "valid_tests":
        return base[base["total"].notna() & (base["total"] > 0)]
    raise ValueError(f"Regra desconhecida: {rule}")


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
    """Wilcoxon unilateral (alternative='less': com-ia < sem-ia = IA reduz)."""
    diffs = pairs["diff"].to_numpy(dtype=float)
    nonzero = diffs[diffs != 0]
    result = {
        "alternative": "less",
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
    test = wilcoxon(nonzero, alternative="less", method="exact")
    result.update(
        statistic=float(test.statistic),
        p_value=float(test.pvalue),
        rank_biserial=rank_biserial(nonzero),
        note="significativo" if test.pvalue < ALPHA else "não significativo",
    )
    return result


def censoring_note(df):
    lines = []
    for treatment in TREATMENTS:
        group = df[df["treatment"] == treatment]
        total = len(group)
        completed = int((group["status"] == "completed").sum())
        censored = int(group["censored"].fillna(False).astype(bool).sum())
        interrupted = int((group["status"] == "interrupted").sum())
        lines.append(
            f"  {treatment}: {total} trials | concluídos {completed} | "
            f"censurados {censored} | interrompidos {interrupted}"
        )
    return lines


def by_kata(df, column):
    """Mediana da métrica por kata × tratamento (leitura complementar)."""
    table = (
        df.groupby(["kata", "treatment"], observed=True)[column]
        .median()
        .unstack("treatment")
    )
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
    parser.add_argument("--output", type=Path, default=ROOT / "results/rq1_rq2.csv")
    parser.add_argument("--pairs", type=Path, default=ROOT / "results/rq1_rq2_pares.csv")
    args = parser.parse_args()

    df = load(args.csv)

    print("=" * 78)
    print("RQ1 (tempo) e RQ2 (defeitos): com-ia vs. sem-ia (Issue #32)")
    print("=" * 78)
    print(
        f"{len(df)} trials | Wilcoxon pareado unilateral (H1: IA reduz), "
        f"α = {ALPHA} | scipy {scipy.__version__}"
    )
    print()
    print("Censura por tratamento (RQ1 usa só concluídos; §3):")
    for line in censoring_note(df):
        print(line)

    summary_rows, pair_rows = [], []
    for rq, column, label, rule in METRICS:
        base = eligible(df, rule)
        pairs = participant_pairs(base, column)
        result = test_metric(pairs)
        summary_rows.append({"rq": rq, "metric": label, "column": column, **result})
        for _, p in pairs.iterrows():
            pair_rows.append({"rq": rq, "column": column, **p.to_dict()})

        print()
        print(f"[{rq}] {label}")
        print(f"  {'participante':<16}{'sem-ia':>12}{'com-ia':>12}{'dif.':>12}")
        for _, p in pairs.iterrows():
            print(
                f"  {p['participant']:<16}{fmt(p['sem_ia']):>12}"
                f"{fmt(p['com_ia']):>12}{fmt(p['diff']):>12}"
            )
        print(
            f"  pares: {result['n_pairs']} (dif. zero descartados: "
            f"{result['n_zero_diffs']}) | mediana das dif.: {fmt(result['median_diff'])} | "
            f"W = {fmt(result['statistic'])} | p = {fmt(result['p_value'])} | "
            f"r_rb = {fmt(result['rank_biserial'])} | {result['note']}"
        )
        print("  mediana por kata (sem-ia / com-ia):")
        kata_table = by_kata(base, column)
        for kata, row in kata_table.iterrows():
            print(f"    {kata}: {fmt(row.get('sem-ia'))} / {fmt(row.get('com-ia'))}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(summary_rows).to_csv(args.output, index=False)
    pd.DataFrame(pair_rows).to_csv(args.pairs, index=False)
    print()
    print(f"Tabelas salvas em: {args.output} e {args.pairs}")


if __name__ == "__main__":
    main()
