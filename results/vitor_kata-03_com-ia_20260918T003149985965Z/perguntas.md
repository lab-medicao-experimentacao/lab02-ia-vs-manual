# Resumo das perguntas ao Claude

- Modelo/esforço: Claude Sonnet 5, esforço High (Claude Code / terminal).
- Após colar o enunciado do kata-03, pedi que a IA propusesse a abordagem de implementação de `RunCompressor.compress`.
- A IA sugeriu: varrer a string com dois ponteiros, identificando corridas de caracteres consecutivos iguais; para cada corrida, anexar a contagem ao resultado apenas quando o tamanho for `>= 2`, seguida do caractere; tratar `null` e `""` como casos especiais antes da varredura.
- Aprovei a abordagem sem alterações; a IA implementou o método diretamente no arquivo, usando `StringBuilder` para montar a saída.
- Rodei os testes uma única vez (ENTER no cronômetro): 8/8 passaram de primeira, sem necessidade de correções adicionais.
