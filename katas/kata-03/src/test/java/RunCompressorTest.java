import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

class RunCompressorTest {

    @Test
    void codificaCorridasComPrefixoDeContagem() {
        assertEquals("3ab4cd", RunCompressor.compress("aaabccccd"));
    }

    @Test
    void mantemCaracteresIsoladosLiterais() {
        assertEquals("abc", RunCompressor.compress("abc"));
    }

    @Test
    void tratamentoDeEspacosComoCaractere() {
        assertEquals("2a 2b", RunCompressor.compress("aa bb"));
    }

    @Test
    void corridaDeDigitosGeraContagemSeguidaDoDigito() {
        assertEquals("312", RunCompressor.compress("1112"));
    }

    @Test
    void contagemComMaisDeUmDigito() {
        assertEquals("12a", RunCompressor.compress("aaaaaaaaaaaa"));
    }

    @Test
    void umUnicoCaractere() {
        assertEquals("a", RunCompressor.compress("a"));
    }

    @Test
    void entradaVaziaResultaVazio() {
        assertEquals("", RunCompressor.compress(""));
    }

    @Test
    void entradaNulaResultaNula() {
        assertNull(RunCompressor.compress(null));
    }
}
