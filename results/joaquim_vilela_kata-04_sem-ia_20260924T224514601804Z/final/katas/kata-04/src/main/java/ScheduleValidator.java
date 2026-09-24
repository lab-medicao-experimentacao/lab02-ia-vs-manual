import java.util.ArrayList;
import java.util.List;

public class ScheduleValidator {

    public static List<String> conflicts(List<String> reunioes) {
        List<String> resultado = new ArrayList<>();

        if (reunioes == null || reunioes.isEmpty()) {
            return resultado;
        }

        List<Reuniao> validas = new ArrayList<>();

        for (String reuniao : reunioes) {
            if (reuniao == null || reuniao.isEmpty()) {
                continue;
            }

            String[] partes = reuniao.split(" ", -1);

            if (partes.length != 2 || partes[0].isEmpty()) {
                continue;
            }

            String[] horarios = partes[1].split("-", -1);

            if (horarios.length != 2) {
                continue;
            }

            try {
                int inicio = minutos(horarios[0]);
                int fim = minutos(horarios[1]);

                

                validas.add(new Reuniao(partes[0], inicio, fim));

            } catch (IllegalArgumentException e) {
            }
        }

        for (int i = 0; i < validas.size(); i++) {
            for (int j = i + 1; j < validas.size(); j++) {
                Reuniao a = validas.get(i);
                Reuniao b = validas.get(j);

                if (a.inicio < b.fim && b.inicio < a.fim) {
                    String nomeA;
                    String nomeB;

                    if (a.nome.compareTo(b.nome) < 0) {
                        nomeA = a.nome;
                        nomeB = b.nome;
                    } else {
                        nomeA = b.nome;
                        nomeB = a.nome;
                    }

                    resultado.add(nomeA + " & " + nomeB);
                }
            }
        }

        resultado.sort(String::compareTo);

        return resultado;
    }

    private static int minutos(String horario) {
        if (!horario.matches("\\d{2}:\\d{2}")) {
            throw new IllegalArgumentException();
        }

        int hora = Integer.parseInt(horario.substring(0, 2));
        int minuto = Integer.parseInt(horario.substring(3, 5));

        if (hora < 0 || hora > 23 || minuto < 0 || minuto > 59) {
            throw new IllegalArgumentException();
        }

        return hora * 60 + minuto;
    }

    private static class Reuniao {
        String nome;
        int inicio;
        int fim;

        Reuniao(String nome, int inicio, int fim) {
            this.nome = nome;
            this.inicio = inicio;
            this.fim = fim;
        }
    }
}