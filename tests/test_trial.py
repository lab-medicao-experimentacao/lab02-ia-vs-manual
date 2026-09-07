import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

spec = importlib.util.spec_from_file_location(
    "trial", Path(__file__).resolve().parents[1] / "scripts/trial.py"
)
trial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trial)


class TrialTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.module = self.root / "katas/smoke"
        (self.module / "src/test/java").mkdir(parents=True)
        (self.module / "src/main/java").mkdir(parents=True)
        (self.module / "src/test/java/Test.java").write_text("// fixture")
        (self.module / "src/main/java/Main.java").write_text("// solution")
        (self.module / "README.md").write_text("Exercício provisório")
        (self.module / "pom.xml").write_text("<project/>")
        (self.root / "pom.xml").write_text("<project/>")
        binary = self.root / "bin"
        binary.mkdir()
        mvn = binary / "mvn"
        mvn.write_text(
            """#!/usr/bin/env python3
import os, sys, time
from pathlib import Path
module = Path(sys.argv[sys.argv.index('-f')+1]).parent
mode = os.environ.get('FAKE_MODE', 'success')
if mode == 'slow' and 'runs' in module.parts: time.sleep(10)
if mode == 'compile': sys.exit(1)
reports = module / 'target/surefire-reports'
reports.mkdir(parents=True)
failures = 1 if mode == 'fail' else 0
skipped = 1 if mode == 'skip' else 0
(reports/'TEST-example.xml').write_text(f'<testsuite tests="2" failures="{failures}" errors="0" skipped="{skipped}"/>')
sys.exit(1 if failures else 0)
"""
        )
        mvn.chmod(0o755)
        self.env = patch.dict(
            os.environ, {"PATH": str(binary) + os.pathsep + os.environ["PATH"]}
        )
        self.env.start()
        self.addCleanup(self.env.stop)
        self.root_patch = patch.object(trial, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def execute(self, mode="success", seconds=0.4):
        args = SimpleNamespace(
            kata="smoke",
            participant="A",
            treatment="sem-ia",
            id="test",
            output=self.root / "results",
            seconds=seconds,
            practice=True,
            auto_test=True,
        )
        with patch.dict(os.environ, {"FAKE_MODE": mode}), contextlib.redirect_stdout(
            io.StringIO()
        ):
            trial.run(args)
        return json.loads((args.output / "test/trial.json").read_text())

    def test_success_and_snapshot(self):
        data = self.execute(seconds=2)
        self.assertEqual(data["status"], "completed")
        self.assertFalse(data["censored"])
        self.assertEqual(data["final_evaluation"]["tests"]["passed"], 2)
        self.assertTrue(
            (
                self.root / "results/test/final/katas/smoke/src/main/java/Main.java"
            ).exists()
        )

    def test_failed_tests_censored_and_preserved(self):
        data = self.execute("fail")
        self.assertEqual(data["status"], "censored")
        self.assertEqual(data["elapsed_seconds"], 0.4)
        self.assertIsNone(data["time_to_green_seconds"])
        self.assertEqual(data["final_evaluation"]["tests"]["failed"], 1)

    def test_deadline_kills_running_tests_without_counting_late_green(self):
        data = self.execute("slow")
        self.assertEqual(data["status"], "censored")
        self.assertEqual(data["final_evaluation"]["tests"]["passed"], 2)
        self.assertIsNone(data["time_to_green_seconds"])

    def test_compilation_error_is_not_green_or_zero_failures(self):
        data = self.execute("compile")
        self.assertEqual(data["status"], "censored")
        self.assertIsNone(data["final_evaluation"]["tests"])
        self.assertEqual(
            data["final_evaluation"]["classification"], "build_or_execution_error"
        )

    def test_skipped_tests_do_not_mean_success(self):
        data = self.execute("skip")
        self.assertEqual(data["status"], "censored")

    def test_missing_executable_records_incident(self):
        with patch.object(
            trial, "launch", side_effect=FileNotFoundError("mvn ausente")
        ):
            data = self.execute()
        self.assertEqual(data["status"], "interrupted")
        self.assertIn("mvn ausente", data["incident"])

    def test_does_not_overwrite_attempt(self):
        self.execute()
        with self.assertRaises(FileExistsError):
            self.execute()

    def test_missing_reports_cannot_pass(self):
        self.assertIsNone(trial.report(self.root))
        self.assertFalse(trial.green(0, None))

    def test_export_excludes_practice_by_default(self):
        self.execute()
        args = SimpleNamespace(
            input=self.root / "results",
            output=self.root / "all.csv",
            include_practice=False,
        )
        with self.assertRaises(ValueError):
            trial.export(args)
        args.include_practice = True
        with contextlib.redirect_stdout(io.StringIO()):
            trial.export(args)
        self.assertIn("test,A,smoke", args.output.read_text())


if __name__ == "__main__":
    unittest.main()
