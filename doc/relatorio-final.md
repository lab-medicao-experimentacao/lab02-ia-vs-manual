# Relatório de Laboratório

**Laboratório de Experimentação de Software**

| | |
|---|---|
| **Curso** | Engenharia de Software |
| **Disciplina** | Laboratório de Experimentação de Software |
| **Turno / Período** | Noite / 6º |
| **Professor(a)** | Danilo Maia |
| **Laboratório** | Lab02 — IA vs. codificação manual |
| **Grupo (trio)** | Joaquim Guilherme de Carvalho Vilela Silva · Vitor Costa Vianna · Gabriel Nogueira Vieira Resende |
| **Link do repositório / GitHub Projects** | https://github.com/lab-medicao-experimentacao/lab02-ia-vs-manual |
| **Data de entrega** | 24/09/2026 |

---

## 1. Introdução

Assistentes de IA baseados em modelos de linguagem se tornaram parte do fluxo diário de
programação, com a promessa de acelerar a escrita de código e reduzir defeitos. Falta,
porém, evidência **controlada** sobre o real impacto dessas ferramentas: quanto elas
aceleram a resolução de uma tarefa e a que custo em qualidade estrutural do código. Este
laboratório investiga esse impacto num experimento **crossover within-subject**, em que
três participantes resolvem seis katas de Java 21 sob time-box de 35 minutos — metade
**com** assistente de IA (Claude), metade **sem** — em ordem contrabalanceada.

Seguindo a abordagem **GQM**, o estudo responde às três Questões de Pesquisa do enunciado:

- **RQ1 — Tempo.** O uso de assistente de IA reduz o tempo necessário para resolver uma
  tarefa de programação?
- **RQ2 — Defeitos.** O uso de assistente de IA reduz a quantidade de defeitos (testes que
  falham) no código produzido?
- **RQ3 — Estrutura.** O uso de assistente de IA altera a complexidade ciclomática ou a
  duplicação do código produzido?

**Hipóteses informais do grupo (antes da coleta):**

- **RQ1:** esperávamos que a IA **reduzisse** o tempo (hipótese direcional H1₁).
- **RQ2:** esperávamos que a IA **reduzisse** os testes falhando (hipótese direcional H2₁).
- **RQ3:** sem expectativa de direção — apenas verificar se **há diferença** estrutural
  (hipótese não direcional H3₁), com LOC como métrica de controle.

**Contribuições próprias do grupo (30% de inovação), detalhadas na Metodologia §3.6:**

- (a) **Métrica de tamanho de efeito** (rank-biserial pareado) além do p-valor exigido.
- (b) **Análise explícita da resolução do teste** para n = 3, mostrando o p-valor mínimo
  alcançável e suas consequências de interpretação.
- (c) **Infraestrutura própria de cronometragem e captura** em Docker (relógio monotônico,
  preservação de código no limite), garantindo comparabilidade entre trials.

## 2. Contexto

Este é o **Lab02** da disciplina, com desenho experimental controlado. Foi conduzido em três sprints: **S01** (desenho do experimento, seleção e
validação dos katas, ambiente e scripts), **S02** (execução dos 18 trials oficiais) e
**S03** (análise estatística, dashboard e este relatório).

O **objeto de estudo** é o processo de resolução de katas de programação, comparando dois
tratamentos: `com-ia` (Claude, Sonnet 5, esforço High, acessado pelo navegador) e
`sem-ia` (assistentes de IA desativados). Cada participante resolve os seis katas uma vez,
três por tratamento, sob time-box fixo de **35 minutos** por trial. Os katas são
**autorais e de baixa indexação**, para reduzir o risco de a IA reproduzir uma solução
memorizada em vez de auxiliar de fato.

**Base conceitual:** o método **GQM** (Basili, Caldiera & Rombach) estrutura a ligação
entre objetivo, questões (RQ1–RQ3) e métricas; a complexidade ciclomática segue a
definição de **McCabe**; a análise estatística usa o teste **de Wilcoxon dos postos
sinalizados** para amostras pareadas, coerente com o desenho within-subject.

