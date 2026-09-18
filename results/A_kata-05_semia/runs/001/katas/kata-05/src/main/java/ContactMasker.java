import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ContactMasker {

    public static List<String> mask(List<String> contatos) {
        if (contatos == null || contatos.isEmpty()) {
            return Collections.emptyList();
        }

        List<String> resultado = new ArrayList<>();

        for (String contato : contatos) {
            if (contato == null) {
                continue;
            }

            int divisor = contato.indexOf(':');
            if (divisor == -1) {
                continue;
            }

            String tipo = contato.substring(0, divisor).trim().toLowerCase();
            String valor = contato.substring(divisor + 1).trim();

            if (valor.isEmpty()) {
                continue;
            }

            switch (tipo) {
                case "email" -> {
                    String mascarado = mascararEmail(valor);
                    if (mascarado != null) {
                        resultado.add("email:" + mascarado);
                    }
                }
                case "telefone" -> {
                    String mascarado = mascararTelefone(valor);
                    if (mascarado != null) {
                        resultado.add("telefone:" + mascarado);
                    }
                }
                default -> {
                    // Tipos desconhecidos são ignorados
                }
            }
        }

        return resultado;
    }

    private static String mascararEmail(String email) {
        int arrobaIndex = email.indexOf('@');
        // Deve conter exatamente um '@', não podendo ser o primeiro nem o último caractere
        if (arrobaIndex <= 0 || arrobaIndex != email.lastIndexOf('@') || arrobaIndex == email.length() - 1) {
            return null;
        }

        char primeiroCaractere = email.charAt(0);
        String dominio = email.substring(arrobaIndex + 1);

        return primeiroCaractere + "***@" + dominio;
    }

    private static String mascararTelefone(String telefone) {
        int tamanho = telefone.length();
        if (tamanho < 4) {
            return null;
        }

        for (int i = 0; i < tamanho; i++) {
            if (!Character.isDigit(telefone.charAt(i))) {
                return null;
            }
        }

        if (tamanho == 4) {
            return telefone;
        }

        int digitosParaOcultar = tamanho - 4;
        return "*".repeat(digitosParaOcultar) + telefone.substring(digitosParaOcultar);
    }
}