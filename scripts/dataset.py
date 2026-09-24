#!/usr/bin/env python3
"""Carrega o CSV consolidado num DataFrame único para análise e dashboard.

O CSV de scripts/trial.py export já contém tempos, testes e métricas estruturais
(metrics.json) por trial. Este módulo converte tipos, descarta práticas e acrescenta
colunas derivadas. Valores ausentes permanecem NaN — nunca zero.

Uso em outro script:
    from dataset import load
    df = load()
"""
import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "results/consolidado.csv"

NUMERIC = [
    "limit_seconds",
    "elapsed_seconds",
    "time_to_green_seconds",
    "total",
    "passed",
    "failed",
    "skipped",
    "success_percent",
    "loc_total",
    "method_count",
    "complexity_avg",
    "duplicated_loc",
    "duplication_percent",
]
METRIC_COLUMNS = [
    "loc_total",
    "method_count",
    "complexity_avg",
    "duplicated_loc",
    "duplication_percent",
]
BOOLEAN = ["practice", "censored"]


def load(csv_path=DEFAULT_CSV):
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False, na_values=[""])
    missing = [c for c in METRIC_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"CSV sem colunas de métricas ({', '.join(missing)}): "
            "rode metrics.py collect-all e trial.py export novamente."
        )
    for column in NUMERIC:
        df[column] = pd.to_numeric(df[column])
    for column in BOOLEAN:
        df[column] = df[column] == "True"
    df = df[~df["practice"]].reset_index(drop=True)
    df["treatment"] = pd.Categorical(df["treatment"], categories=["sem-ia", "com-ia"])
    df["time_to_green_minutes"] = df["time_to_green_seconds"] / 60
    df["has_metrics"] = df[METRIC_COLUMNS].notna().all(axis=1)
    return df


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_CSV)
    args = parser.parse_args()
    df = load(args.input)
    print(f"{len(df)} trials | sem métricas: {(~df['has_metrics']).sum()}")
    print(df.groupby(["participant", "treatment"], observed=True).size().to_string())


if __name__ == "__main__":
    main()