## 3. Metodologia

### 3.1 Principais Desafios

- **Padronizar katas de dificuldade equivalente e evitar memorização pela IA.** Foi o
  desafio central de desenho: katas muito conhecidos (LeetCode/HackerRank) permitiriam à
  IA reproduzir soluções prontas, inflando o efeito do tratamento. Resolvemos com seis
  katas **autorais**, com regras e contratos de I/O próprios, mesmo quando a ideia
  subjacente é conhecida (ex.: run-length no kata-03 com regra própria).
- **Capturar o código exatamente no limite de tempo** sem contar uma execução posterior
  como conclusão dentro do prazo. Exigiu um cronômetro com relógio monotônico que preserva
  o código ao atingir 35 min e avalia a cópia final separadamente.
- **Poder estatístico com apenas 3 participantes.** O desenho de três participantes impõe
  n = 3 pares no teste pareado; enfrentamos isso definindo um protocolo estatístico
  explícito (§3.2) e assumindo o caráter exploratório dos resultados.
- **Integrar dados heterogêneos** (tempos/testes do cronômetro + métricas estruturais do
  PMD/CPD) num único CSV consolidado para análise reprodutível.

### 3.2 Tomadas de Decisão

- **Assistente de IA:** Claude (Sonnet 5, esforço High), acessado pelo navegador,
  disponível no plano gratuito para os três integrantes. Mesmo modelo, configuração e
  **prompt inicial padronizado** em todos os trials com IA; nova conversa por trial, sem
  histórico. Escolha por padronização e comparabilidade.
- **Linguagem Java 21 + PMD/CPD:** os katas são em Java para permitir métricas estáticas
  com CK/PMD (CK exige Java); usamos **PMD** para complexidade e **CPD** para duplicação.
- **Time-box de 35 min, fixo:** conforme o enunciado (só pode ser reduzido, nunca
  aumentado). Mantivemos os 35 min em todos os trials para comparabilidade máxima.
- **Métrica de defeitos:** número de testes falhando ao final (e taxa de sucesso), sobre
  suites de 8 testes de aceitação idênticas para todos no mesmo kata.
- **Estatística com mediana/IQR e Wilcoxon pareado:** dado o n pequeno, preferimos mediana
  e IQR à média/desvio, e o teste não paramétrico de Wilcoxon, coerente com o desenho.
  **Agregação:** a mediana dos 3 trials de cada participante × tratamento forma um par, de
  modo que a **unidade de análise é o participante** (n = 3 pares), não o trial.
- **Tratamento de outliers:** identificados pela regra de Tukey (1.5×IQR), mas **mantidos
  sem descarte** — são valores plausíveis dos katas mais difíceis, e remover agravaria o
  baixo poder.
- **Configuração do processo (WIP):** board no GitHub Projects (v2) com o fluxo
  Backlog → To Do → Doing → Review → Done e **limite de WIP = 3** na coluna Doing (um item
  ativo por integrante), evitando trabalho em paralelo excessivo num trio.

### 3.3 Etapas

O trabalho seguiu três sprints; a divisão reflete os *Assignees* reais das Issues no
GitHub Projects (não apenas narrativa).

