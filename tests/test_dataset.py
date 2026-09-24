import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    "dataset", Path(__file__).resolve().parents[1] / "scripts/dataset.py"
)
dataset = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dataset)

HEADER = (
    "trial_id,participant,kata,treatment,practice,status,limit_seconds,"
    "elapsed_seconds,time_to_green_seconds,censored,incident,total,passed,failed,"
    "skipped,success_percent,loc_total,method_count,complexity_avg,duplicated_loc,"
    "duplication_percent"
)


class DatasetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.csv = Path(self.tmp.name) / "consolidado.csv"

    def load(self, *rows, header=HEADER):
        self.csv.write_text("\n".join([header, *rows]) + "\n")
        return dataset.load(self.csv)

    def test_converts_types(self):
        df = self.load(
            "t1,vitor,kata-01,com-ia,False,completed,2100,99.5,99.5,False,,8,8,0,0,100.0,18,1,4.0,0,0.0"
        )
        row = df.iloc[0]
        self.assertEqual(row["time_to_green_seconds"], 99.5)
        self.assertEqual(row["loc_total"], 18)
        self.assertIs(bool(row["censored"]), False)
        self.assertEqual(list(df["treatment"].cat.categories), ["sem-ia", "com-ia"])

    def test_keeps_missing_values_as_nan(self):
        df = self.load(
            "t1,vitor,kata-02,sem-ia,False,censored,2100,2100,,True,,8,6,2,0,75.0,,,,,"
        )
        row = df.iloc[0]
        self.assertTrue(row["time_to_green_seconds"] != row["time_to_green_seconds"])
        self.assertFalse(row["has_metrics"])

    def test_adds_minutes(self):
        df = self.load(
            "t1,vitor,kata-01,com-ia,False,completed,2100,90,90,False,,8,8,0,0,100.0,18,1,4.0,0,0.0"
        )
        self.assertEqual(df.iloc[0]["time_to_green_minutes"], 1.5)
        self.assertTrue(df.iloc[0]["has_metrics"])

    def test_drops_practice_trials(self):
        df = self.load(
            "t1,vitor,kata-01,com-ia,False,completed,2100,90,90,False,,8,8,0,0,100.0,18,1,4.0,0,0.0",
            "t2,vitor,smoke,sem-ia,True,completed,60,5,5,False,,1,1,0,0,100.0,3,1,1.0,0,0.0",
        )
        self.assertEqual(list(df["trial_id"]), ["t1"])

    def test_rejects_csv_without_metric_columns(self):
        header = HEADER.split(",loc_total")[0]
        with self.assertRaisesRegex(ValueError, "trial.py export"):
            self.load(
                "t1,vitor,kata-01,com-ia,False,completed,2100,90,90,False,,8,8,0,0,100.0",
                header=header,
            )


if __name__ == "__main__":
    unittest.main()
