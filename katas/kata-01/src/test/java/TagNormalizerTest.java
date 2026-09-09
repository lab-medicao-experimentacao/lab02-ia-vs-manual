import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class TagNormalizerTest {

    @Test
    void aparaEspacosEConverteParaMinusculas() {
        assertEquals(List.of("java", "kotlin"), TagNormalizer.normalize("  Java , KOTLIN "));
    }

    @Test
    void removeDuplicatasMantendoPrimeiraOcorrencia() {
        assertEquals(List.of("java"), TagNormalizer.normalize("Java, java , JAVA"));
    }

    @Test
    void preservaOrdemDeInsercao() {
        assertEquals(List.of("a", "b", "c"), TagNormalizer.normalize("a,b,a,c,b"));
    }

    @Test
    void colapsaEspacosInternos() {
        assertEquals(List.of("code review"), TagNormalizer.normalize("Code   Review"));
    }

    @Test
    void descartaEtiquetasVazias() {
        assertEquals(List.of("code review", "testing"), TagNormalizer.normalize("  Code   Review , testing,  "));
    }

    @Test
    void entradaVaziaResultaListaVazia() {
        assertTrue(TagNormalizer.normalize("").isEmpty());
    }

    @Test
    void entradaNulaResultaListaVazia() {
        assertTrue(TagNormalizer.normalize(null).isEmpty());
    }

    @Test
    void apenasSeparadoresResultaListaVazia() {
        assertTrue(TagNormalizer.normalize(" , , ").isEmpty());
    }
}
