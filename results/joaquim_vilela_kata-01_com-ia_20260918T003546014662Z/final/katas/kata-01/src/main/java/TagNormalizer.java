import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class TagNormalizer {
    // Implementação inicial falha propositalmente: retorna lista vazia.
    public static List<String> normalize(String entrada) {
        ArrayList<String> resultado = new ArrayList<>();

        if (entrada == null || entrada.isEmpty()) {
            return resultado;
        }

        for (String tag : entrada.split(",")) {
            String tagNormalizada = tag
                    .trim()
                    .toLowerCase(Locale.ROOT)
                    .replaceAll("\\s+", " ");

            if (!tagNormalizada.isEmpty() && !resultado.contains(tagNormalizada)) {
                resultado.add(tagNormalizada);
            }
        }

        return resultado;
    }
}
