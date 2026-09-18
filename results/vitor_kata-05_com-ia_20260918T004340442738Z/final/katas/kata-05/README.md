# Kata 05 — Mascarador de Contatos

Implemente `ContactMasker.mask(List<String> contatos)`, que mascara uma lista de
contatos (e-mail ou telefone) para exibição segura.

## Entrada

Cada contato é uma string no formato `"tipo:valor"`, onde:

- `tipo` é `"email"` ou `"telefone"` (sensível a maiúsculas/minúsculas — comparar em
  minúsculas; a saída sempre usa `tipo` em minúsculas);
- `valor` é o endereço de e-mail ou o telefone (somente dígitos).
- Espaços antes e depois de `tipo` e de `valor` são ignorados.

## Regras

1. **E-mail:** `valor` deve conter exatamente um `@`, com parte local (antes do `@`)
   não vazia e domínio (depois do `@`) não vazio. O mascaramento mantém o **primeiro
   caractere** da parte local, seguido de `"***"`, seguido de `"@"` e do domínio
   inalterado (ex.: `"ana.silva@exemplo.com"` → `"a***@exemplo.com"`).
2. **Telefone:** `valor` deve conter **somente dígitos**, com **4 ou mais**
   caracteres. O mascaramento mantém os **últimos 4 dígitos** e substitui cada dígito
   anterior por `"*"` (ex.: `"11987654321"` → `"*******4321"`). Com exatamente 4
   dígitos, nenhum caractere é substituído (ex.: `"1234"` → `"1234"`).
3. Contatos com `tipo` desconhecido, `valor` inválido para o tipo (e-mail sem `@`
   ou com parte local/domínio vazios; telefone com caractere não numérico ou menos
   de 4 dígitos), formato sem `":"`, ou entrada `null`/vazia são **descartados** —
   não geram item na saída.
4. A ordem de entrada é preservada na saída, ignorando os contatos descartados.
5. A saída é uma lista de strings `"tipo:mascarado"`.

Entrada `null` ou vazia resulta em lista vazia.

## Assinatura

```java
public class ContactMasker {
    public static java.util.List<String> mask(java.util.List<String> contatos) { ... }
}
```

## Exemplos

| Entrada | Saída |
|---|---|
| `["email:ana.silva@exemplo.com"]` | `["email:a***@exemplo.com"]` |
| `["telefone:11987654321"]` | `["telefone:*******4321"]` |
| `["telefone:1234"]` | `["telefone:1234"]` |
| `[" Email : a@exemplo.com "]` | `["email:a***@exemplo.com"]` |
| `["email:invalido.com", "fax:123", "telefone:11a87654321"]` | `[]` |
| `["email:a@x.com", "email:invalido", "telefone:11987654321"]` | `["email:a***@x.com", "telefone:*******4321"]` |
