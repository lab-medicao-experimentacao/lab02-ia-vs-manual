import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class RouteChainerTest {

    @Test
    void encadeiaTrechosSequenciais() {
        assertEquals(List.of("A-B-C"), RouteChainer.chain(List.of("A-B", "B-C")));
    }

    @Test
    void mantemTrechoIsoladoSemContinuacao() {
        assertEquals(List.of("D-E"), RouteChainer.chain(List.of("D-E")));
    }

    @Test
    void ordenaItinerariosPelaPrimeiraCidade() {
        assertEquals(List.of("A-B-C", "D-E"), RouteChainer.chain(List.of("D-E", "B-C", "A-B")));
    }

    @Test
    void descartaTrechosComOrigemRamificada() {
        assertTrue(RouteChainer.chain(List.of("A-B", "A-C")).isEmpty());
    }

    @Test
    void descartaTrechosComDestinoConvergente() {
        assertTrue(RouteChainer.chain(List.of("A-C", "B-C")).isEmpty());
    }

    @Test
    void descartaItinerarioComCiclo() {
        assertTrue(RouteChainer.chain(List.of("A-B", "B-A")).isEmpty());
    }

    @Test
    void descartaTrechosComFormatoInvalido() {
        assertEquals(List.of("A-B"), RouteChainer.chain(java.util.Arrays.asList("A-A", "A-B", "", null, "X-Y-Z")));
    }

    @Test
    void entradaNulaOuVaziaResultaListaVazia() {
        assertTrue(RouteChainer.chain(List.of()).isEmpty());
        assertTrue(RouteChainer.chain(null).isEmpty());
    }
}
