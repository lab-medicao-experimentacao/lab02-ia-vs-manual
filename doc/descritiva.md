# LAB02 — Estatística descritiva por tratamento (RQ1/RQ2/RQ3)

Registro da estatística descritiva do experimento (Issue #31), com **mediana e IQR por
tratamento**, identificação de **trials censurados** e de **outliers**, conforme o
protocolo analítico de [doc/decisoes.md §7](decisoes.md#7-análise-planejada). É a etapa
descritiva que antecede os testes de hipótese (Wilcoxon pareado, Issue #32).

## Como reproduzir

```bash
# 1. Consolidar os trials oficiais em CSV
docker compose run --rm lab python scripts/trial.py export

# 2. Calcular mediana e IQR por tratamento
docker compose run --rm lab python scripts/descriptive_stats.py
```

Entradas: `results/consolidado.csv` (tempos, estados e contagens de teste) e os
`results/<trial_id>/metrics.json` (complexidade, duplicação e LOC). Saídas:
`results/descritiva.csv` (uma linha por métrica × tratamento) e a tabela no terminal.

## Métricas e regras de elegibilidade

| RQ | Métrica | Origem | Elegibilidade |
|---|---|---|---|
| RQ1 | Tempo até verde (s) | `time_to_green_seconds` | Apenas trials `completed`. Censurados são contados à parte, **nunca** como tempo de conclusão. |
| RQ2 | Testes falhando (nº) | `failed` | Trials com avaliação final válida (`total > 0`). |
| RQ3 | Complexidade ciclomática média/método | `metrics.json → complexity.average` | Trials com `metrics.json`. |
| RQ3 | Duplicação de linhas (%) | `metrics.json → duplication.percent` | Trials com `metrics.json`. |
| RQ3 | LOC (código do participante) | `metrics.json → loc.total` | Trials com `metrics.json`. |

- **IQR** = Q3 − Q1 (percentis 25 e 75).
- **Outliers**: regra de Tukey — valor abaixo de `Q1 − 1.5·IQR` ou acima de `Q3 + 1.5·IQR`.
- A censura é reportada por tratamento (concluídos / censurados / interrompidos); um
  registro de 35 min sem sucesso não representa tempo de conclusão (§7).

## Resultados (18 trials)

Executado sobre os **18 trials oficiais** (3 participantes × 6 katas, 9 por tratamento),
todos com `metrics.json`.

Censura por tratamento: `sem-ia` 9/9 concluídos; `com-ia` 9/9 concluídos. Nenhum
censurado ou interrompido.

| RQ | Métrica | Tratamento | n | Mediana | Q1 | Q3 | IQR | Outliers |
|---|---|---|---|---|---|---|---|---|
| RQ1 | Tempo até verde (s) | sem-ia | 9 | 820.35 | 550.49 | 1163.67 | 613.18 | 0 |
| RQ1 | Tempo até verde (s) | com-ia | 9 | 221.91 | 99.62 | 290.67 | 191.05 | 0 |
| RQ2 | Testes falhando (nº) | sem-ia | 9 | 0 | 0 | 0 | 0 | 0 |
| RQ2 | Testes falhando (nº) | com-ia | 9 | 0 | 0 | 0 | 0 | 0 |
| RQ3 | Complexidade ciclomática média/método | sem-ia | 9 | 8.33 | 7 | 11 | 4 | 1 |
| RQ3 | Complexidade ciclomática média/método | com-ia | 9 | 7 | 6 | 11 | 5 | 1 |
| RQ3 | Duplicação de linhas (%) | sem-ia | 9 | 0 | 0 | 0 | 0 | 0 |
| RQ3 | Duplicação de linhas (%) | com-ia | 9 | 0 | 0 | 0 | 0 | 0 |
| RQ3 | LOC (código do participante) | sem-ia | 9 | 47 | 37 | 59 | 22 | 0 |
| RQ3 | LOC (código do participante) | com-ia | 9 | 38 | 26 | 45 | 19 | 1 |

Leitura descritiva:

- **RQ1:** a mediana com IA é cerca de 3,7× menor (222 s contra 820 s), e o Q3 com IA
  (291 s) fica abaixo do Q1 sem IA (550 s).
- **RQ2:** todos os 18 trials terminaram com 8/8 testes passando; não há variação.
- **RQ3:** complexidade e LOC são um pouco menores com IA, com IQRs sobrepostos.
  Duplicação é 0% em todos os trials.

**Outliers identificados** (regra de Tukey), todos no kata-06 (Encadeador de Trechos):

| Métrica | Tratamento | Trial | Valor | Cerca |
|---|---|---|---|---|
| Complexidade média/método | sem-ia | joaquim_vilela/kata-06 | 18 | [1, 17] |
| Complexidade média/método | com-ia | A/kata-06 | 23 | [−1.5, 18.5] |
| LOC | com-ia | A/kata-06 | 79 | [−2.5, 73.5] |

A análise e a decisão de tratamento desses outliers estão em [outliers.md](outliers.md)
(Issue #64).

## Limitações

Com três participantes e o desenho within-subject, a leitura é exploratória (§7, §8.6).
Os 18 trials não devem ser tratados como observações independentes: a agregação por
participante, o tratamento de censura e os testes de hipótese seguem o
[protocolo estatístico](protocolo-estatistico.md) (Issue #30) e estão em
[rq1-rq2.md](rq1-rq2.md) (Issue #32) e [rq3.md](rq3.md) (Issue #33).
