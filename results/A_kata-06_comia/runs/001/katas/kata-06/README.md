# Kata 06 — Encadeador de Trechos

Implemente `RouteChainer.chain(List<String> trechos)`, que monta itinerários a
partir de trechos soltos de viagem (origem-destino).

## Entrada

Cada trecho é uma string no formato `"origem-destino"`, com exatamente um hífen
(`-`) separando dois identificadores não vazios (sem espaços internos).

## Regras

1. Um trecho é **inválido** — e descartado individualmente — quando: não tem
   exatamente um `-`; origem ou destino são vazios; ou origem é igual a destino
   (ex.: `"A-A"`). Entradas `null` também são descartadas.
2. Entre os trechos válidos restantes, uma cidade que aparece como **origem em mais
   de um trecho** (ramificação) torna **todos** os trechos com aquela origem
   inválidos; uma cidade que aparece como **destino em mais de um trecho**
   (convergência) torna **todos** os trechos com aquele destino inválidos. Essa
   filtragem é feita antes de montar as cadeias.
3. Os trechos restantes são encadeados quando o destino de um é a origem do
   próximo, formando itinerários (ex.: `"A-B"`, `"B-C"` → `"A-B-C"`). Um trecho sem
   continuação forma um itinerário de um trecho só.
4. Se seguir os trechos leva de volta a uma cidade já visitada no mesmo itinerário
   (ciclo), **todo** esse itinerário é descartado — ciclos não representam um
   itinerário válido.
5. A saída é a lista de itinerários, cada um como as cidades unidas por `-`
   (ex.: `"A-B-C"`), **ordenada alfabeticamente pela primeira cidade** do
   itinerário.

Entrada `null` ou vazia, ou sem trechos válidos, resulta em lista vazia.

## Assinatura

```java
public class RouteChainer {
    public static java.util.List<String> chain(java.util.List<String> trechos) { ... }
}
```

## Exemplos

| Entrada | Saída |
|---|---|
| `["A-B", "B-C", "D-E"]` | `["A-B-C", "D-E"]` |
| `["D-E"]` | `["D-E"]` |
| `["A-B", "A-C"]` | `[]` (A ramifica: origem duplicada) |
| `["A-C", "B-C"]` | `[]` (C converge: destino duplicado) |
| `["A-B", "B-A"]` | `[]` (ciclo) |
| `["A-A", "A-B", "", "X-Y-Z"]` | `["A-B"]` (demais trechos com formato inválido) |
