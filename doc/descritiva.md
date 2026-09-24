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

## Resultados atuais (parciais)

Executado sobre os **12 trials coletados até agora** (dos 18 planejados). Os números
mudam à medida que os trials pendentes forem executados; basta rerodar os dois comandos.

Censura por tratamento: `sem-ia` 3/3 concluídos; `com-ia` 9/9 concluídos. Nenhum
censurado ou interrompido.

| RQ | Métrica | Tratamento | n | Mediana | Q1 | Q3 | IQR | Outliers |
|---|---|---|---|---|---|---|---|---|
| RQ1 | Tempo até verde (s) | sem-ia | 3 | 238.71 | 167.39 | 394.60 | 227.21 | 0 |
| RQ1 | Tempo até verde (s) | com-ia | 9 | 221.91 | 99.62 | 290.67 | 191.05 | 0 |
| RQ2 | Testes falhando (nº) | sem-ia | 3 | 0 | 0 | 0 | 0 | 0 |
| RQ2 | Testes falhando (nº) | com-ia | 9 | 0 | 0 | 0 | 0 | 0 |
| RQ3 | Complexidade ciclomática média/método | sem-ia | 0 | — | — | — | — | 0 |
| RQ3 | Complexidade ciclomática média/método | com-ia | 6 | 6.50 | 5.00 | 7.00 | 2.00 | 1 |
| RQ3 | Duplicação de linhas (%) | sem-ia | 0 | — | — | — | — | 0 |
| RQ3 | Duplicação de linhas (%) | com-ia | 6 | 0 | 0 | 0 | 0 | 0 |
| RQ3 | LOC (código do participante) | sem-ia | 0 | — | — | — | — | 0 |
| RQ3 | LOC (código do participante) | com-ia | 6 | 26 | 22.25 | 35 | 12.75 | 0 |

**Outlier identificado** (RQ3, complexidade, com-ia): o trial
`joaquim_vilela_kata-05_com-ia` tem complexidade média 13, fora da cerca `[2, 10]`. É o
kata-05 (Mascarador de Contatos), com solução de método único e muitas ramificações de
validação; o valor deve ser considerado na leitura de RQ3 e na decisão de tratamento de
outliers (Issue #64).

## Lacunas de dados (afetam a interpretação)

Estes vazios **não** são resultados nulos; são dados ainda não coletados. Precisam ser
preenchidos antes da análise inferencial (Issue #32) e da leitura final de RQ3.

1. **Tratamento `sem-ia` incompleto.** Só há trials `sem-ia` do participante A (Gabriel).
   Joaquim e Vitor ainda não executaram seus trials `sem-ia` (Issues #44/#46/#48 e
   #56/#59/#60). Sem eles não há pares `com-ia`/`sem-ia` por participante para o Wilcoxon.
2. **Métricas estruturais parciais.** Há `metrics.json` para 6 dos 12 trials, todos
   `com-ia`. Faltam as métricas dos 6 trials do participante A (Issue #63) e de todos os
   trials `sem-ia`. Por isso as linhas de RQ3 em `sem-ia` aparecem com `n = 0`.

Enquanto as lacunas existirem, a comparação descritiva entre tratamentos para RQ3 não é
possível, e a de RQ1/RQ2 fica limitada ao desbalanceamento 3 (`sem-ia`) × 9 (`com-ia`).

## Limitações

Com três participantes e o desenho within-subject, a leitura é exploratória (§7, §8.6).
Os 12 (futuros 18) trials não devem ser tratados como observações independentes; a
agregação por participante e o tratamento de censura seguem o protocolo da Issue #30.
