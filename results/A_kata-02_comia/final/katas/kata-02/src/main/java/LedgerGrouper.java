import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class LedgerGrouper {

    public static List<String> group(List<String> lancamentos) {
        if (lancamentos == null || lancamentos.isEmpty()) {
            return new ArrayList<>();
        }

        Map<String, Long> totais = new HashMap<>();

        for (String lancamento : lancamentos) {
            if (lancamento == null || lancamento.isBlank()) {
                continue;
            }

            int separador = lancamento.indexOf(':');

            // Deve existir exatamente um ":".
            if (separador <= 0 || separador != lancamento.lastIndexOf(':')) {
                continue;
            }

            String categoria = lancamento.substring(0, separador).strip();
            String valorTexto = lancamento.substring(separador + 1).strip();

            if (categoria.isEmpty() || valorTexto.isEmpty()) {
                continue;
            }

            try {
                long valor = Long.parseLong(valorTexto);
                totais.merge(categoria, valor, Long::sum);
            } catch (NumberFormatException ignorado) {
                // Lançamento inválido: ignora.
            }
        }

        return totais.entrySet()
                .stream()
                .sorted(
                        Comparator
                                .<Map.Entry<String, Long>>comparingLong(
                                        Map.Entry::getValue
                                )
                                .reversed()
                                .thenComparing(Map.Entry::getKey)
                )
                .map(entry -> entry.getKey() + "=" + entry.getValue())
                .toList();
    }
}