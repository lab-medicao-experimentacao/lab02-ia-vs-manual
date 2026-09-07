#!/usr/bin/env python3
"""Coleta de métricas estruturais (complexidade, duplicação, LOC) via PMD/CPD.

Opera sobre o código final preservado de um trial (final/katas/<kata>/src/main/java),
excluindo testes e infraestrutura. Consulte doc/metricas.md para a definição das
regras, limiares e cálculos usados.
"""
import argparse
import json
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from trial import ROOT, save, utc

PMD_NS = "{http://pmd.sourceforge.net/report/2.0.0}"
CPD_NS = "{https://pmd-code.org/schema/cpd-report}"

# Threshold do CPD: menor que o padrão da ferramenta (100) porque os katas têm
# soluções curtas (35 minutos); um limiar alto deixaria de detectar duplicação
# no nível de método. Ver doc/metricas.md.
MINIMUM_TOKENS = 50

COMPLEXITY_RULESET = """<?xml version="1.0" encoding="UTF-8"?>
<ruleset name="metrics-complexity" xmlns="http://pmd.sourceforge.net/ruleset/2.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://pmd.sourceforge.net/ruleset/2.0.0 https://pmd.sourceforge.io/ruleset_2_0_0.xsd">
  <description>Complexidade ciclomática por método, reportando todos os métodos</description>
  <rule ref="category/java/design.xml/CyclomaticComplexity">
    <properties>
      <property name="methodReportLevel" value="1"/>
    </properties>
  </rule>
</ruleset>
"""

COMPLEXITY_PATTERN = re.compile(r"cyclomatic complexity of (\d+)")


def _strip_comments(source):
    """Remove comentários preservando quebras de linha, para manter a numeração original."""
    result = []
    state = "code"
    i, n = 0, len(source)
    while i < n:
        c = source[i]
        nxt = source[i + 1] if i + 1 < n else ""
        if state == "code":
            if c == "/" and nxt == "/":
                state = "line_comment"
                i += 2
            elif c == "/" and nxt == "*":
                state = "block_comment"
                i += 2
            elif c in "\"'":
                state = "string" if c == '"' else "char"
                result.append(c)
                i += 1
            else:
                result.append(c)
                i += 1
        elif state == "line_comment":
            if c == "\n":
                state = "code"
                result.append(c)
            i += 1
        elif state == "block_comment":
            if c == "*" and nxt == "/":
                state = "code"
                i += 2
            else:
                if c == "\n":
                    result.append(c)
                i += 1
        else:  # string ou char
            result.append(c)
            if c == "\\" and i + 1 < n:
                result.append(source[i + 1])
                i += 2
                continue
            if (state == "string" and c == '"') or (state == "char" and c == "'"):
                state = "code"
            i += 1
    return "".join(result)


def code_line_numbers(source):
    """Linhas (1-indexadas) com conteúdo além de espaços e comentários."""
    stripped = _strip_comments(source)
    return {n for n, line in enumerate(stripped.splitlines(), start=1) if line.strip()}


def loc(java_files):
    """LOC por arquivo e total: linhas não vazias e não compostas só por comentário."""
    per_file = {}
    for file in java_files:
        per_file[file] = code_line_numbers(file.read_text())
    total = sum(len(lines) for lines in per_file.values())
    return total, per_file


def complexity(source_dir):
    """Complexidade ciclomática por método via PMD (regra CyclomaticComplexity)."""
    with tempfile.TemporaryDirectory() as temp:
        ruleset = Path(temp) / "complexity-ruleset.xml"
        ruleset.write_text(COMPLEXITY_RULESET)
        report = Path(temp) / "pmd.xml"
        result = subprocess.run(
            [
                "pmd", "check",
                "-d", str(source_dir),
                "-R", str(ruleset),
                "-f", "xml",
                "-r", str(report),
            ],
        )
        # 0: sem violações; 4: violações encontradas (não é falha de execução).
        if result.returncode not in (0, 4):
            raise RuntimeError(f"pmd check falhou com código {result.returncode}")
        root = ET.parse(report).getroot()
    values = []
    for violation in root.iter(f"{PMD_NS}violation"):
        if violation.get("method") is None:
            continue  # ignora o total agregado por classe
        match = COMPLEXITY_PATTERN.search(violation.text or "")
        if match:
            values.append(int(match.group(1)))
    return {
        "per_method": values,
        "method_count": len(values),
        "average": sum(values) / len(values) if values else None,
    }


