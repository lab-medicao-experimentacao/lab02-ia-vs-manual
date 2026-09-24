import java.util.*;

public class RouteChainer {

    public static List<String> chain(List<String> trechos) {
        if (trechos == null || trechos.isEmpty()) {
            return List.of();
        }

        List<String[]> validos = new ArrayList<>();
        Map<String, Integer> origens = new HashMap<>();
        Map<String, Integer> destinos = new HashMap<>();

        for (String trecho : trechos) {
            if (trecho == null || trecho.indexOf('-') != trecho.lastIndexOf('-')) {
                continue;
            }

            String[] partes = trecho.split("-", -1);

            if (partes.length != 2 ||
                partes[0].isEmpty() ||
                partes[1].isEmpty() ||
                partes[0].equals(partes[1])) {
                continue;
            }

            validos.add(partes);

            origens.merge(partes[0], 1, Integer::sum);
            destinos.merge(partes[1], 1, Integer::sum);
        }

        Map<String, String> rotas = new HashMap<>();

        for (String[] trecho : validos) {
            String origem = trecho[0];
            String destino = trecho[1];

            if (origens.get(origem) == 1 &&
                destinos.get(destino) == 1) {
                rotas.put(origem, destino);
            }
        }

        List<String> resultado = new ArrayList<>();

        for (String inicio : rotas.keySet()) {

            if (rotas.containsValue(inicio)) {
                continue;
            }

            List<String> caminho = new ArrayList<>();
            Set<String> visitadas = new HashSet<>();

            String atual = inicio;
            boolean ciclo = false;

            while (rotas.containsKey(atual)) {
                if (!visitadas.add(atual)) {
                    ciclo = true;
                    break;
                }

                caminho.add(atual);
                atual = rotas.get(atual);
            }

            if (!ciclo) {
                caminho.add(atual);
                resultado.add(String.join("-", caminho));
            }
        }

        resultado.sort(String::compareTo);

        return resultado;
    }
}