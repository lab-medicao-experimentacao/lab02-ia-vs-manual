import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ContactMaskerTest {

    @Test
    void mascaraEmailPadrao() {
        assertEquals(List.of("email:a***@exemplo.com"), ContactMasker.mask(List.of("email:ana.silva@exemplo.com")));
    }

    @Test
    void mascaraEmailComLocalDeUmCaractere() {
        assertEquals(List.of("email:a***@exemplo.com"), ContactMasker.mask(List.of("email:a@exemplo.com")));
    }

    @Test
    void mascaraTelefonePadrao() {
        assertEquals(List.of("telefone:*******4321"), ContactMasker.mask(List.of("telefone:11987654321")));
    }

    @Test
    void telefoneComExatamenteQuatroDigitosPermaneceIntacto() {
        assertEquals(List.of("telefone:1234"), ContactMasker.mask(List.of("telefone:1234")));
    }

    @Test
    void removeEspacosAoRedorDeTipoEValor() {
        assertEquals(List.of("email:a***@exemplo.com"), ContactMasker.mask(List.of(" Email : a@exemplo.com ")));
    }

    @Test
    void descartaEntradasInvalidas() {
        assertTrue(ContactMasker.mask(List.of(
                "email:invalido.com",
                "fax:123",
                "telefone:11a87654321",
                "telefone:123",
                "email:@exemplo.com",
                "semdoispontos"
        )).isEmpty());
    }

    @Test
    void preservaOrdemEIgnoraInvalidosEntreValidos() {
        assertEquals(
                List.of("email:a***@x.com", "telefone:*******4321"),
                ContactMasker.mask(List.of("email:a@x.com", "email:invalido", "telefone:11987654321")));
    }

    @Test
    void entradaNulaOuVaziaResultaListaVazia() {
        assertTrue(ContactMasker.mask(List.of()).isEmpty());
        assertTrue(ContactMasker.mask(null).isEmpty());
    }
}
