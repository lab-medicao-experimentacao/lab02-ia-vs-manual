import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ScheduleValidator {

    private static final Pattern PADRAO = Pattern.compile(
            "^([^\\s]+) ([0-9]{2}):([0-9]{2})-([0-9]{2}):([0-9]{2})$"
    );

    private record Reuniao(String nome, int inicio, int fim) {
    }

    public static List<String> conflicts(List<String> reunioes) {
        if (reunioes == null || reunioes.isEmpty()) {
            return new ArrayList<>();
        }

        List<Reuniao> validas = new ArrayList<>();

        for (String texto : reunioes) {
            Reuniao reuniao = interpretar(texto);

            if (reuniao != null) {
                validas.add(reuniao);
            }
        }

        List<String> conflitos = new ArrayList<>();

        for (int i = 0; i < validas.size(); i++) {
            for (int j = i + 1; j < validas.size(); j++) {
                Reuniao primeira = validas.get(i);
                Reuniao segunda = validas.get(j);

                // Fim é exclusivo: reuniões que apenas se tocam não conflitam.
                boolean sobrepoem = primeira.inicio < segunda.fim
                        && segunda.inicio < primeira.fim;

                if (sobrepoem) {
                    String nomeA;
                    String nomeB;

                    if (primeira.nome.compareTo(segunda.nome) < 0) {
                        nomeA = primeira.nome;
                        nomeB = segunda.nome;
                    } else {
                        nomeA = segunda.nome;
                        nomeB = primeira.nome;
                    }

                    conflitos.add(nomeA + " & " + nomeB);
                }
            }
        }

        Collections.sort(conflitos);
        return conflitos;
    }

    private static Reuniao interpretar(String texto) {
        if (texto == null || texto.isEmpty()) {
            return null;
        }

        Matcher matcher = PADRAO.matcher(texto);

        if (!matcher.matches()) {
            return null;
        }

        int horaInicio = Integer.parseInt(matcher.group(2));
        int minutoInicio = Integer.parseInt(matcher.group(3));
        int horaFim = Integer.parseInt(matcher.group(4));
        int minutoFim = Integer.parseInt(matcher.group(5));

        if (horaInicio > 23 || horaFim > 23
                || minutoInicio > 59 || minutoFim > 59) {
            return null;
        }

        int inicio = horaInicio * 60 + minutoInicio;
        int fim = horaFim * 60 + minutoFim;

        if (inicio >= fim) {
            return null;
        }

        return new Reuniao(matcher.group(1), inicio, fim);
    }
}