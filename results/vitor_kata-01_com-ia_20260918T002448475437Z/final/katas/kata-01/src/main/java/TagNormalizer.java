import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;

public class TagNormalizer {
    public static List<String> normalize(String entrada) {
        if (entrada == null) {
            return List.of();
        }
        LinkedHashSet<String> etiquetas = new LinkedHashSet<>();
        for (String bruta : entrada.split(",")) {
            String normalizada = bruta.trim().toLowerCase().replaceAll("\\s+", " ");
            if (!normalizada.isEmpty()) {
                etiquetas.add(normalizada);
            }
        }
        return new ArrayList<>(etiquetas);
    }
}
