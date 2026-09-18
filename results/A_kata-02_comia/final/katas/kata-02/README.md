# Kata 02 — Agrupador de Extrato

Implemente `LedgerGrouper.group(List<String> lancamentos)`, que consolida
lançamentos de um extrato por categoria.

## Entrada

Cada lançamento é uma string no formato `"categoria:valor"`, onde:

- `categoria` é um texto (pode conter espaços internos, mas não `:`);
- `valor` é um inteiro, possivelmente negativo (ex.: `"mercado:-30"`).

## Regras

1. Some os valores de todos os lançamentos de uma mesma categoria.
2. A comparação de categoria é **sensível a maiúsculas/minúsculas** e usa a
   categoria já aparada (sem espaços nas pontas).
3. Espaços antes e depois de `categoria` e de `valor` são ignorados
   (ex.: `" mercado : 10 "` conta como `mercado` = `10`).
4. Lançamentos `null`, vazios ou fora do formato `categoria:valor` são ignorados.
5. A saída é uma lista de strings `"categoria=total"`, ordenada por **total
   decrescente**; em caso de empate no total, por **categoria em ordem alfabética
   crescente**.

Entrada `null` ou vazia resulta em lista vazia.

## Assinatura

```java
public class LedgerGrouper {
    public static java.util.List<String> group(java.util.List<String> lancamentos) { ... }
}
```

## Exemplo

Entrada:

```
["mercado:100", "transporte:50", "mercado:-30", "lazer:20", "transporte:20"]
```

Saída:

```
["mercado=70", "transporte=70", "lazer=20"]
```

(`mercado` e `transporte` empatam em 70; o desempate é alfabético crescente,
então `mercado` precede `transporte`. `lazer=20` vem por último por ter o menor total.)
