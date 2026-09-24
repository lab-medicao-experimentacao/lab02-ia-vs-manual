import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("dashboard", SCRIPTS / "dashboard.py")
dashboard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dashboard)
import dataset  # noqa: E402

HEADER = (
    "trial_id,participant,kata,treatment,practice,status,limit_seconds,"
    "elapsed_seconds,time_to_green_seconds,censored,incident,total,passed,failed,"
    "skipped,success_percent,loc_total,method_count,complexity_avg,duplicated_loc,"
    "duplication_percent"
)


def row(trial_id, participant, kata, treatment, seconds, status="completed", loc=30):
    censored = status == "censored"
    green = "" if censored else seconds
    failed = 2 if censored else 0
    return (
        f"{trial_id},{participant},{kata},{treatment},False,{status},2100,{seconds},"
        f"{green},{censored},,8,{8 - failed},{failed},0,{(8 - failed) * 12.5},{loc},1,5.0,0,0.0"
    )


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def frame(self, *rows):
        csv = self.root / "consolidado.csv"
        csv.write_text("\n".join([HEADER, *rows]) + "\n")
        return dataset.load(csv)

    def sample(self):
        return self.frame(
            row("a1", "ana", "kata-01", "sem-ia", 600),
            row("a2", "ana", "kata-02", "com-ia", 120),
            row("b1", "bia", "kata-01", "com-ia", 180),
            row("b2", "bia", "kata-02", "sem-ia", 2100, status="censored"),
            row("c1", "caio", "kata-01", "com-ia", 240),
        )

    def test_summary_medians_rates_and_censoring(self):
        s = dashboard.summary(self.sample())
        self.assertEqual(s["n"], 5)
        self.assertEqual(s["by_treatment"]["sem-ia"]["n"], 2)
        self.assertEqual(s["by_treatment"]["com-ia"]["n"], 3)
        # Mediana de tempo considera só trials concluídos (censurados à parte).
        self.assertEqual(s["by_treatment"]["sem-ia"]["median_minutes"], 10.0)
        self.assertEqual(s["by_treatment"]["com-ia"]["median_minutes"], 3.0)
        self.assertEqual(s["by_treatment"]["sem-ia"]["success_rate"], 50.0)
        self.assertEqual(s["by_treatment"]["com-ia"]["success_rate"], 100.0)
        self.assertEqual(s["censored"], 1)
        self.assertAlmostEqual(s["speedup"], 10.0 / 3.0)

    def test_missing_pairs_lists_participants_without_a_treatment(self):
        gaps = dashboard.missing_pairs(self.sample())
        self.assertEqual(gaps, [("caio", "sem-ia")])

    def test_build_writes_page_and_figures(self):
        out = self.root / "dashboard"
        dashboard.build(self.sample(), out)
        html = (out / "index.html").read_text(encoding="utf-8")
        self.assertIn("<svg", html)
        self.assertIn("caio", html)  # aviso de par ausente
        self.assertIn("a1", html)  # tabela / tooltip do trial
        for name in dashboard.FIGURES:
            self.assertTrue((out / f"{name}.png").exists(), name)
            self.assertTrue((out / f"{name}.svg").exists(), name)

    def test_build_uses_theme_variables_in_inline_svg(self):
        out = self.root / "dashboard"
        dashboard.build(self.sample(), out)
        html = (out / "index.html").read_text(encoding="utf-8")
        self.assertIn("var(--sem-ia)", html)
        self.assertIn("var(--com-ia)", html)


if __name__ == "__main__":
    unittest.main()
