import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ScheduleValidatorTest {

    @Test
    void detectaSobreposicaoSimples() {
        assertEquals(List.of("daily & review"),
                ScheduleValidator.conflicts(List.of(
                        "daily 09:00-09:15", "review 09:10-10:00", "lunch 12:00-13:00")));
    }

    @Test
    void bordasQueSeTocamNaoConflitam() {
        assertTrue(ScheduleValidator.conflicts(List.of(
                "a 10:00-11:00", "b 11:00-12:00")).isEmpty());
    }

    @Test
    void ordenaNomesDentroDoPar() {
        assertEquals(List.of("a & z"),
                ScheduleValidator.conflicts(List.of("z 09:00-10:00", "a 09:30-09:45")));
    }

    @Test
    void ordenaListaDeConflitosAlfabeticamente() {
        assertEquals(List.of("a & b", "a & c"),
                ScheduleValidator.conflicts(List.of(
                        "a 09:00-12:00", "b 09:30-10:00", "c 11:00-11:30")));
    }

    @Test
    void reuniaoTotalmenteContidaEmOutra() {
        assertEquals(List.of("externa & interna"),
                ScheduleValidator.conflicts(List.of(
                        "externa 08:00-18:00", "interna 12:00-13:00")));
    }

    @Test
    void ignoraEntradasForaDoFormato() {
        assertEquals(List.of("daily & review"),
                ScheduleValidator.conflicts(Arrays.asList(
                        "daily 09:00-09:15", "review 09:10-10:00", "invalido", "", "  ", null)));
    }

    @Test
    void semConflitosResultaListaVazia() {
        assertTrue(ScheduleValidator.conflicts(List.of(
                "a 08:00-09:00", "b 09:00-10:00", "c 10:00-11:00")).isEmpty());
    }

    @Test
    void entradaNulaResultaListaVazia() {
        assertTrue(ScheduleValidator.conflicts(null).isEmpty());
    }
}
