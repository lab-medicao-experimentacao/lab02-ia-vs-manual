# Resumo das perguntas ao Claude

- Modelo/esforço: Claude Sonnet 5, esforço High (Claude Code / terminal).
- Perguntei como interpretar e normalizar o campo `tipo`: confirmei com a IA se deveria
  fazer `trim()` e comparar em minúsculas contra `"email"`/`"telefone"`, mantendo a saída
  sempre em minúsculas independente do caso de entrada. A IA confirmou e alertou que o
  mesmo `trim()` deveria ser aplicado ao `valor`, não só ao `tipo` (o exemplo com
  `" Email : a@exemplo.com "` exige isso).
- Perguntei sobre a separação `tipo:valor`: se deveria cortar no primeiro `:` (tudo depois,
  incluindo `:` extras, vira valor) e se ausência de `:` deveria descartar o contato. A IA
  confirmou as duas coisas e sugeriu `indexOf(':')` em vez de `split`, para não truncar o
  valor por engano caso ele contivesse `:` adicionais.
- Perguntei sobre a estrutura geral do `mask()`: loop único com métodos auxiliares
  `maskEmail`/`maskTelefone` retornando `null` para inválido, versus tudo inline no loop.
  A IA recomendou os métodos separados por legibilidade/responsabilidade única e propôs o
  esqueleto do loop com `switch` sobre `tipo`.
- Propus a validação de e-mail via `valor.split("@", -1)` checando `length == 2` e nenhuma
  parte vazia (usando limite `-1` para não descartar `@` finais). A IA validou a abordagem
  percorrendo os casos-limite (`"a@"`, `"@b"`, `"a@b@c.com"`, `"ab"`) e confirmou que era
  equivalente ao `indexOf`/`lastIndexOf` que ela havia sugerido antes, só que mais legível.
- Propus a validação/mascaramento de telefone via `valor.matches("\\d{4,}")` seguido de
  `length - 4` asteriscos + últimos 4 dígitos. A IA conferiu contra os exemplos do
  enunciado (`"11987654321"` → `"*******4321"`, `"1234"` → `"1234"`) e confirmou.
- Perguntei se o retorno deveria ser `ArrayList` mutável ou algo imutável (`List.of`). A IA
  respondeu que `ArrayList` está correto, já que `assertEquals` compara por conteúdo
  (`List.equals`) e não por tipo concreto, e que envolver com `List.copyOf` no final seria
  complexidade sem ganho.
- Com as decisões acima fechadas, pedi para a IA escrever o arquivo completo.
- Rodei os testes uma única vez (ENTER no cronômetro): 8/8 passaram de primeira, sem
  necessidade de correções adicionais. Tempo até verde: 410,77s (~6min51s).