| Sprint | Entregas | Responsável(is) | Issues (nº) |
|---|---|---|---|
| S01 — Desenho | Decisões do experimento, seleção/validação dos 6 katas, ameaças à validade | Gabriel (katas, hipóteses, ameaças); Joaquim (cronômetro); Vitor (Docker/métricas) | #3–#21 |
| S02 — Execução | 18 trials oficiais (9 com-ia + 9 sem-ia), perguntas.md, métricas | Cada integrante executa seus trials | #43–#60, #63, #70 |
| S03 — Análise | Protocolo estatístico, descritiva, Wilcoxon RQ1/RQ2 e RQ3, outliers, dashboard, relatório | Gabriel (#30/#31/#32/#35/#37/#39/#40/#64); Vitor (#33/#34/#36/#65); Joaquim (#38/#41/#61/#62) | #30–#41, #61–#65 |

**Configuração do processo.** Colunas do board: Backlog → To Do → Doing → Review → Done;
limite de WIP = 3 em Doing. Cada trial oficial tem uma Issue individual atribuída ao
responsável, e os commits referenciam a Issue correspondente.

> _Sugestão de anexo: inserir aqui o print do quadro Kanban (GitHub Projects) ao final do
> laboratório, mostrando o fluxo real de trabalho._

### 3.4 Ferramentas

- **Java 21 (Temurin 21.0.7) + Maven 3.9.9 + JUnit 5.13.4** — implementação e testes de
  aceitação dos katas.
- **Docker + Docker Compose** — ambiente padronizado com versões fixadas por digest,
  garantindo reprodutibilidade da compilação, testes e coleta.
- **Python 3.12** com scripts próprios do grupo:
  - `scripts/trial.py` — cronômetro (relógio monotônico), execução dos testes e export CSV.
  - `scripts/metrics.py` — coleta de métricas estruturais.
  - `scripts/dataset.py` — carga/união do CSV num DataFrame de análise.
  - `scripts/descriptive_stats.py`, `scripts/rq1_rq2.py`, `scripts/rq3.py`,
    `scripts/outliers.py`, `scripts/dashboard.py` — análise e visualização.
- **PMD / CPD 7.17.0** — complexidade ciclomática (regra `CyclomaticComplexity`) e
  duplicação (`cpd --minimum-tokens 50`).
- **pandas 2.2.3, numpy 2.1.3, scipy 1.14.1** — manipulação e testes estatísticos
  (`scipy.stats.wilcoxon`, `method="exact"`); **matplotlib 3.9.2 / seaborn 0.13.2** —
  gráficos do dashboard.
- **GitHub Projects (v2)** — ferramenta de processo (board do grupo, link na capa).

### 3.5 Tabela de Métricas

| RQ | Métrica | Definição operacional | Unidade | Ferramenta / Fonte |
|---|---|---|---|---|
| RQ1 | Tempo até verde | Tempo (relógio monotônico) do início do trial até todos os testes passarem, se dentro do time-box | Segundos | `scripts/trial.py` |
| RQ2 | Testes falhando | Nº de testes de aceitação com falha/erro na avaliação final (total − passando) | Contagem | JUnit/Surefire via `trial.py` |
| RQ2 | Taxa de sucesso | Testes passando ÷ total × 100 | % | JUnit/Surefire via `trial.py` |
| RQ3a | Complexidade ciclomática média/método | Média aritmética da complexidade (McCabe) por método reportada pelo PMD | — | PMD 7.17.0 (`CyclomaticComplexity`) |
| RQ3b | Duplicação de linhas | Linhas duplicadas (CPD, ≥ 50 tokens, sem sobreposição) ÷ LOC × 100 | % | CPD 7.17.0 |
| RQ3c | LOC (controle) | Linhas de código não vazias/não comentário em `src/main/java` | Contagem | `scripts/metrics.py` |

### 3.6 Inovações Propostas pelo Grupo (30% da nota)

- **(a) Tamanho de efeito (rank-biserial pareado).** Além do p-valor exigido, cada teste
  reporta `r = (W⁺ − W⁻)/(W⁺ + W⁻)`, de −1 a +1. Isso permite descrever a **magnitude e a
  direção** do efeito mesmo quando o p-valor não é significativo — essencial neste
  experimento, em que o poder é baixo. **Onde aparece:** §4.3 (RQ1 com r = −1,00).
- **(b) Análise da resolução do teste para n = 3.** Demonstramos, com verificação
  numérica, que o menor p-valor alcançável é **0,125** (unilateral) e **0,25** (bilateral)
  com três pares — logo, nenhum resultado pode ser significativo a α = 0,05 neste desenho.
  Isso reposiciona a leitura: os testes são reportados por rigor, mas a conclusão se apoia
  na direção dos pares e na descritiva. **Onde aparece:** §4.3 e §5, documentado em
  `doc/limitacao-inferencial.md`.
- **(c) Infraestrutura própria de cronometragem e captura em Docker.** Em vez de
  cronometrar manualmente, construímos um cronômetro com relógio monotônico que executa os
  testes pelo Maven, detecta o "verde", encerra a edição no limite e preserva o código
  final para avaliação separada — controlando a ameaça de contar uma execução tardia como
  conclusão no prazo. **Onde aparece:** confiabilidade dos tempos de RQ1 em §4.

## 4. Resultados

### 4.1 Coleta de Dados

Foram concluídos os **18 trials oficiais** planejados (3 participantes × 6 katas, 9 por
tratamento). **Todos** terminaram com estado `completed`, dentro do time-box de 35 min —
nenhum censurado (esgotamento do tempo) e nenhum interrompido por ocorrência técnica.
Todos os 18 trials passaram **8/8** testes de aceitação. As métricas estruturais foram
coletadas para os 18 trials sobre o código final preservado.

**Outliers.** Pela regra de Tukey (1.5×IQR), foram identificados **3 outliers**, todos no
**kata-06** (o mais complexo, com detecção de ciclo): complexidade de 18 (Joaquim, sem-ia)
e 23 (Gabriel, com-ia) e LOC de 79 (Gabriel, com-ia). São valores plausíveis do problema,
não erros de medição; foram **mantidos**, sem descarte (documentado em `doc/outliers.md`).

### 4.2 Visualização Gráfica

Os gráficos abaixo são gerados por `scripts/dashboard.py` (dashboard completo em
`doc/dashboard/index.html`). Como há n pequeno e distribuição assimétrica, usa-se
**mediana** como tendência central.

**RQ1 — O uso de IA reduz o tempo de resolução?**

![Tempo por participante e tratamento](dashboard/tempo_participante.png)

Pontos conectados (before/after) por participante: os três reduzem o tempo com IA. As
medianas por participante caem de 238,7 → 183,2 s (Gabriel), 999,1 → 290,7 s (Joaquim) e
1163,7 → 99,6 s (Vitor).

![Tempo por kata e tratamento](dashboard/tempo_kata.png)

Por kata, a vantagem da IA é maior nos exercícios mais longos (kata-04 e kata-06); no
kata-01, o mais curto, o tempo com IA foi maior (mediana de ~213 s contra ~96 s sem IA).

**RQ2 — O uso de IA reduz os defeitos?**

Não há variação a exibir em defeitos: a **taxa de sucesso foi 100% (8/8) em todos os 18
trials**, nos dois tratamentos, por isso não há gráfico para RQ2 (o dashboard mostra uma
nota no lugar do gráfico vazio).

**RQ3 — O uso de IA altera a estrutura do código?**

![Métricas estruturais por tratamento](dashboard/estrutura.png)

Complexidade e LOC não têm direção consistente entre tratamentos; a duplicação é 0% em
todos os trials.

### 4.3 Discussão

**RQ1 — Tempo. Hipótese apoiada pela direção dos dados, sem significância estatística.** Os três participantes foram mais
rápidos com IA (diferenças de −55,6 s, −708,4 s e −1064,1 s; mediana −708 s), com direção
100% consistente e tamanho de efeito máximo (rank-biserial = −1,00). O **Wilcoxon pareado
unilateral** deu **W = 0, p = 0,125** — não significativo a α = 0,05. Em linguagem
acessível: *todos* melhoraram com IA e na maior intensidade que o teste consegue captar,
mas com três participantes o p-valor não consegue descer abaixo de 0,125, então a
tendência é **forte e uniforme, porém não confirmável estatisticamente**. A hipótese H1₁
é apoiada pela direção dos dados, sem significância formal.

**RQ2 — Defeitos. Hipótese não testável.** Como todos os trials atingiram 8/8, as
diferenças pareadas são zero e o teste não se aplica. A qualidade funcional foi **máxima**
nos dois tratamentos dentro do time-box; a diferença entre tratar com ou sem IA apareceu
no **tempo** (RQ1), não no acerto final. Não confirma nem refuta H2₁ — a métrica não
discrimina com estes katas.

**RQ3 — Estrutura. Sem diferença consistente.** Complexidade caiu com IA para dois
participantes e subiu para um (p = 0,75); LOC seguiu o mesmo padrão (p = 1,00); duplicação
foi 0% em todos. A variação estrutural reflete mais o estilo/tamanho da solução de cada
participante do que o tratamento. Não se rejeita H3₀ — lembrando que, com n = 3, "sem
diferença detectável" **não** equivale a "equivalência comprovada".

**Ameaças à validade.** (i) *Poder estatístico* — dominante: n = 3 impede significância a
5% (inovação (b)); conclusões exploratórias. (ii) *Efeito de aprendizado e confusão
tratamento/participante* — o contrabalanceamento 2:1 faz o tratamento coincidir com o
participante dentro de cada kata. (iii) *Memorização pela IA* — mitigada por katas
autorais; o ganho concentrado nos katas difíceis é compatível com auxílio genuíno. (iv)
*Exposição de quem preparou os katas* — Gabriel, autor dos katas, foi justamente o de
menor ganho com IA e maior complexidade/LOC com IA, o que deve ser considerado.

**Contribuição das inovações (§3.6).** O tamanho de efeito (a) foi decisivo para mostrar
que RQ1, apesar do p não significativo, tem efeito consistente e máximo; a análise de
resolução do teste (b) explicou *por que* nenhum p seria significativo, evitando a leitura
equivocada de "IA não faz diferença"; a infraestrutura de cronometragem (c) sustenta a
confiabilidade dos tempos que embasam o achado de RQ1.

## 5. Conclusão

O experimento sugere que o assistente de IA **reduz o tempo** de resolução de katas de
Java sob time-box, de forma consistente entre os três participantes e mais acentuada nos
problemas mais difíceis, **sem degradar** a corretude funcional (todos os trials chegaram
a 8/8) e **sem diferença estrutural detectável** (complexidade, duplicação e LOC sem
direção consistente). Não observamos o trade-off "mais rápido, porém pior" — o que, com
n = 3, não equivale a demonstrar que ele não existe.

A principal **limitação** é o tamanho amostral: com três participantes, o teste de
Wilcoxon não alcança significância a 5% em nenhuma RQ (o p mínimo é 0,125 nos testes
unilaterais de RQ1/RQ2 e 0,25 nos bilaterais de RQ3), de modo que
todos os achados são **exploratórios**. Somam-se as ameaças de contrabalanceamento
incompleto (2:1), possível memorização pela IA e a exposição do integrante que preparou os
katas.

**O que faríamos diferente com mais tempo/recursos:** ampliar substancialmente o número de
participantes (ou de réplicas independentes por condição) para obter poder estatístico
real; usar katas maiores, em que duplicação e complexidade tenham variância suficiente
para discriminar; e adotar métricas de qualidade mais sensíveis que a contagem de testes
verdes. Entre as inovações (§3.6), o **tamanho de efeito** e a **análise de poder para n
pequeno** são as que mais valeria expandir — juntas, permitem interpretar corretamente
experimentos com amostras reduzidas, comuns em estudos com participantes humanos.

## Referências

- BASILI, V. R.; CALDIERA, G.; ROMBACH, H. D. *The Goal Question Metric Approach.* 1994.
- McCABE, T. J. *A Complexity Measure.* IEEE Transactions on Software Engineering, 1976.
- WILCOXON, F. *Individual Comparisons by Ranking Methods.* Biometrics Bulletin, v. 1,
  n. 6, p. 80–83, 1945.
- PMD. *PMD Source Code Analyzer — CyclomaticComplexity e CPD (v7).* https://pmd.github.io/
- Vídeo: https://www.youtube.com/shorts/YwnaeO95AN8
