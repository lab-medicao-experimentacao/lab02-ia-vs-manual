import java.util.*;

public class RouteChainer {

    private record Trecho(String origem, String destino) {}

    public static List<String> chain(List<String> trechos) {
        if (trechos == null || trechos.isEmpty()) {
            return Collections.emptyList();
        }

        // 1. Filtragem individual de trechos inválidos
        List<Trecho> validosIndividuais = new ArrayList<>();
        for (String item : trechos) {
            if (item == null) {
                continue;
            }

            int primeiroHifen = item.indexOf('-');
            int ultimoHifen = item.lastIndexOf('-');

            // Deve conter exatamente um hífen
            if (primeiroHifen == -1 || primeiroHifen != ultimoHifen) {
                continue;
            }

            String origem = item.substring(0, primeiroHifen);
            String destino = item.substring(primeiroHifen + 1);

            // Origem e destino não vazios e distintos entre si
            if (origem.isEmpty() || destino.isEmpty() || origem.equals(destino)) {
                continue;
            }

            validosIndividuais.add(new Trecho(origem, destino));
        }

        if (validosIndividuais.isEmpty()) {
            return Collections.emptyList();
        }

        // 2. Detecção de ramificações (origens duplicadas) e convergências (destinos duplicados)
        Map<String, Integer> contagemOrigem = new HashMap<>();
        Map<String, Integer> contagemDestino = new HashMap<>();

        for (Trecho t : validosIndividuais) {
            contagemOrigem.put(t.origem(), contagemOrigem.getOrDefault(t.origem(), 0) + 1);
            contagemDestino.put(t.destino(), contagemDestino.getOrDefault(t.destino(), 0) + 1);
        }

        // Descarta trechos envolvidos em ramificação ou convergência
        List<Trecho> trechosValidos = new ArrayList<>();
        for (Trecho t : validosIndividuais) {
            if (contagemOrigem.get(t.origem()) == 1 && contagemDestino.get(t.destino()) == 1) {
                trechosValidos.add(t);
            }
        }

        if (trechosValidos.isEmpty()) {
            return Collections.emptyList();
        }

        // Mapeamentos para travessia: proximoDestino e antecessor
        Map<String, String> proximoDestino = new HashMap<>();
        Set<String> temAntecessor = new HashSet<>();
        Set<String> todosVertices = new HashSet<>();

        for (Trecho t : trechosValidos) {
            proximoDestino.put(t.origem(), t.destino());
            temAntecessor.add(t.destino());
            todosVertices.add(t.origem());
            todosVertices.add(t.destino());
        }

        // 3. Montar itinerários a partir de nós iniciais (in-degree == 0)
        List<String> itinerarios = new ArrayList<>();
        Set<String> verticesVisitadosEmCadeias = new HashSet<>();

        for (Trecho t : trechosValidos) {
            String inicio = t.origem();
            if (!temAntecessor.contains(inicio) && !verticesVisitadosEmCadeias.contains(inicio)) {
                List<String> caminho = new ArrayList<>();
                Set<String> visitadosNoCaminho = new HashSet<>();
                String atual = inicio;
                boolean temCiclo = false;

                while (atual != null) {
                    if (visitadosNoCaminho.contains(atual)) {
                        temCiclo = true;
                        break;
                    }
                    visitadosNoCaminho.add(atual);
                    caminho.add(atual);
                    atual = proximoDestino.get(atual);
                }

                // Se não formou ciclo, adiciona o itinerário formatado
                if (!temCiclo) {
                    verticesVisitadosEmCadeias.addAll(caminho);
                    itinerarios.add(String.join("-", caminho));
                }
            }
        }

        // 4. Ordenar alfabeticamente pela primeira cidade
        // Como o itinerário começa com a primeira cidade e hifens/letras mantêm a ordem lexicográfica pelo prefixo,
        // ordenamos diretamente pelo nome da cidade inicial.
        itinerarios.sort(Comparator.comparing(rota -> rota.split("-")[0]));

        return itinerarios;
    }
}