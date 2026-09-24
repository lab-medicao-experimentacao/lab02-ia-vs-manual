import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class LedgerGrouper {

    public static List<String> group(List<String> lancamentos) {
        if (lancamentos == null || lancamentos.isEmpty()) {
            return List.of();
        }

        Map<String, Integer> totais = new HashMap<>();

        for (String lancamento : lancamentos) {
            if (lancamento == null || lancamento.trim().isEmpty()) {
                continue;
            }

            int separador = lancamento.indexOf(':');

            if (separador <= 0 || separador == lancamento.length() - 1) {
                continue;
            }

            String categoria = lancamento.substring(0, separador).trim();
            String valorTexto = lancamento.substring(separador + 1).trim();

            if (categoria.isEmpty()) {
                continue;
            }

            try {
                int valor = Integer.parseInt(valorTexto);
                totais.merge(categoria, valor, Integer::sum);
            } catch (NumberFormatException e) {
            }
        }

        List<String> resultado = new ArrayList<>();

        for (Map.Entry<String, Integer> entrada : totais.entrySet()) {
            resultado.add(entrada.getKey() + "=" + entrada.getValue());
        }

        resultado.sort((a, b) -> {
            String[] partesA = a.split("=", 2);
            String[] partesB = b.split("=", 2);

            int totalA = Integer.parseInt(partesA[1]);
            int totalB = Integer.parseInt(partesB[1]);

            int comparacao = Integer.compare(totalB, totalA);

            if (comparacao != 0) {
                return comparacao;
            }

            return partesA[0].compareTo(partesB[0]);
        });

        return resultado;
    }
}