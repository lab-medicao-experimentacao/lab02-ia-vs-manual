# Kata 04 — Validador de Agenda

Implemente `ScheduleValidator.conflicts(List<String> reunioes)`, que detecta pares
de reuniões que se sobrepõem no tempo.

## Entrada

Cada reunião é uma string no formato `"nome HH:MM-HH:MM"`:

- `nome` é um identificador sem espaços (ex.: `"daily"`, `"1x1"`).
- O horário é um intervalo `inicio-fim` em relógio de 24 horas (`HH:MM`), com
  `inicio` estritamente antes de `fim` no mesmo dia.
- Exatamente um espaço separa o `nome` do intervalo.

## Regras

1. Duas reuniões **se sobrepõem** quando compartilham algum instante de tempo.
   Intervalos que apenas se tocam na borda **não** conflitam: `10:00-11:00` e
   `11:00-12:00` são compatíveis (fim exclusivo).
2. A saída é a lista de conflitos, um por par sobreposto, no formato
   `"nomeA & nomeB"`, onde `nomeA` e `nomeB` são ordenados **alfabeticamente**
   dentro do par (`nomeA` < `nomeB`).
3. A lista de conflitos é ordenada alfabeticamente pela string do par.
4. Entradas `null`, vazias ou fora do formato são ignoradas.
5. Não há reuniões com o mesmo nome; assuma nomes únicos entre as entradas válidas.

Entrada `null` ou vazia, ou sem conflitos, resulta em lista vazia.

## Assinatura

```java
public class ScheduleValidator {
    public static java.util.List<String> conflicts(java.util.List<String> reunioes) { ... }
}
```

## Exemplos

Entrada:

```
["daily 09:00-09:15", "review 09:10-10:00", "lunch 12:00-13:00"]
```

Saída:

```
["daily & review"]
```

Entrada com bordas que se tocam:

```
["a 10:00-11:00", "b 11:00-12:00"]
```

Saída:

```
[]
```
