import java.util.ArrayList;
import java.util.List;

public class ContactMasker {
    // Implementação inicial falha propositalmente: retorna lista vazia.
    public static List<String> mask(List<String> contatos) {
        List<String> resultado = new ArrayList<>();

        if (contatos == null || contatos.isEmpty()) {
            return resultado;
        }

        for (String contato : contatos) {
            if (contato == null) {
                continue;
            }

            int separador = contato.indexOf(':');
            if (separador < 0 || separador != contato.lastIndexOf(':')) {
                continue;
            }

            String tipo = contato.substring(0, separador).trim().toLowerCase();
            String valor = contato.substring(separador + 1).trim();

            if (tipo.equals("email")) {
                int arroba = valor.indexOf('@');

                if (arroba > 0
                        && arroba == valor.lastIndexOf('@')
                        && arroba < valor.length() - 1) {
                    String emailMascarado = valor.charAt(0)
                            + "***@"
                            + valor.substring(arroba + 1);
                    resultado.add("email:" + emailMascarado);
                }
            } else if (tipo.equals("telefone") && valor.matches("\\d{4,}")) {
                int quantidadeAsteriscos = valor.length() - 4;
                String telefoneMascarado = "*".repeat(quantidadeAsteriscos)
                        + valor.substring(valor.length() - 4);
                resultado.add("telefone:" + telefoneMascarado);
            }
        }

        return resultado;
    }
}
