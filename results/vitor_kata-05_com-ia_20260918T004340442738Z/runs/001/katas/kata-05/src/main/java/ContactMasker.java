import java.util.ArrayList;
import java.util.List;

public class ContactMasker {
    public static List<String> mask(List<String> contatos) {
        List<String> resultado = new ArrayList<>();
        if (contatos == null) {
            return resultado;
        }

        for (String contato : contatos) {
            if (contato == null) {
                continue;
            }
            int separador = contato.indexOf(':');
            if (separador < 0) {
                continue;
            }

            String tipo = contato.substring(0, separador).trim().toLowerCase();
            String valor = contato.substring(separador + 1).trim();

            String mascarado = switch (tipo) {
                case "email" -> maskEmail(valor);
                case "telefone" -> maskTelefone(valor);
                default -> null;
            };

            if (mascarado != null) {
                resultado.add(tipo + ":" + mascarado);
            }
        }
        return resultado;
    }

    private static String maskEmail(String valor) {
        String[] partes = valor.split("@", -1);
        if (partes.length != 2 || partes[0].isEmpty() || partes[1].isEmpty()) {
            return null;
        }
        return partes[0].charAt(0) + "***@" + partes[1];
    }

    private static String maskTelefone(String valor) {
        if (!valor.matches("\\d{4,}")) {
            return null;
        }
        int qtdAsteriscos = valor.length() - 4;
        String ultimos4 = valor.substring(valor.length() - 4);
        return "*".repeat(qtdAsteriscos) + ultimos4;
    }
}
