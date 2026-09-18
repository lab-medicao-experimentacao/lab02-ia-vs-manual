import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;

public class TagNormalizer {

    public static List<String> normalize(String entrada) {
        if (entrada == null || entrada.isEmpty()) {
            return new ArrayList<>();
        }

        Set<String> tagsNormalizadas = new LinkedHashSet<>();

        for (String tag : entrada.split(",", -1)) {
            String normalizada = tag
                    .strip()
                    .replaceAll("(?U)\\s+", " ")
                    .toLowerCase(Locale.ROOT);

            if (!normalizada.isEmpty()) {
                tagsNormalizadas.add(normalizada);
            }
        }

        return new ArrayList<>(tagsNormalizadas);
    }
}