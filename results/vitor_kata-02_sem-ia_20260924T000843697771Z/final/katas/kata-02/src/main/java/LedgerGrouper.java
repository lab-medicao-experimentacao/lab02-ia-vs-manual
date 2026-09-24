import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class LedgerGrouper {

    public static List<String> group(List<String> lancamentos) {
        List<String> result = new ArrayList<>();
        if (lancamentos == null || lancamentos.isEmpty()) {
            return result;
        }

        Map<String, Long> totals = new HashMap<>();
        for (String lancamento : lancamentos) {
            if (lancamento == null) continue;

            String[] parts = lancamento.split(":", -1);
            if (parts.length != 2) continue;

            String categoria = parts[0].trim();
            String valorTxt = parts[1].trim();
            if (categoria.isEmpty() || valorTxt.isEmpty()) continue;

            long valor;
            try {
                valor = Integer.parseInt(valorTxt);
            } catch (NumberFormatException e) {
                continue;
            }

            totals.merge(categoria, valor, Long::sum);
        }

        List<Map.Entry<String, Long>> entries = new ArrayList<>(totals.entrySet());
        entries.sort((a, b) -> {
            int cmp = Long.compare(b.getValue(), a.getValue());
            return cmp != 0 ? cmp : a.getKey().compareTo(b.getKey());
        });

        for (Map.Entry<String, Long> e : entries) {
            result.add(e.getKey() + "=" + e.getValue());
        }
        return result;
    }
}