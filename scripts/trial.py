#!/usr/bin/env python3
"""Cronometragem de trials. Apenas biblioteca padrão; execução Linux/Docker."""
import argparse
import csv
import json
import os
from pathlib import Path
import re
import select
import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def utc():
    return datetime.now(timezone.utc).isoformat()


def save(path, data):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    temporary.replace(path)


def report(directory):
    files = sorted(directory.glob("TEST-*.xml"))
    if not files:
        return None
    totals = dict(total=0, failures=0, errors=0, skipped=0)
    for file in files:
        suite = ET.parse(file).getroot()
        for key, attr in [
            ("total", "tests"),
            ("failures", "failures"),
            ("errors", "errors"),
            ("skipped", "skipped"),
        ]:
            totals[key] += int(suite.get(attr, "0"))
    totals["passed"] = totals["total"] - sum(
        totals[k] for k in ("failures", "errors", "skipped")
    )
    totals["failed"] = totals["failures"] + totals["errors"]
    if totals["passed"] < 0:
        raise ValueError("Contagens inválidas no relatório JUnit")
    totals["success_percent"] = (
        100 * totals["passed"] / totals["total"] if totals["total"] else None
    )
    return totals


def green(code, counts):
    return (
        code == 0
        and counts is not None
        and counts["total"] > 0
        and counts["passed"] == counts["total"]
    )


def snapshot(module, destination):
    destination.mkdir(parents=True)
    shutil.copy2(ROOT / "pom.xml", destination / "pom.xml")
    shutil.copytree(
        module,
        destination / "katas" / module.name,
        ignore=shutil.ignore_patterns("target", "__pycache__"),
    )
    return destination / "katas" / module.name


