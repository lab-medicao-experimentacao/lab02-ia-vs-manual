public class RunCompressor {

    public static String compress(String entrada) {
        if (entrada == null || entrada.isEmpty()) {
            return entrada;
        }

        StringBuilder resultado = new StringBuilder();

        int inicio = 0;

        while (inicio < entrada.length()) {
            char caractere = entrada.charAt(inicio);
            int fim = inicio + 1;

            while (fim < entrada.length()
                    && entrada.charAt(fim) == caractere) {
                fim++;
            }

            int quantidade = fim - inicio;

            if (quantidade >= 2) {
                resultado.append(quantidade);
            }

            resultado.append(caractere);
            inicio = fim;
        }

        return resultado.toString();
    }
}