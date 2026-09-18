# Kata 01 — Normalizador de Etiquetas

Implemente `TagNormalizer.normalize(String entrada)`, que recebe uma linha de
etiquetas (tags) separadas por vírgula e devolve a lista normalizada.

## Regras

1. As etiquetas são separadas por vírgula (`,`). Espaços antes e depois de cada
   etiqueta são removidos.
2. Cada etiqueta é convertida para minúsculas.
3. Espaços internos são colapsados: qualquer sequência de espaços em branco dentro
   de uma etiqueta vira um único espaço simples (ex.: `"Code   Review"` → `"code review"`).
4. Etiquetas vazias (depois de aparar espaços) são descartadas.
5. Duplicatas são removidas, mantendo a **ordem da primeira ocorrência**.

A entrada pode ser `null` ou vazia; nesses casos o resultado é uma lista vazia.

## Assinatura

```java
public class TagNormalizer {
    public static java.util.List<String> normalize(String entrada) { ... }
}
```

## Exemplos

| Entrada | Saída |
|---|---|
| `"Java, java ,  JAVA"` | `["java"]` |
| `"  Code   Review , testing,  "` | `["code review", "testing"]` |
| `""` | `[]` |
| `null` | `[]` |
| `"a,b,a,c,b"` | `["a", "b", "c"]` |
