#!/usr/bin/env python3
"""Baixa dependências e valida a execução offline antes da cronometragem."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
from trial import ROOT, snapshot, summarize, utc

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--kata",
    choices=["smoke", "kata-01", "kata-02", "kata-03", "kata-04"],
    required=True,
)
args = parser.parse_args()
module = ROOT / "katas" / args.kata
if not list((module / "src/test/java").rglob("*.java")):
    parser.error("O módulo ainda não tem testes de aceitação.")
versions = {}
for name, command in [
    ("java", ["java", "-version"]),
    ("maven", ["mvn", "-version"]),
    ("python", ["python", "--version"]),
    ("pmd", ["pmd", "--version"]),
]:
    result = subprocess.run(
        command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True
    )
    versions[name] = result.stdout.strip()
with tempfile.TemporaryDirectory() as temp:
    frozen = snapshot(module, Path(temp) / "project")
    for offline in (False, True):
        command = ["mvn", "-B", "-ntp", "-f", str(frozen / "pom.xml"), "clean", "test"]
        if offline:
            command.insert(1, "-o")
        result = subprocess.run(command)
        evaluation = summarize(frozen, result.returncode)
        if evaluation["classification"] not in ("success", "tests_failed"):
            parser.exit(
                1,
                "Preparação falhou: corrija compilação, dependências ou execução dos testes.\n",
            )
versions.update(prepared_at=utc(), kata=args.kata, initial_tests=evaluation["tests"])
output = ROOT / "results" / f"environment-{args.kata}.json"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(versions, indent=2, ensure_ascii=False) + "\n")
print(f"Ambiente preparado e validado offline. Registro: {output}")