def launch(module):
    log = (module.parent.parent / "maven.log").open("w")
    try:
        proc = subprocess.Popen(
            ["mvn", "-o", "-B", "-ntp", "-f", str(module / "pom.xml"), "clean", "test"],
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    except BaseException:
        log.close()
        raise
    return proc, log


def stop(proc):
    if proc and proc.poll() is None:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.wait()


def summarize(module, code):
    try:
        counts = report(module / "target/surefire-reports")
        return {
            "exit_code": code,
            "tests": counts,
            "classification": (
                "success"
                if green(code, counts)
                else (
                    "tests_failed"
                    if counts and counts["failed"]
                    else "build_or_execution_error"
                )
            ),
        }
    except (ET.ParseError, ValueError) as exc:
        return {
            "exit_code": code,
            "tests": None,
            "classification": "invalid_report",
            "detail": str(exc),
        }


def run(args):
    module = ROOT / "katas" / args.kata
    if not (module / "src/test/java").exists() or not list(
        (module / "src/test/java").rglob("*.java")
    ):
        raise ValueError(
            "Kata sem testes de aceitação: prepare o módulo antes de iniciar."
        )
    if not sys.stdin.isatty() and not args.auto_test:
        raise ValueError(
            "Use terminal interativo ou --auto-test para validação automatizada."
        )
    statement = (module / "README.md").read_text()
    if args.seconds != 2100 and not args.practice:
        raise ValueError(
            "Trials oficiais exigem 2100 segundos; use --practice para validações curtas."
        )
    trial_id = (
        args.id
        or f"{args.participant}_{args.kata}_{args.treatment}_{datetime.now(timezone.utc):%Y%m%dT%H%M%S%fZ}"
    )
    if not re.fullmatch(r"[A-Za-z0-9_-]+", trial_id):
        raise ValueError("Identificador deve conter somente letras, números, _ e -.")
    out = args.output.resolve() / trial_id
    out.mkdir(parents=True, exist_ok=False)
    environment = ROOT / "results" / f"environment-{args.kata}.json"
    if environment.exists():
        shutil.copy2(environment, out / "environment.json")
    path = out / "trial.json"
    data = dict(
        schema_version=1,
        trial_id=trial_id,
        participant=args.participant,
        kata=args.kata,
        treatment=args.treatment,
        practice=args.practice,
        limit_seconds=args.seconds,
        status="running",
        started_at=utc(),
        ended_at=None,
        elapsed_seconds=None,
        censored=False,
        time_to_green_seconds=None,
        runs=[],
        final_evaluation=None,
        incident=None,
    )
    start = time.monotonic()
    deadline = start + args.seconds
    save(path, data)
    print(statement, flush=True)
    print(
        "Cronômetro iniciado. ENTER: testar; incidente MOTIVO: encerrar por falha técnica.",
        flush=True,
    )
    proc = log = current = winning = None
    request = args.auto_test

    def interrupted(signum, frame):
        raise KeyboardInterrupt

    old_signal = signal.signal(signal.SIGTERM, interrupted)
    try:
        while True:
            now = time.monotonic()
            if now >= deadline:
                data.update(
                    status="censored", censored=True, elapsed_seconds=args.seconds
                )
                break
            if proc and proc.poll() is not None:
                elapsed = time.monotonic() - start
                log.close()
                result = summarize(current, proc.returncode)
                result.update(
                    elapsed_seconds=elapsed, snapshot=str(current.relative_to(out))
                )
                data["runs"].append(result)
                proc = log = None
                save(path, data)
                print(json.dumps(result, ensure_ascii=False), flush=True)
                if (
                    green(result["exit_code"], result["tests"])
                    and elapsed < args.seconds
                ):
                    winning = current.parent.parent
                    data.update(
                        status="completed",
                        elapsed_seconds=elapsed,
                        time_to_green_seconds=elapsed,
                    )
                    break
            if request and proc is None:
                current = snapshot(module, out / "runs" / f'{len(data["runs"])+1:03}')
                proc, log = launch(current)
                request = False
            if (
                not args.auto_test
                and select.select(
                    [sys.stdin], [], [], min(0.1, max(0, deadline - time.monotonic()))
                )[0]
            ):
                line = sys.stdin.readline()
                if not line:
                    raise RuntimeError("Terminal de controle fechado")
                command = line.strip()
                if command.startswith("incidente "):
                    raise RuntimeError(command.removeprefix("incidente ").strip())
                if not command and proc is None:
                    request = True
                elif not command:
                    print("Testes já em execução; o relógio continua.", flush=True)
            else:
                time.sleep(0.05)
    except (KeyboardInterrupt, Exception) as exc:
        data.update(
            status="interrupted",
            incident=str(exc) or "Interrupção pelo operador",
            elapsed_seconds=min(time.monotonic() - start, args.seconds),
        )
    finally:
        data["ended_at"] = utc()
        save(path, data)
        stop(proc)
        if log:
            log.close()
        signal.signal(signal.SIGTERM, old_signal)

    # Não volta a medir: avaliação final usa somente a cópia preservada.
    final = out / "final"
    if winning:
        shutil.copytree(winning, final)
        data["final_evaluation"] = data["runs"][-1]
    else:
        frozen = snapshot(module, final)
        save(path, data)
        print(
            "Trial encerrado. Código preservado; avaliando a cópia final.", flush=True
        )
        final_proc = final_log = None
        try:
            final_proc, final_log = launch(frozen)
            code = final_proc.wait(timeout=120)
            data["final_evaluation"] = summarize(frozen, code)
        except subprocess.TimeoutExpired:
            data["final_evaluation"] = {
                "classification": "evaluation_timeout",
                "tests": None,
            }
        except (KeyboardInterrupt, OSError) as exc:
            data["final_evaluation"] = {
                "classification": "evaluation_error",
                "tests": None,
                "detail": str(exc),
            }
        finally:
            stop(final_proc)
            if final_log:
                final_log.close()
    if args.treatment == "com-ia":
        (out / "perguntas.md").write_text(
            "# Resumo das perguntas ao Claude\n\nPreencher após o trial. Registrar também modelo e esforço exibidos na interface.\n"
        )
    save(path, data)
    print(f'Registro: {path}\nEstado: {data["status"]}', flush=True)
    return 0


def export(args):
    rows = []
    for path in sorted(args.input.glob("*/trial.json")):
        data = json.loads(path.read_text())
        if data.get("practice") and not args.include_practice:
            continue
        row = {
            k: data.get(k)
            for k in (
                "trial_id",
                "participant",
                "kata",
                "treatment",
                "practice",
                "status",
                "limit_seconds",
                "elapsed_seconds",
                "time_to_green_seconds",
                "censored",
                "incident",
            )
        }
        counts = (data.get("final_evaluation") or {}).get("tests") or {}
        row.update(
            {
                k: counts.get(k)
                for k in ("total", "passed", "failed", "skipped", "success_percent")
            }
        )
        rows.append(row)
    if not rows:
        raise ValueError("Nenhum registro elegível para exportação.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} registros exportados para {args.output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    run_parser = sub.add_parser("start", help="Iniciar trial com limite contínuo")
    run_parser.add_argument("--participant", required=True)
    run_parser.add_argument(
        "--kata",
        choices=["kata-01", "kata-02", "kata-03", "kata-04", "smoke"],
        required=True,
    )
    run_parser.add_argument("--treatment", choices=["com-ia", "sem-ia"], required=True)
    run_parser.add_argument("--id")
    run_parser.add_argument("--output", type=Path, default=ROOT / "results")
    run_parser.add_argument("--seconds", type=float, default=2100)
    run_parser.add_argument("--practice", action="store_true")
    run_parser.add_argument(
        "--auto-test", action="store_true", help="Executar testes uma vez ao iniciar"
    )
    run_parser.set_defaults(func=run)
    export_parser = sub.add_parser("export", help="Consolidar JSONs em CSV")
    export_parser.add_argument("--input", type=Path, default=ROOT / "results")
    export_parser.add_argument(
        "--output", type=Path, default=ROOT / "results/consolidado.csv"
    )
    export_parser.add_argument("--include-practice", action="store_true")
    export_parser.set_defaults(func=export)
    args = parser.parse_args()
    if args.command == "start":
        if not 0 < args.seconds <= 2100:
            parser.error("--seconds deve estar entre 0 e 2100.")
        if args.kata == "smoke" and not args.practice:
            parser.error("O módulo smoke exige --practice.")
    try:
        return args.func(args)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Erro: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
