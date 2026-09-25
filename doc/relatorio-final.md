# Relatório Final — LAB02: IA vs. codificação manual

Estudo experimental within-subject comparando a resolução de katas de programação em
Java **com** e **sem** assistente de IA (Claude), medindo tempo, qualidade funcional e
métricas estruturais do código produzido.

> Estrutura conforme o Passo 5 do [enunciado](enunciado.md): (i) introdução com as
> hipóteses; (ii) metodologia reprodutível; (iii) resultados por RQ; (iv) discussão
> final; (v) link do repositório/GitHub Projects. Este documento é montado em partes por
> issue: **§1 (Issue #37)**, §2 (#38), §3 (#39), §4 (#40) e §5 (#41).

## 1. Introdução e hipóteses

### 1.1 Contexto e objetivo

Assistentes de IA baseados em modelos de linguagem passaram a fazer parte do fluxo de
programação, com a promessa de acelerar a escrita de código e reduzir defeitos. Resta a
questão empírica de **quanto**, e a **que custo** em qualidade estrutural, esse ganho se
concretiza em tarefas curtas e bem delimitadas. Este experimento investiga o efeito do
uso de um assistente de IA (Claude, Sonnet 5, esforço High) na resolução de **katas** de
Java 21 sob time-box de 35 minutos, num desenho **within-subject (crossover)** com três
participantes, cada um resolvendo seis katas — metade com IA, metade sem — em ordem
contrabalanceada (ver [doc/decisoes.md](decisoes.md) §4).

O objetivo, seguindo a abordagem **GQM**, é responder a três questões de pesquisa sobre o
efeito do tratamento (uso ou não do assistente de IA) em três dimensões: **tempo**,
**qualidade funcional** e **estrutura do código**.

### 1.2 Variáveis

- **Variável independente (tratamento):** uso do assistente de IA — dois níveis,
  `com-ia` e `sem-ia`.
- **Variáveis dependentes:**
  - Tempo até passar nos testes de aceitação (*time-to-green*), em segundos.
  - Número de testes de aceitação passando/falhando ao final do trial.
  - Métricas estruturais: complexidade ciclomática média por método, percentual de
    linhas duplicadas e LOC (métrica de controle).
- **Controles:** mesmo conjunto de katas e testes para todos; mesmo ambiente Docker
  (versões fixadas); mesmo assistente, modelo e configuração; time-box fixo de 35 min;
  ordem de tratamento contrabalanceada entre participantes.

### 1.3 Questões de pesquisa e hipóteses

As hipóteses conceituais foram definidas no desenho do experimento
([decisoes.md](decisoes.md) §6). RQ1 e RQ2 têm hipóteses **direcionais** (esperamos que a
IA reduza tempo e defeitos); RQ3 tem hipóteses **não direcionais** (investigamos se há
diferença estrutural, sem prever o sentido).

**RQ1 — Tempo.** O uso do assistente de IA reduz o tempo até passar nos testes de
aceitação?

- **H1₀:** o uso de IA **não reduz** o tempo até verde (mediana com-ia ≥ mediana sem-ia).
- **H1₁:** o uso de IA **reduz** o tempo até verde (mediana com-ia < mediana sem-ia).

**RQ2 — Qualidade funcional.** O uso do assistente de IA reduz a proporção de testes de
aceitação falhando ao final do trial?

- **H2₀:** o uso de IA **não reduz** o número de testes falhando.
- **H2₁:** o uso de IA **reduz** o número de testes falhando.

**RQ3 — Estrutura do código.** O uso do assistente de IA altera as métricas estruturais
do código produzido (complexidade ciclomática, duplicação, LOC)?

- **H3₀:** **não há diferença** entre tratamentos na métrica estrutural considerada.
- **H3₁:** **há diferença** entre tratamentos na métrica estrutural considerada.

RQ3 é avaliada por métrica (complexidade, duplicação e LOC), cada uma com seu par
H₀/H₁. LOC é interpretada como métrica de **controle** para leitura de complexidade e
duplicação, não como desfecho de qualidade em si.

### 1.4 Análise e limitações previstas

As hipóteses são testadas com o **teste de Wilcoxon pareado** sobre valores agregados por
participante (unilateral para RQ1/RQ2, bilateral para RQ3; α = 0,05), conforme o
[protocolo estatístico](protocolo-estatistico.md) (Issue #30). Com **três participantes**,
o poder estatístico é muito baixo e os resultados têm caráter **exploratório**: ausência
de significância não será interpretada como equivalência entre os tratamentos (§4 e
[decisoes.md](decisoes.md) §7–§8).

## 2. Metodologia

> A preencher — Issue #38 (ambiente, katas usados, assistente de IA e versão, protocolo
> experimental, com detalhe suficiente para reprodução/replicação).

## 3. Resultados por questão de pesquisa

Base de dados: **18 trials oficiais** (3 participantes × 6 katas), todos `completed` e com
8/8 testes passando, com métricas estruturais coletadas. A análise segue o
[protocolo estatístico](protocolo-estatistico.md) (Issue #30): agregação por **mediana**
dos 3 trials de cada participante × tratamento (**n = 3 pares**) e **Wilcoxon pareado**
(unilateral para RQ1/RQ2, bilateral para RQ3; α = 0,05). Detalhes e reprodução em
[rq1-rq2.md](rq1-rq2.md) (Issue #32), [rq3.md](rq3.md) (Issue #33),
[descritiva.md](descritiva.md) (Issue #31) e [outliers.md](outliers.md) (Issue #64).

**Nota sobre poder estatístico.** Com n = 3 pares, o menor p-valor alcançável é **0,125**
(unilateral, RQ1/RQ2) e **0,25** (bilateral, RQ3). Logo, **nenhum** resultado consegue ser
significativo a α = 0,05 neste desenho: os testes são reportados por rigor de protocolo, e
a leitura se apoia na direção/magnitude dos pares e na descritiva
([limitacao-inferencial.md](limitacao-inferencial.md), Issue #35). Não houve trials
censurados nem interrompidos; nenhum outlier foi descartado (Issue #64).

### 3.1 RQ1 — Tempo até verde

| Participante | sem-ia (s) | com-ia (s) | Diferença (com − sem) |
|---|---|---|---|
| gabriel | 238,71 | 183,16 | −55,55 |
| joaquim_vilela | 999,05 | 290,67 | −708,38 |
| vitor | 1163,67 | 99,62 | −1064,05 |

**Wilcoxon pareado unilateral (H₁: IA reduz):** W = 0, **p = 0,125**, r_rb = **−1,00**,
mediana das diferenças = **−708,38 s**. Não rejeita H1₀ a α = 0,05.

Os **três** participantes foram mais rápidos com IA (direção 100% consistente, efeito
máximo r = −1,00). O p = 0,125 é o mínimo possível com n = 3 unilateral — ou seja, há uma
**tendência forte e uniforme** de redução de tempo, sem poder para confirmá-la
estatisticamente. A magnitude cresce com a dificuldade do kata: nos katas mais longos sem
IA (kata-04 e kata-06, medianas > 1170 s), o tratamento com IA cai para 180–240 s. A única
inversão pontual é o kata-01 (curto), em que o tempo com IA ficou acima do sem-ia.

### 3.2 RQ2 — Testes falhando

Todos os 18 trials terminaram com **8/8 testes passando** (0 falhando) nos dois
tratamentos. As três diferenças pareadas são zero, todos os pares são descartados e o
**teste não é aplicável**. A qualidade funcional foi **máxima** em ambas as condições
dentro do time-box; a métrica **não discrimina** neste experimento — a diferença entre
tratamentos apareceu no tempo (RQ1), não no acerto final.

### 3.3 RQ3 — Estrutura do código

| Métrica | Participante | sem-ia | com-ia | Diferença |
|---|---|---|---|---|
| Complexidade média/método (RQ3a) | gabriel | 6,67 | 11,00 | +4,33 |
| | joaquim_vilela | 11,00 | 7,00 | −4,00 |
| | vitor | 10,00 | 4,67 | −5,33 |
| LOC — controle (RQ3c) | gabriel | 24 | 70 | +46 |
| | joaquim_vilela | 59 | 26 | −33 |
| | vitor | 40 | 26 | −14 |

**Testes (Wilcoxon pareado bilateral):**

| RQ | Métrica | Pares (efetivos) | Mediana das dif. | W | p | r_rb | Decisão |
|---|---|---|---|---|---|---|---|
| RQ3a | Complexidade média/método | 3 (3) | −4,00 | 2 | 0,75 | −0,33 | Não rejeita H₀ |
| RQ3b | Duplicação (%) | 3 (0) | 0 | — | — | — | Não aplicável |
| RQ3c | LOC (controle) | 3 (3) | −14 | 3 | 1,00 | 0,00 | Não rejeita H₀ |

- **Complexidade (RQ3a):** sem direção consistente — Joaquim e Vitor produziram código
  **menos** complexo com IA; Gabriel, **mais**. Efeito fraco (r = −0,33), p = 0,75.
- **Duplicação (RQ3b):** o CPD não detectou duplicação em **nenhum** trial (0% em todos);
  a métrica não varia neste conjunto de katas curtos e não discrimina.
- **LOC (RQ3c, controle):** acompanha a complexidade — Gabriel escreveu mais código com
  IA (+46), os outros dois menos, indicando que a variação de complexidade está ligada ao
  tamanho da solução de cada participante, não a um efeito isolado do tratamento.

Os três outliers identificados (todos no kata-06, o mais complexo) foram mantidos, sem
afetar a leitura (Issue #64).

### 3.4 Síntese

| RQ | Resultado | Direção | Significância (α = 0,05) |
|---|---|---|---|
| RQ1 — Tempo | IA reduz o tempo nos 3 participantes (mediana −708 s) | Consistente com H₁ | Não significativo (p = 0,125; piso do n=3) |
| RQ2 — Defeitos | 8/8 em todos os trials nos dois tratamentos | Sem variância | Teste não aplicável |
| RQ3 — Estrutura | Sem diferença consistente; duplicação sempre 0% | Não direcional | Não significativo / não aplicável |

O achado central é de **RQ1**: uma redução de tempo forte e uniforme com IA, que o
desenho de três participantes descreve mas não confirma estatisticamente. RQ2 e RQ3 não
distinguem os tratamentos com os katas e o instrumento usados.

## 4. Discussão final

> A preencher — Issue #40 (achados, limitações e ameaças à validade à luz dos resultados).

## 5. Repositório e GitHub Projects

> A preencher — Issue #41 (link do repositório e do GitHub Projects do grupo).
