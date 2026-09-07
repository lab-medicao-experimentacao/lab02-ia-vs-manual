import json
from pathlib import Path
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import metrics  # noqa: E402  (precisa do sys.path acima)

PMD_XML = """<?xml version="1.0" encoding="UTF-8"?>
<pmd xmlns="http://pmd.sourceforge.net/report/2.0.0" version="7.17.0" timestamp="t">
<file name="Foo.java">
<violation beginline="1" endline="1" begincolumn="1" endcolumn="1" rule="CyclomaticComplexity" ruleset="Design" class="Foo" method="bar()" priority="3">
The method 'bar()' has a cyclomatic complexity of 3.
</violation>
<violation beginline="5" endline="5" begincolumn="1" endcolumn="1" rule="CyclomaticComplexity" ruleset="Design" class="Foo" method="baz()" priority="3">
The method 'baz()' has a cyclomatic complexity of 7.
</violation>
<violation beginline="1" endline="1" begincolumn="1" endcolumn="1" rule="CyclomaticComplexity" ruleset="Design" class="Foo" priority="3">
The class 'Foo' has a total cyclomatic complexity of 10 (highest 7).
</violation>
</file>
</pmd>
"""

EMPTY_PMD_XML = (
    '<?xml version="1.0"?>'
    '<pmd xmlns="http://pmd.sourceforge.net/report/2.0.0" version="7.17.0" timestamp="t"></pmd>'
)

EMPTY_CPD_XML = (
    '<?xml version="1.0"?>'
    '<pmd-cpd xmlns="https://pmd-code.org/schema/cpd-report" pmdVersion="7.17.0" '
    'timestamp="t" version="1.0.0"></pmd-cpd>'
)

