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

> A preencher — Issue #39 (resultados de RQ1, RQ2 e RQ3 com as respostas estatísticas
> obtidas). Base: [estatística descritiva](descritiva.md) (Issue #31) e testes de
> Wilcoxon (Issue #32).

## 4. Discussão final

> A preencher — Issue #40 (achados, limitações e ameaças à validade à luz dos resultados).

## 5. Repositório e GitHub Projects

> A preencher — Issue #41 (link do repositório e do GitHub Projects do grupo).