def duplicated_line_ranges(source_dir, minimum_tokens=MINIMUM_TOKENS):
    """Linhas duplicadas por arquivo (união de todas as ocorrências reportadas pelo CPD)."""
    with tempfile.TemporaryDirectory() as temp:
        report = Path(temp) / "cpd.xml"
        result = subprocess.run(
            [
                "pmd", "cpd",
                "-d", str(source_dir),
                "-l", "java",
                "--minimum-tokens", str(minimum_tokens),
                "-f", "xml",
                "-r", str(report),
            ],
        )
        # 0: sem duplicação; 4: duplicação encontrada (não é falha de execução).
        if result.returncode not in (0, 4):
            raise RuntimeError(f"pmd cpd falhou com código {result.returncode}")
        root = ET.parse(report).getroot()
    ranges = {}
    for duplication in root.findall(f"{CPD_NS}duplication"):
        for file_elem in duplication.findall(f"{CPD_NS}file"):
            path = file_elem.get("path")
            start, end = int(file_elem.get("line")), int(file_elem.get("endline"))
            ranges.setdefault(path, set()).update(range(start, end + 1))
    return ranges


def collect(source_dir, minimum_tokens=MINIMUM_TOKENS):
    """Calcula LOC, complexidade ciclomática média e percentual de duplicação."""
    java_files = sorted(source_dir.rglob("*.java"))
    if not java_files:
        raise ValueError(f"Nenhum arquivo .java encontrado em {source_dir}")
    total_loc, per_file_lines = loc(java_files)
    duplicated_ranges = duplicated_line_ranges(source_dir, minimum_tokens)
    duplicated_loc = sum(
        len(lines & duplicated_ranges.get(str(file.resolve()), set()))
        for file, lines in per_file_lines.items()
    )
    return {
        "source": str(source_dir),
        "collected_at": utc(),
        "loc": {
            "total": total_loc,
            "per_file": {
                str(file.relative_to(source_dir)): len(lines)
                for file, lines in per_file_lines.items()
            },
        },
        "complexity": complexity(source_dir),
        "duplication": {
            "minimum_tokens": minimum_tokens,
            "duplicated_loc": duplicated_loc,
            "percent": 100 * duplicated_loc / total_loc if total_loc else None,
        },
    }


def resolve_source(trial_dir):
    trial_data = json.loads((trial_dir / "trial.json").read_text())
    source = trial_dir / "final" / "katas" / trial_data["kata"] / "src/main/java"
    if not source.exists():
        raise ValueError(f"Código final não encontrado em {source}")
    return source, trial_data


def collect_trial(trial_dir, force=False):
    output = trial_dir / "metrics.json"
    if output.exists() and not force:
        return output, False
    source, trial_data = resolve_source(trial_dir)
    metrics = collect(source)
    metrics.update(trial_id=trial_data["trial_id"], kata=trial_data["kata"])
    save(output, metrics)
    return output, True


def find_trials(results_dir):
    return (path.parent for path in sorted(results_dir.glob("*/trial.json")))


def collect_one(args):
    output, written = collect_trial(Path(args.trial).resolve(), force=args.force)
    print(f"{'Gravado' if written else 'Já existia (use --force)'}: {output}")
    return 0


def collect_all(args):
    processed = 0
    for trial_dir in find_trials(args.input):
        try:
            output, written = collect_trial(trial_dir, force=args.force)
        except ValueError as exc:
            print(f"Ignorado {trial_dir.name}: {exc}")
            continue
        if written:
            processed += 1
            print(f"Gravado: {output}")
    print(f"{processed} trial(s) processado(s).")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    single = sub.add_parser("collect", help="Coletar métricas de um trial")
    single.add_argument("--trial", required=True, help="Pasta do trial (results/<trial_id>)")
    single.add_argument("--force", action="store_true")
    single.set_defaults(func=collect_one)

    batch = sub.add_parser(
        "collect-all", help="Coletar métricas de todos os trials com código final preservado"
    )
    batch.add_argument("--input", type=Path, default=ROOT / "results")
    batch.add_argument("--force", action="store_true")
    batch.set_defaults(func=collect_all)

    args = parser.parse_args()
    try:
        return args.func(args)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Erro: {exc}\n")


if __name__ == "__main__":
    import sys
    sys.exit(main())
