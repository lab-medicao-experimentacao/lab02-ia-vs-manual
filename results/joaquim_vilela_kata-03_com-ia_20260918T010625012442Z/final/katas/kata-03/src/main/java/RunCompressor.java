public class RunCompressor {
    // Implementação inicial falha propositalmente: devolve sempre uma string fixa.
    public static String compress(String entrada) {
        if (entrada == null) {
            return null;
        }

        if (entrada.isEmpty()) {
            return "";
        }

        StringBuilder resultado = new StringBuilder();
        int inicioCorrida = 0;

        while (inicioCorrida < entrada.length()) {
            int fimCorrida = inicioCorrida + 1;

            while (fimCorrida < entrada.length()
                    && entrada.charAt(fimCorrida) == entrada.charAt(inicioCorrida)) {
                fimCorrida++;
            }

            int tamanhoCorrida = fimCorrida - inicioCorrida;

            if (tamanhoCorrida >= 2) {
                resultado.append(tamanhoCorrida);
            }

            resultado.append(entrada.charAt(inicioCorrida));
            inicioCorrida = fimCorrida;
        }

        return resultado.toString();
    }
}
