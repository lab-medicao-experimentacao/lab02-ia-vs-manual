public class RunCompressor {
    public static String compress(String entrada) {
        if (entrada == null) {
            return null;
        }
        if (entrada.isEmpty()) {
            return "";
        }
        StringBuilder saida = new StringBuilder();
        int inicio = 0;
        while (inicio < entrada.length()) {
            char atual = entrada.charAt(inicio);
            int fim = inicio;
            while (fim < entrada.length() && entrada.charAt(fim) == atual) {
                fim++;
            }
            int tamanho = fim - inicio;
            if (tamanho >= 2) {
                saida.append(tamanho);
            }
            saida.append(atual);
            inicio = fim;
        }
        return saida.toString();
    }
}