CPD_XML_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<pmd-cpd xmlns="https://pmd-code.org/schema/cpd-report" pmdVersion="7.17.0" timestamp="t" version="1.0.0">
<file path="{path}" totalNumberOfTokens="10"/>
<duplication lines="3" tokens="30">
<file line="1" endline="3" path="{path}"/>
</duplication>
</pmd-cpd>
"""


def fake_run(report_content, returncode=4):
    def _run(argv, **kwargs):
        report = Path(argv[argv.index("-r") + 1])
        report.write_text(report_content)
        return SimpleNamespace(returncode=returncode)

    return _run


class StripCommentsTests(unittest.TestCase):
    def test_removes_line_comment(self):
        source = "int a = 1; // comentário\nint b = 2;\n"
        self.assertEqual(metrics.code_line_numbers(source), {1, 2})

    def test_removes_block_comment_spanning_lines(self):
        source = "int a = 1;\n/* bloco\nde comentário */\nint b = 2;\n"
        self.assertEqual(metrics.code_line_numbers(source), {1, 4})

    def test_blank_and_whitespace_lines_not_counted(self):
        source = "int a = 1;\n\n   \nint b = 2;\n"
        self.assertEqual(metrics.code_line_numbers(source), {1, 4})

    def test_comment_markers_inside_strings_are_not_comments(self):
        source = 'String s = "// not a comment";\n'
        self.assertEqual(metrics.code_line_numbers(source), {1})


class ComplexityTests(unittest.TestCase):
    def test_parses_method_level_violations_only(self):
        with patch("metrics.subprocess.run", side_effect=fake_run(PMD_XML)):
            result = metrics.complexity(Path("dummy"))
        self.assertEqual(result["per_method"], [3, 7])
        self.assertEqual(result["method_count"], 2)
        self.assertEqual(result["average"], 5.0)

    def test_average_is_none_without_methods(self):
        with patch("metrics.subprocess.run", side_effect=fake_run(EMPTY_PMD_XML, 0)):
            result = metrics.complexity(Path("dummy"))
        self.assertEqual(result["per_method"], [])
        self.assertIsNone(result["average"])

    def test_unexpected_exit_code_raises(self):
        with patch("metrics.subprocess.run", side_effect=fake_run(EMPTY_PMD_XML, 1)):
            with self.assertRaises(RuntimeError):
                metrics.complexity(Path("dummy"))


class DuplicationTests(unittest.TestCase):
    def test_collects_line_ranges_per_file(self):
        xml = CPD_XML_TEMPLATE.format(path="/workspace/Foo.java")
        with patch("metrics.subprocess.run", side_effect=fake_run(xml)):
            ranges = metrics.duplicated_line_ranges(Path("dummy"))
        self.assertEqual(ranges, {"/workspace/Foo.java": {1, 2, 3}})

    def test_no_duplication_gives_empty_ranges(self):
        with patch("metrics.subprocess.run", side_effect=fake_run(EMPTY_CPD_XML, 0)):
            ranges = metrics.duplicated_line_ranges(Path("dummy"))
        self.assertEqual(ranges, {})


class CollectTrialTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.trial_dir = self.root / "results/t1"
        source = self.trial_dir / "final/katas/kata-01/src/main/java"
        source.mkdir(parents=True)
        (source / "Solution.java").write_text("public class Solution {\n    int a = 1;\n}\n")
        (self.trial_dir / "trial.json").write_text(
            json.dumps({"trial_id": "t1", "kata": "kata-01"})
        )

    def run_tools(self, argv, **kwargs):
        report = Path(argv[argv.index("-r") + 1])
        content = EMPTY_PMD_XML if argv[1] == "check" else EMPTY_CPD_XML
        report.write_text(content)
        return SimpleNamespace(returncode=0)

    def test_collect_writes_metrics_json(self):
        with patch("metrics.subprocess.run", side_effect=self.run_tools):
            output, written = metrics.collect_trial(self.trial_dir)
        self.assertTrue(written)
        data = json.loads(output.read_text())
        self.assertEqual(data["kata"], "kata-01")
        self.assertEqual(data["trial_id"], "t1")
        self.assertEqual(data["loc"]["total"], 3)
        self.assertIsNone(data["complexity"]["average"])
        self.assertEqual(data["duplication"]["duplicated_loc"], 0)
        self.assertEqual(data["duplication"]["percent"], 0.0)

    def test_does_not_overwrite_without_force(self):
        (self.trial_dir / "metrics.json").write_text("{}")
        output, written = metrics.collect_trial(self.trial_dir)
        self.assertFalse(written)
        self.assertEqual(output.read_text(), "{}")

    def test_force_recomputes(self):
        (self.trial_dir / "metrics.json").write_text("{}")
        with patch("metrics.subprocess.run", side_effect=self.run_tools):
            output, written = metrics.collect_trial(self.trial_dir, force=True)
        self.assertTrue(written)
        self.assertNotEqual(output.read_text(), "{}")


class CollectEdgeCaseTests(unittest.TestCase):
    def test_zero_loc_gives_none_percent(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "src/main/java"
            source.mkdir(parents=True)
            (source / "OnlyComments.java").write_text("// nada além de comentário\n")

            def run(argv, **kwargs):
                report = Path(argv[argv.index("-r") + 1])
                report.write_text(EMPTY_PMD_XML if argv[1] == "check" else EMPTY_CPD_XML)
                return SimpleNamespace(returncode=0)

            with patch("metrics.subprocess.run", side_effect=run):
                result = metrics.collect(source)
        self.assertEqual(result["loc"]["total"], 0)
        self.assertIsNone(result["duplication"]["percent"])


class ResolveSourceTests(unittest.TestCase):
    def test_missing_final_code_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            trial_dir = Path(tmp)
            trial_dir.mkdir(exist_ok=True)
            (trial_dir / "trial.json").write_text(
                json.dumps({"trial_id": "x", "kata": "kata-02"})
            )
            with self.assertRaises(ValueError):
                metrics.resolve_source(trial_dir)

    def test_no_java_files_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "src/main/java"
            source.mkdir(parents=True)
            with self.assertRaises(ValueError):
                metrics.collect(source)


if __name__ == "__main__":
    unittest.main()
