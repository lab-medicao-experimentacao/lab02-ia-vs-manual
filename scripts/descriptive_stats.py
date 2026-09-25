#!/usr/bin/env python3
"""Estatística descritiva (mediana e IQR) por tratamento — Issue #31.

Calcula mediana e IQR por tratamento para as métricas das três questões de pesquisa,
identificando trials censurados e outliers, conforme o protocolo analítico em
doc/decisoes.md §7 (mediana e IQR por tratamento; censura contada à parte; não tratar
os 18 trials como 18 participantes independentes).

Métricas por RQ:
  - RQ1 (tempo):    time_to_green_seconds — apenas trials `completed` (censurados são
                    contados separadamente, nunca como tempo de conclusão).
  - RQ2 (defeitos): número absoluto de testes falhando ao final (`failed`), sobre todos
                    os trials com avaliação final válida.
  - RQ3 (estrutura): complexidade ciclomática média/método, % de duplicação e LOC,
                    lidos dos metrics.json de cada trial.

Entradas:
  - results/consolidado.csv  (gerado por scripts/trial.py export)
  - results/<trial_id>/metrics.json  (gerado por scripts/metrics.py)

Saídas:
  - results/descritiva.csv   (uma linha por métrica × tratamento)
  - tabela legível no stdout, com lacunas de dados e outliers explicitados.

Dependências: pandas, numpy (disponíveis na imagem Docker do laboratório).
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

# Rótulo legível, coluna de origem e regra de elegibilidade de cada métrica.
METRICS = [
    ("RQ1", "time_to_green_seconds", "Tempo até verde (s)", "completed_only"),
    ("RQ2", "failed", "Testes falhando (nº)", "valid_tests"),
    ("RQ3", "complexity_avg", "Complexidade ciclomática média/método", "has_metrics"),
    ("RQ3", "duplication_percent", "Duplicação de linhas (%)", "has_metrics"),
    ("RQ3", "loc_total", "LOC (código do participante)", "has_metrics"),
]


def load_metrics(results_dir):
    """Lê os metrics.json de cada trial e devolve um DataFrame por trial_id."""
    rows = []
    for path in sorted(results_dir.glob("*/metrics.json")):
        data = json.loads(path.read_text())
        complexity = data.get("complexity") or {}
        duplication = data.get("duplication") or {}
        loc = data.get("loc") or {}
        rows.append(
            {
                "trial_id": data.get("trial_id") or path.parent.name,
                "complexity_avg": complexity.get("average"),
                "duplication_percent": duplication.get("percent"),
                "loc_total": loc.get("total"),
            }
        )
    return pd.DataFrame(rows)


def eligible(df, rule):
    """Filtra o DataFrame conforme a regra de elegibilidade da métrica."""
    if rule == "completed_only":
        return df[df["status"] == "completed"]
    if rule == "valid_tests":
        return df[df["total"].notna() & (df["total"] > 0)]
    if rule == "has_metrics":
        return df
    raise ValueError(f"Regra desconhecida: {rule}")


def iqr_outliers(values):
    """Q1, Q3, IQR e as cercas de Tukey (1.5×IQR); devolve máscara de outliers."""
    q1 = np.nanpercentile(values, 25)
    q3 = np.nanpercentile(values, 75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    mask = (values < lower) | (values > upper)
    return q1, q3, iqr, lower, upper, mask


def summarize(df, metrics_df):
    # O consolidado.csv já traz as métricas estruturais (Issue #36); mantém só as dos
    # metrics.json para o merge não gerar colunas duplicadas (_x/_y).
    overlap = [c for c in metrics_df.columns if c != "trial_id" and c in df.columns]
    merged = df.drop(columns=overlap).merge(metrics_df, on="trial_id", how="left")
    treatments = ["sem-ia", "com-ia"]
    summary_rows = []
    outlier_notes = []
    coverage_notes = []

    for rq, column, label, rule in METRICS:
        base = eligible(merged, rule)
        for treatment in treatments:
            group = base[base["treatment"] == treatment]
            series = pd.to_numeric(group[column], errors="coerce").dropna()
            n = int(series.size)
            row = {
                "rq": rq,
                "metric": label,
                "column": column,
                "treatment": treatment,
                "n": n,
                "median": np.nan,
                "q1": np.nan,
                "q3": np.nan,
                "iqr": np.nan,
                "min": np.nan,
                "max": np.nan,
                "n_outliers": 0,
            }
            if n:
                values = series.to_numpy(dtype=float)
                q1, q3, iqr, lower, upper, mask = iqr_outliers(values)
                row.update(
                    median=float(np.median(values)),
                    q1=float(q1),
                    q3=float(q3),
                    iqr=float(iqr),
                    min=float(values.min()),
                    max=float(values.max()),
                    n_outliers=int(mask.sum()),
                )
                if mask.any():
                    ids = group.loc[series.index[mask], "trial_id"].tolist()
                    for tid, val in zip(ids, values[mask]):
                        outlier_notes.append(
                            f"  [{rq}] {label} · {treatment}: {tid} = {val:g} "
                            f"(fora de [{lower:g}, {upper:g}])"
                        )
            summary_rows.append(row)

        # Cobertura: quantos trials contribuíram vs. o total daquele tratamento.
        for treatment in treatments:
            total_t = int((merged["treatment"] == treatment).sum())
            used_t = int(
                pd.to_numeric(
                    base[base["treatment"] == treatment][column], errors="coerce"
                )
                .notna()
                .sum()
            )
            if used_t < total_t:
                coverage_notes.append(
                    f"  [{rq}] {label} · {treatment}: {used_t}/{total_t} trials com dado"
                )

    return pd.DataFrame(summary_rows), outlier_notes, coverage_notes


def censoring_report(df):
    lines = []
    for treatment in ["sem-ia", "com-ia"]:
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


def fmt(value):
    if pd.isna(value):
        return "—"
    if float(value).is_integer():
        return f"{int(value)}"
    return f"{value:.2f}"


def print_table(summary):
    header = ["RQ", "Métrica", "Tratamento", "n", "Mediana", "Q1", "Q3", "IQR", "Outliers"]
    widths = [4, 38, 10, 3, 9, 9, 9, 9, 8]
    line = "  ".join(h.ljust(w) for h, w in zip(header, widths))
    print(line)
    print("-" * len(line))
    for _, r in summary.iterrows():
        cells = [
            r["rq"],
            r["metric"][:38],
            r["treatment"],
            str(int(r["n"])),
            fmt(r["median"]),
            fmt(r["q1"]),
            fmt(r["q3"]),
            fmt(r["iqr"]),
            str(int(r["n_outliers"])),
        ]
        print("  ".join(c.ljust(w) for c, w in zip(cells, widths)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=ROOT / "results/consolidado.csv")
    parser.add_argument("--results", type=Path, default=ROOT / "results")
    parser.add_argument("--output", type=Path, default=ROOT / "results/descritiva.csv")
    args = parser.parse_args()

    if not args.csv.exists():
        parser.exit(
            1,
            f"Erro: {args.csv} não existe. Rode antes: "
            f"python scripts/trial.py export\n",
        )

    df = pd.read_csv(args.csv)
    metrics_df = load_metrics(args.results)
    summary, outlier_notes, coverage_notes = summarize(df, metrics_df)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.output, index=False)

    print("=" * 78)
    print("ESTATÍSTICA DESCRITIVA POR TRATAMENTO — mediana e IQR (Issue #31)")
    print("=" * 78)
    print(f"Fonte: {args.csv}  |  {len(df)} trials  |  metrics.json: {len(metrics_df)} trials")
    print()
    print("Censura por tratamento (contada à parte, não como tempo de conclusão):")
    for l in censoring_report(df):
        print(l)
    print()
    print_table(summary)
    print()
    if outlier_notes:
        print("Outliers (regra de Tukey, 1.5×IQR):")
        for l in outlier_notes:
            print(l)
    else:
        print("Outliers (1.5×IQR): nenhum identificado.")
    print()
    if coverage_notes:
        print("Lacunas de cobertura (dado ausente para parte dos trials):")
        for l in coverage_notes:
            print(l)
    else:
        print("Cobertura: todas as métricas disponíveis para todos os trials.")
    print()
    print(f"Tabela salva em: {args.output}")


if __name__ == "__main__":
    main()
