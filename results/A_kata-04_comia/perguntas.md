# Resumo das perguntas ao Claude

- **Modelo e esforço exibidos na interface:** Sonnet 5, esforço High (conforme
  confirmado em `doc/decisoes.md` §3).
- **Prompt inicial:** o prompt padronizado (§3.1) seguido do enunciado do kata-04
  colado na íntegra.
- **Perguntas feitas ao Claude durante o trial:**
  1. Como verificar se duas reuniões conflitam? O Claude sugeriu converter os
     horários para minutos desde meia-noite e usar a condição
     `inicioA < fimB && inicioB < fimA`, observando que ela trata corretamente
     bordas que se tocam (ex.: `10:00-11:00` e `11:00-12:00` não conflitam).
  2. Como ordenar os nomes no resultado quando a entrada não vem em ordem
     alfabética (ex.: `"review 09:10-10:00"` antes de `"daily 09:00-09:15"`)? O
     Claude indicou ordenar os nomes do par com `compareTo`, independente da
     ordem de entrada.
  3. Deve aceitar horários sem zero à esquerda, como `"daily 9:00-10:00"`? O
     Claude esclareceu que não — o formato exige `HH:MM` com dois dígitos — e
     listou outros casos a rejeitar: `24:00-25:00`, `10:60-11:00`,
     `11:00-10:00` (fim antes do início) e `10:00-10:00` (intervalo vazio).
  4. Uma reunião pode aparecer em mais de um conflito? O Claude confirmou que
     sim, com um exemplo de três reuniões onde uma conflita com as outras duas,
     mas essas duas não conflitam entre si, gerando dois pares no resultado.
- **Resultado:** com as respostas acima, a implementação de `ScheduleValidator`
  passou nos 8 testes (`time_to_green_seconds` ≈ 183,2s).
