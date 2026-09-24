import java.util.*;

public class RouteChainer {
    public static List<String> chain(List<String> trechos) {
        List<String> resultado = new ArrayList<>();
        if (trechos == null || trechos.isEmpty()) {
            return resultado;
        }

        // Regra 1: validação individual (duplicatas são mantidas de propósito)
        List<String[]> validos = new ArrayList<>();
        for (String t : trechos) {
            String[] par = parse(t);
            if (par != null) validos.add(par);
        }

        // Regra 2: ramificação (origem repetida) e convergência (destino repetido)
        Map<String, Integer> contOrigem = new HashMap<>();
        Map<String, Integer> contDestino = new HashMap<>();
        for (String[] v : validos) {
            contOrigem.merge(v[0], 1, Integer::sum);
            contDestino.merge(v[1], 1, Integer::sum);
        }

        Map<String, String> proximo = new LinkedHashMap<>();
        Set<String> destinos = new HashSet<>();
        for (String[] v : validos) {
            if (contOrigem.get(v[0]) > 1 || contDestino.get(v[1]) > 1) continue;
            proximo.put(v[0], v[1]);
            destinos.add(v[1]);
        }

        // Regras 3 e 4: encadeia a partir das cidades que não são destino de nenhum trecho.
        // Cadeias fechadas (ciclos) não têm ponto de partida e nunca entram no resultado;
        // o conjunto de visitadas é uma proteção extra contra ciclos.
        for (String inicio : proximo.keySet()) {
            if (destinos.contains(inicio)) continue;
            List<String> cidades = new ArrayList<>();
            Set<String> visitadas = new HashSet<>();
            String atual = inicio;
            boolean ciclo = false;
            while (atual != null) {
                if (!visitadas.add(atual)) { ciclo = true; break; }
                cidades.add(atual);
                atual = proximo.get(atual);
            }
            if (!ciclo) resultado.add(String.join("-", cidades));
        }

        // Regra 5: ordena pela primeira cidade do itinerário
        resultado.sort(Comparator.comparing(it -> it.substring(0, it.indexOf('-'))));
        return resultado;
    }

    private static String[] parse(String t) {
        if (t == null) return null;
        int i = t.indexOf('-');
        if (i < 0 || i != t.lastIndexOf('-')) return null; // exatamente um hífen
        String origem = t.substring(0, i);
        String destino = t.substring(i + 1);
        if (!identificadorValido(origem) || !identificadorValido(destino)) return null;
        if (origem.equals(destino)) return null;
        return new String[]{origem, destino};
    }

    // Identificador não vazio e sem espaços (nem internos nem nas pontas)
    private static boolean identificadorValido(String id) {
        if (id.isEmpty()) return false;
        for (int k = 0; k < id.length(); k++) {
            if (Character.isWhitespace(id.charAt(k))) return false;
        }
        return true;
    }
}