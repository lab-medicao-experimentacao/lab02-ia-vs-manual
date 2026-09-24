# LAB02 — Identificação e tratamento de outliers (Issue #64)

Revisão dos dados coletados e identificação de outliers **antes** dos testes estatísticos,
conforme o Passo 4 da sprint. Registra o critério, os outliers encontrados e a decisão de
tratamento, para que a análise (Issues #32, #33, #39) seja reproduzível e auditável.

## Como reproduzir

```bash
docker compose run --rm lab python scripts/outliers.py
```

Entrada: `results/consolidado.csv`. Saída: `results/outliers.csv` (uma linha por outlier)
e a tabela de cercas no terminal.

## Critério

Regra de **Tukey (1.5×IQR)**, aplicada por **métrica × tratamento** sobre os trials
individuais: é outlier o valor abaixo de `Q1 − 1.5·IQR` ou acima de `Q3 + 1.5·IQR`. É a
mesma regra da estatística descritiva (`scripts/descriptive_stats.py`, Issue #31) e do
protocolo ([protocolo-estatistico.md](protocolo-estatistico.md) §5). A elegibilidade por
métrica segue o protocolo §3–§4 (RQ1 só `completed`; RQ2 com avaliação válida; RQ3 com
`metrics.json`).

## Outliers identificados (18 trials, 9 por tratamento)

Três outliers, **todos no kata-06** (Encadeador de Trechos):

| RQ | Métrica | Tratamento | Trial | Valor | Cerca |
|---|---|---|---|---|---|
| RQ3a | Complexidade média/método | sem-ia | joaquim_vilela/kata-06 | 18 | [1, 17] |
| RQ3a | Complexidade média/método | com-ia | gabriel/kata-06 | 23 | [−1,5, 18,5] |
| RQ3c | LOC (controle) | com-ia | gabriel/kata-06 | 79 | [−2,5, 73,5] |

RQ1 (tempo) e RQ2 (defeitos) não apresentaram outliers. RQ3b (duplicação) é 0% em todos
os trials, sem dispersão.

## Interpretação e decisão de tratamento

Os três outliers concentram-se no **kata-06**, o mais complexo do conjunto (encadeamento
por chave + detecção de ciclo). São valores **substantivamente plausíveis**: soluções de
classe única com muitas ramificações elevam naturalmente a complexidade ciclomática e a
LOC. Não há indício de erro de medição, ocorrência técnica ou trial inválido — as
contagens vêm do PMD sobre o código final preservado, e todos os trials estão
`completed` com 8/8 testes.

**Decisão: manter todos os 18 trials, sem descarte** (protocolo §5;
[decisoes.md](decisoes.md) §7 — "sem descarte automático"). Justificativas:

1. Os outliers refletem a dificuldade real do kata-06, não ruído.
2. Com n = 3 pares por métrica, remover observações agravaria ainda mais o baixo poder
   ([limitacao-inferencial.md](limitacao-inferencial.md)).
3. O teste adotado (Wilcoxon pareado sobre medianas por participante) já é robusto a
   valores extremos: a agregação por mediana amortece o efeito de um trial atípico entre
   os três de um participante.

Os outliers são apenas **sinalizados** para leitura cuidadosa dos resultados de RQ3; se
alguma análise futura optar por excluí-los, a exclusão e sua justificativa devem ser
registradas neste documento.
