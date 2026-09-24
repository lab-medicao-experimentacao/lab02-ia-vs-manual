import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ScheduleValidator {

    private static final Pattern FORMATO = Pattern.compile(
        "^(\\S+) ([01]\\d|2[0-3]):([0-5]\\d)-([01]\\d|2[0-3]):([0-5]\\d)$");

    public static List<String> conflicts(List<String> reunioes) {
        List<String> result = new ArrayList<>();
        if (reunioes == null || reunioes.isEmpty()) {
            return result;
        }

        List<String> nomes = new ArrayList<>();
        List<int[]> intervalos = new ArrayList<>();
        for (String r : reunioes) {
            if (r == null) continue;
            Matcher m = FORMATO.matcher(r);
            if (!m.matches()) continue;

            int inicio = Integer.parseInt(m.group(2)) * 60 + Integer.parseInt(m.group(3));
            int fim = Integer.parseInt(m.group(4)) * 60 + Integer.parseInt(m.group(5));
            if (inicio >= fim) continue;

            nomes.add(m.group(1));
            intervalos.add(new int[] {inicio, fim});
        }

        for (int i = 0; i < nomes.size(); i++) {
            for (int j = i + 1; j < nomes.size(); j++) {
                int[] a = intervalos.get(i);
                int[] b = intervalos.get(j);
                // fim exclusivo: bordas que só se tocam NÃO conflitam
                if (a[0] < b[1] && b[0] < a[1]) {
                    String x = nomes.get(i);
                    String y = nomes.get(j);
                    result.add(x.compareTo(y) < 0 ? x + " & " + y : y + " & " + x);
                }
            }
        }

        Collections.sort(result);
        return result;
    }
}