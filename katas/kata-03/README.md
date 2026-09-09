# Kata 03 — Compressor de Corridas

Implemente `RunCompressor.compress(String entrada)`, uma variação de codificação
por corridas (run-length) com uma regra própria: caracteres isolados **não** são
prefixados por contagem.

## Regras

1. Uma "corrida" é uma sequência de caracteres iguais consecutivos.
2. Uma corrida de tamanho `n >= 2` é codificada como `n` seguido do caractere
   (ex.: `"aaaa"` → `"4a"`).
3. Uma corrida de tamanho `1` mantém o caractere literal, **sem** o número
   (ex.: `"a"` → `"a"`, e não `"1a"`).
4. A codificação preserva a ordem das corridas na string original.
5. Qualquer caractere é válido, inclusive dígitos e espaços; a contagem é sempre
   um número decimal em base 10 (ex.: `"aaaaaaaaaaaa"` → `"12a"`).

Entrada `null` resulta em `null`. Entrada vazia (`""`) resulta em `""`.

## Assinatura

```java
public class RunCompressor {
    public static String compress(String entrada) { ... }
}
```

## Exemplos

| Entrada | Saída |
|---|---|
| `"aaabccccd"` | `"3ab4cd"` |
| `"abc"` | `"abc"` |
| `"aa bb"` | `"2a 2b"` |
| `"1112"` | `"312"` |
| `""` | `""` |
| `null` | `null` |

No exemplo `"aa bb"`: corrida `aa` → `2a`, corrida ` ` (um espaço, tamanho 1) →
` `, corrida `bb` → `2b`, resultando em `"2a 2b"`.

No exemplo `"1112"`: corrida `111` → `31`, corrida `2` (tamanho 1) → `2`,
resultando em `"312"`.
