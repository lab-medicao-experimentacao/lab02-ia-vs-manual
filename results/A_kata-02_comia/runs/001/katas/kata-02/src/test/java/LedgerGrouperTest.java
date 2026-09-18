import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class LedgerGrouperTest {

    @Test
    void somaValoresDaMesmaCategoria() {
        assertEquals(List.of("mercado=70"),
                LedgerGrouper.group(List.of("mercado:100", "mercado:-30")));
    }

    @Test
    void ordenaPorTotalDecrescente() {
        assertEquals(List.of("mercado=100", "lazer=20"),
                LedgerGrouper.group(List.of("lazer:20", "mercado:100")));
    }

    @Test
    void desempataPorCategoriaAlfabetica() {
        assertEquals(List.of("mercado=70", "transporte=70", "lazer=20"),
                LedgerGrouper.group(List.of(
                        "mercado:100", "transporte:50", "mercado:-30", "lazer:20", "transporte:20")));
    }

    @Test
    void aparaEspacosDeCategoriaEValor() {
        assertEquals(List.of("mercado=10"),
                LedgerGrouper.group(List.of(" mercado : 10 ")));
    }

    @Test
    void categoriaEhSensivelACaixa() {
        assertEquals(List.of("Mercado=5", "mercado=5"),
                LedgerGrouper.group(List.of("mercado:5", "Mercado:5")));
    }

    @Test
    void ignoraLancamentosForaDoFormato() {
        assertEquals(List.of("mercado=10"),
                LedgerGrouper.group(Arrays.asList("mercado:10", "invalido", "", "  ", null, "x:")));
    }

    @Test
    void entradaVaziaResultaListaVazia() {
        assertTrue(LedgerGrouper.group(List.of()).isEmpty());
    }

    @Test
    void entradaNulaResultaListaVazia() {
        assertTrue(LedgerGrouper.group(null).isEmpty());
    }
}
