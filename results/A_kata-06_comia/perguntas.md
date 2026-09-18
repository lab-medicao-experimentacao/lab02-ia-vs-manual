# Resumo das perguntas ao Claude

- **Modelo e esforço exibidos na interface:** Sonnet 5, esforço High (conforme
  confirmado em `doc/decisoes.md` §3).
- **Prompt inicial:** o prompt padronizado (§3.1) seguido do enunciado do kata-06
  colado na íntegra.
- **Pergunta feita ao Claude durante o trial:** relatei dificuldade em estruturar a
  lógica de encadeamento dos trechos ("A-B" com "B-C") em conjunto com as regras de
  ramificação, convergência e detecção de ciclo, e pedi uma sugestão de como
  organizar isso de forma limpa em Java.
- **Resposta do Claude:** sugeriu enxergar o problema como um grafo em que, após os
  filtros de ramificação/convergência, cada nó tem no máximo uma aresta de entrada e
  uma de saída — reduzindo o problema a listas lineares ou ciclos isolados. Propôs 4
  passos: (1) saneamento básico do formato de cada trecho (um único `-`, origem/destino
  não vazios, origem ≠ destino); (2) contagem de ocorrências de cada cidade como origem
  e como destino em dois mapas, descartando trechos de cidades com contagem > 1; (3)
  identificar o início de cada itinerário como uma cidade sem antecessor (nunca aparece
  como destino) e caminhar pelos destinos seguintes, descartando o itinerário se uma
  cidade se repetir (ciclo) — notou que ciclos fechados não têm ponto de partida, pois
  toda cidade neles já tem antecessor; (4) formatar cada itinerário com
  `String.join("-", caminho)` e ordenar pela cidade inicial.
- **Resultado:** com essa orientação, a implementação de `RouteChainer` passou nos 8
  testes (`time_to_green_seconds` ≈ 238,3s).
