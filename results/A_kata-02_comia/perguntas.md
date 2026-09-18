# Resumo das perguntas ao Claude

- **Modelo e esforço exibidos na interface:** Sonnet 5, esforço High (conforme
  confirmado em `doc/decisoes.md` §3).
- **Prompt inicial:** o prompt padronizado (§3.1) seguido do enunciado do kata-02
  colado na íntegra.
- **Perguntas de esclarecimento feitas pelo Claude** (antes de propor a solução):
  1. Qual é o enunciado completo do kata? Pediu para colar também a assinatura exata
     da classe e do método exigidos.
  2. Perguntou se já havia alguma implementação em andamento ou se os testes
     estavam falhando, e solicitou o código atual e as mensagens de erro dos
     testes JUnit 5, caso houvesse.
- **Minhas respostas:** colei o enunciado completo do `README.md`, a assinatura de
  `LedgerGrouper.group(List<String>)` e o conteúdo do stub inicial (retornando lista
  vazia), sem mensagens de erro de teste (ainda não havia rodado os testes).
- **Observação:** não fiz perguntas adicionais de acompanhamento — a partir dessas
  duas respostas, o Claude já entregou a implementação completa, que passou nos 8
  testes na primeira execução (`time_to_green_seconds` ≈ 43,3s).
