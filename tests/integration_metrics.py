"""Validação com PMD/CPD reais; execute no Docker."""

from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import metrics

COMPLEX_JAVA = """public class Complex {
    public int classify(int x) {
        if (x < 0) {
            return -1;
        } else if (x == 0) {
            return 0;
        } else if (x < 10) {
            return 1;
        } else if (x < 100) {
            return 2;
        } else {
            return 3;
        }
    }

    public int simple(int x) {
        return x + 1;
    }
}
"""

DUP_JAVA = """public class Dup {
    public int classify(int x) {
        if (x < 0) {
            return -1;
        } else if (x == 0) {
            return 0;
        } else if (x < 10) {
            return 1;
        } else if (x < 100) {
            return 2;
        } else {
            return 3;
        }
    }
}
"""

with tempfile.TemporaryDirectory() as temp:
    source = Path(temp) / "src/main/java"
    source.mkdir(parents=True)
    (source / "Complex.java").write_text(COMPLEX_JAVA)
    (source / "Dup.java").write_text(DUP_JAVA)

    result = metrics.collect(source)

    assert result["complexity"]["method_count"] == 3, result
    assert sorted(result["complexity"]["per_method"]) == [1, 5, 5], result
    assert result["complexity"]["average"] == (1 + 5 + 5) / 3, result

    # classify() é idêntico nos dois arquivos (14 linhas cada); simple() é exclusivo.
    assert result["duplication"]["duplicated_loc"] > 0, result
    assert 0 < result["duplication"]["percent"] < 100, result

    assert result["loc"]["total"] == sum(result["loc"]["per_file"].values())

print(
    "Integração PMD/CPD: complexidade e duplicação calculadas sobre código real "
    f"(complexidade média={result['complexity']['average']:.2f}, "
    f"duplicação={result['duplication']['percent']:.1f}%)."
)
