"""Validação com Maven real; execute no Docker após preparar o módulo smoke."""

import json
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import trial

with tempfile.TemporaryDirectory() as temp:
    original = trial.ROOT
    trial.ROOT = Path(temp)
    shutil.copy2(original / "pom.xml", trial.ROOT / "pom.xml")
    shutil.copytree(
        original / "katas/smoke",
        trial.ROOT / "katas/smoke",
        ignore=shutil.ignore_patterns("target"),
    )
    for name, seconds, expected in [
        ("timeout", 1, "censored"),
        ("success", 30, "completed"),
    ]:
        if name == "success":
            source = trial.ROOT / "katas/smoke/src/main/java/Sum.java"
            source.write_text(source.read_text().replace("return 0;", "return a + b;"))
        args = SimpleNamespace(
            kata="smoke",
            participant="integration",
            treatment="sem-ia",
            id=name,
            output=trial.ROOT / "results",
            seconds=seconds,
            practice=True,
            auto_test=True,
        )
        trial.run(args)
        data = json.loads((args.output / name / "trial.json").read_text())
        assert data["status"] == expected, data
        assert data["final_evaluation"]["tests"]["total"] == 3, data
        assert data["final_evaluation"]["tests"]["passed"] == (
            3 if name == "success" else 1
        ), data
        assert (data["time_to_green_seconds"] is None) == (name == "timeout"), data
    print("Integração Maven/JUnit: censura e sucesso validados em cópias temporárias.")
