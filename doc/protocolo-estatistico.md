# LAB02 — Protocolo estatístico (Issue #30)

Formalização do protocolo analítico **antes da coleta/análise final**, para que as
decisões estatísticas não sejam influenciadas pelos resultados. Detalha o que os §6 e §7
de [doc/decisoes.md](decisoes.md) definem em nível de planejamento: tratamento de
censura, agregação dos trials por participante, nível de significância e critérios dos
testes. É a referência para a estatística descritiva (Issue #31) e para os testes de
hipótese (Issue #32).

## 1. Desenho e unidade de análise

- Desenho **within-subject (crossover)**, 3 participantes × 6 katas, com ordem
  contrabalanceada e distribuição de tratamento 2:1 por kata (decisoes.md §4).
- Total planejado: **18 trials** (3 por tratamento por participante).
- **Unidade de análise = participante**, não o trial. Os 18 trials **não** são tratados
  como 18 observações independentes (decisoes.md §7, §8.6). Cada participante contribui
  com um par (com-ia, sem-ia) de valores agregados por métrica.

## 2. Agregação por participante e tratamento

Cada participante tem 3 trials `com-ia` e 3 `sem-ia`. Antes de qualquer teste pareado,
os 3 trials de um mesmo tratamento são resumidos em **um único valor por participante**,
por métrica:

- **Estatística de agregação: mediana** dos 3 trials do tratamento. A mediana é robusta a
  um trial atípico entre os três e é coerente com o uso de mediana/IQR na descritiva (§7).
- A agregação produz, por participante, um par `(mediana_sem_ia, mediana_com_ia)` para
  cada métrica de RQ1, RQ2 e RQ3.
- O teste pareado (Issue #32) opera sobre esses pares agregados — logo, **n = 3 pares**
  (um por participante), não 9 ou 18.

Justificativa: agregar antes de testar preserva a independência entre unidades exigida
pelo Wilcoxon pareado (as 3 medidas repetidas de um participante não são independentes
entre si) e mantém a leitura within-subject.

## 3. Tratamento de censura e ocorrências técnicas

Estados possíveis de um trial: `completed`, `censored` (35 min sem sucesso),
`interrupted` (ocorrência técnica) e `running` (encerramento abrupto). Regras:

- **RQ1 (tempo).** `time_to_green_seconds` existe **somente** para trials `completed`.
  Um trial `censored` **não** tem tempo de conclusão e **nunca** é lançado como 2100 s
  "de conclusão" (decisoes.md §5, §7).
  - Na **descritiva**, os censurados são reportados à parte (contagem de concluídos vs.
    censurados por tratamento), sem entrar na mediana/IQR do tempo.
  - Na **agregação por participante** para o teste de tempo, se um tratamento de um
    participante contiver trials censurados, isso é registrado e a comparação de tempo
    daquele par é marcada como afetada por censura. O Wilcoxon comum não trata censura
    diretamente (§7); portanto, quando houver censura, a comparação de tempo será
    **descritiva/qualitativa** para o(s) par(es) afetado(s), e o teste será aplicado
    apenas se todos os pares forem de trials concluídos. Qualquer exclusão é declarada.
- **RQ2 (defeitos).** Mesmo censurado, o código final é avaliado e produz contagem de
  testes falhando (`failed`). Logo, RQ2 usa **todos** os trials com avaliação final
  válida (`total > 0`), inclusive censurados. Trials sem relatório válido têm contagem
  **nula** (não zero) e são excluídos daquela métrica, com o motivo registrado.
- **RQ3 (estrutura).** Métricas calculadas sobre o código final preservado, exista ou
  não sucesso; portanto censurados entram normalmente, desde que haja `metrics.json`.
- **`interrupted` / `running`.** Ocorrências técnicas são preservadas e **excluídas** das
  comparações, documentadas caso a caso (decisoes.md §5, §9). Não são substituídas nem
  repetidas automaticamente.

## 4. Métricas por questão de pesquisa

| RQ | Métrica | Fonte | Direção da hipótese |
|---|---|---|---|
| RQ1 | Tempo até verde (s) | `time_to_green_seconds` (só `completed`) | Direcional (H₁: IA reduz o tempo) |
| RQ2 | Nº de testes falhando ao final | `final_evaluation.tests.failed` | Direcional (H₁: IA reduz defeitos) |
| RQ3a | Complexidade ciclomática média/método | `metrics.json → complexity.average` | Não direcional |
| RQ3b | Duplicação de linhas (%) | `metrics.json → duplication.percent` | Não direcional |
| RQ3c | LOC (controle) | `metrics.json → loc.total` | Não direcional |

Hipóteses conceituais conforme decisoes.md §6. LOC é métrica de **controle** para
interpretar complexidade e duplicação, não um desfecho de qualidade em si.

## 5. Estatística descritiva

- **Mediana e IQR (Q1–Q3) por tratamento** para todas as métricas (Issue #31).
- Identificação de **outliers** pela regra de Tukey (fora de `[Q1 − 1.5·IQR, Q3 + 1.5·IQR]`),
  reportados por métrica e tratamento — sem descarte automático; a decisão de tratamento
  de outliers é registrada (Issue #64).
- Contagem de censura por tratamento (concluídos / censurados / interrompidos).

## 6. Testes de hipótese (Issue #32)

- **Teste:** Wilcoxon dos postos sinalizados **pareado**, sobre os pares agregados por
  participante (§2). Escolha não paramétrica coerente com o desenho within-subject e o n
  pequeno (decisoes.md §7).
- **Direcionalidade:**
  - RQ1 e RQ2 — hipóteses **direcionais** ⇒ teste **unilateral** (H₁: IA reduz
    tempo/defeitos).
  - RQ3 (todas as métricas) — hipóteses **não direcionais** ⇒ teste **bilateral**.
- **Nível de significância:** α = **0,05**.
- **Pares nulos (diferença zero):** tratados pelo método padrão do Wilcoxon (pares com
  diferença zero são descartados antes do cálculo dos postos); o número de pares
  descartados é reportado.
- **Estatística e reporte:** reportar a estatística do teste, o p-valor, o n de pares
  efetivos, a mediana das diferenças e uma medida de tamanho de efeito quando aplicável.
- **Empates de postos:** usar a correção padrão para empates da implementação
  (`scipy.stats.wilcoxon`), declarando a versão.

## 7. Limitações inferenciais (resumo; detalhe na Issue #35)

- Com **3 participantes**, o Wilcoxon pareado tem **n = 3 pares** por métrica — poder
  estatístico muito baixo. Resultados são **exploratórios**.
- **Ausência de significância não é equivalência** entre tratamentos (decisoes.md §7, §8.6).
- O contrabalanceamento não é completo (2:1 por kata), então efeito de aprendizado não é
  totalmente neutralizado (decisoes.md §8.3).
- A censura reduz ainda mais os pares utilizáveis em RQ1 quando presente.

## 8. Ferramentas e reprodutibilidade

- Cálculos em Python: `pandas`/`numpy` para descritiva (`scripts/descriptive_stats.py`) e
  `scipy.stats.wilcoxon` para os testes (Issue #32).
- Entradas: `results/consolidado.csv` (via `scripts/trial.py export`) e os
  `results/<trial_id>/metrics.json` (via `scripts/metrics.py`).
- Versões das bibliotecas serão registradas junto aos resultados para permitir replicação
  (decisoes.md §11; metodologia na Issue #38).

## 9. Pré-condições de dados

O protocolo só produz resultados finais quando os **18 trials** estiverem coletados e com
métricas. Enquanto houver lacunas (trials `sem-ia` pendentes — Issues #44/#46/#48 e
#56/#59/#60 — e `metrics.json` faltantes — Issue #63), a análise é parcial: a descritiva
roda sobre o disponível e os testes pareados ficam suspensos até existir, para cada
participante, o par completo (com-ia, sem-ia) da métrica.
