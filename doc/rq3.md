# LAB02 — Análise estrutural RQ3 (Issue #33)

**RQ3 — O uso do assistente de IA altera as métricas estruturais do código?** Hipóteses
**não direcionais** para complexidade ciclomática média/método (RQ3a) e percentual de
duplicação (RQ3b); LOC (RQ3c) é métrica de **controle** para interpretar as outras duas
([protocolo-estatistico.md](protocolo-estatistico.md) §4).

## Como reproduzir

```bash
docker compose run --rm lab sh -c "python scripts/metrics.py collect-all && python scripts/trial.py export && python scripts/rq3.py"
```

Saídas: `results/rq3.csv` (teste por métrica) e `results/rq3_pares.csv` (pares por
participante). Ferramentas: pandas 2.2.3, numpy 2.1.3, scipy 1.14.1
(`scipy.stats.wilcoxon`, `method="exact"`).

## Método

Segue o [protocolo estatístico](protocolo-estatistico.md) (Issue #30):

1. **Elegibilidade.** Trials `completed` ou `censored` com `metrics.json` (§3). Os 18
   trials oficiais são elegíveis: todos `completed`, nenhum excluído.
2. **Agregação (§2).** Para cada participante, a **mediana** dos 3 trials de cada
   tratamento, formando um par `(sem-ia, com-ia)` por métrica — **n = 3 pares**.
3. **Teste (§6).** Wilcoxon dos postos sinalizados pareado, **bilateral**, α = 0,05, sobre
   as diferenças `com-ia − sem-ia`. Pares com diferença zero são descartados antes dos
   postos (`zero_method="wilcox"`).
4. **Tamanho de efeito.** Correlação rank-biserial pareada,
   `r = (W⁺ − W⁻) / (W⁺ + W⁻)`, de −1 (com-ia sempre menor) a +1 (com-ia sempre maior).

**Resolução do teste.** Com 3 pares, o menor p-valor bilateral possível é
2 × 1/2³ = **0,25** (as três diferenças no mesmo sentido). Logo **nenhum** resultado pode
ser significativo a 5% neste desenho; o teste é reportado por rigor de protocolo, e a
leitura se apoia nos pares e na descritiva ([limitacao-inferencial.md](limitacao-inferencial.md)).

## Resultados

### Pares por participante (mediana dos 3 trials)

| Métrica | Participante | sem-ia | com-ia | Diferença (com − sem) |
|---|---|---|---|---|
| Complexidade média/método | gabriel | 6,67 | 11,00 | +4,33 |
| | joaquim_vilela | 11,00 | 7,00 | −4,00 |
| | vitor | 10,00 | 4,67 | −5,33 |
| Duplicação (%) | gabriel | 0 | 0 | 0 |
| | joaquim_vilela | 0 | 0 | 0 |
| | vitor | 0 | 0 | 0 |
| LOC | gabriel | 24 | 70 | +46 |
| | joaquim_vilela | 59 | 26 | −33 |
| | vitor | 40 | 26 | −14 |

### Testes

| RQ | Métrica | Pares (efetivos) | Mediana das dif. | W | p (bilateral) | r (rank-biserial) | Decisão |
|---|---|---|---|---|---|---|---|
| RQ3a | Complexidade média/método | 3 (3) | −4,00 | 2 | 0,75 | −0,33 | Não rejeita H₀ |
| RQ3b | Duplicação (%) | 3 (0) | 0 | — | — | — | Teste não aplicável |
| RQ3c | LOC (controle) | 3 (3) | −14 | 3 | 1,00 | 0,00 | Não rejeita H₀ |

### Leitura por kata (mediana de cada tratamento)

| Kata | Complexidade sem-ia | Complexidade com-ia | LOC sem-ia | LOC com-ia |
|---|---|---|---|---|
| kata-01 | 5,00 | 5,00 | 23,0 | 19,5 |
| kata-02 | 10,50 | 11,00 | 42,0 | 44,0 |
| kata-03 | 7,00 | 7,00 | 24,0 | 26,0 |
| kata-04 | 10,00 | 9,00 | 55,5 | 70,0 |
| kata-05 | 6,67 | 8,83 | 67,0 | 41,5 |
| kata-06 | 13,17 | 23,00 | 59,0 | 79,0 |

Cada kata tem 3 trials em proporção 2:1 entre tratamentos, e o tratamento dentro de um
kata coincide com o participante. Esta tabela é **descritiva**: diferenças entre colunas
misturam efeito do tratamento com estilo do participante.

## Interpretação

- **Complexidade (RQ3a).** Não há direção consistente: dois participantes (Joaquim e
  Vitor) produziram código **menos** complexo com IA, e um (Gabriel) **mais**. A mediana
  das diferenças é −4, mas o efeito é fraco (r = −0,33) e p = 0,75. Por kata, os valores
  são quase iguais em kata-01 a kata-04; as maiores diferenças estão em kata-05 e
  kata-06, puxadas por um único trial com IA em cada (Joaquim no kata-05, complexidade
  13; Gabriel no kata-06, 23), ambos com toda a lógica em um só método.
- **Duplicação (RQ3b).** CPD não detectou duplicação em **nenhum** dos 18 trials (0% em
  todos). As soluções são curtas (18–79 LOC) e nenhum trecho repetido atinge o limiar de
  50 tokens do CPD ([metricas.md](metricas.md)); o resultado indica que a métrica **não discrimina**
  neste experimento, não que os tratamentos sejam equivalentes em duplicação.
- **LOC (RQ3c, controle).** O padrão acompanha o da complexidade: Gabriel escreveu mais
  código com IA (+46) e os outros dois, menos. Isso sugere que a variação de complexidade
  está ligada ao tamanho da solução de cada participante, e não a um efeito isolado do
  tratamento.
- **Conclusão para RQ3.** Os dados **não** mostram que a IA altere de forma consistente a
  estrutura do código. Com n = 3 pares e p mínimo de 0,25, a ausência de significância
  **não** é evidência de equivalência ([decisoes.md](decisoes.md) §8.6); é uma leitura
  exploratória em que a variação entre participantes supera a diferença entre
  tratamentos.

## Limitações específicas

- Tratamento confundido com participante dentro de cada kata (contrabalanceamento 2:1,
  [decisoes.md](decisoes.md) §8.3).
- Complexidade média por método é sensível ao número de métodos: 13 dos 18 trials têm
  um único método, em que a "média" é a complexidade total da solução (ver outlier de
  kata-05 em
  [descritiva.md](descritiva.md)); tratamento de outliers na Issue #64.
- Duplicação sem variância: a métrica não contribui para a comparação com katas deste
  tamanho.
