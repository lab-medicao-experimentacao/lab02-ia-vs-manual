# LAB02 — Decisões do experimento

Decisões acordadas pelo grupo durante o planejamento da Sprint 1, com base no [enunciado](enunciado.md). Este documento registra o planejamento; não atesta que o ambiente ou os exercícios já foram implementados e validados.

## 1. Ambiente e organização

| Item | Decisão |
|---|---|
| Linguagem dos katas | Java 21 |
| Build e dependências | Maven |
| Testes de aceitação | JUnit |
| Ambiente de execução | Docker, com versões fixadas de Java, Maven, Python e ferramentas de métricas |
| Cronometragem e coleta | Script Python executado no Docker |
| Organização | Um repositório para o trio; projeto Maven com um módulo por kata |
| Editor | IDE habitual de cada integrante, mantendo a configuração entre seus trials e registrando nome e versão |
| Recursos da IDE | Autocomplete sem IA, indicação de erros, navegação, refatoração e depurador permitidos nos dois tratamentos |

Docker padronizará compilação, testes e coleta, dispensando a instalação local dessas ferramentas. Docker e um editor continuarão necessários na máquina do participante; o Claude será acessado pelo navegador. Diferenças de hardware não são eliminadas pelo Docker.

As imagens devem estar construídas, as dependências baixadas e o ambiente verificado antes da medição. Durante o trial, somente o código da solução pode ser alterado, incluindo métodos e classes auxiliares. Serão usadas as bibliotecas padrão do Java 21; testes, dependências, Docker e scripts de medição permanecerão fixos.

## 2. Exercícios e testes

- Foram selecionados **4 katas autorais de baixa indexação**, evitando clássicos muito difundidos (LeetCode/HackerRank/Codewars), para reduzir o risco de memorização pela IA.
- A seleção combinou classificação de dificuldade e critérios comuns: conhecimentos exigidos, quantidade de regras, tamanho esperado da solução e adequação ao limite de 35 minutos.
- Foram priorizados problemas de lógica, coleções e manipulação de dados/strings, sem frameworks ou algoritmos especializados.
- Exercícios já resolvidos por algum integrante serão substituídos antes da execução.
- Todos os testes de aceitação são visíveis e executáveis desde o início do trial, iguais para todos os participantes de um mesmo kata e não poderão ser alterados.
- A preparação deverá evitar acesso antecipado aos próximos enunciados. A separação em módulos, por si só, não restringe esse acesso.

A escolha de exercícios pouco conhecidos reduz, mas não elimina, o risco de memorização pela IA. A exposição do integrante que prepara os katas está documentada como ameaça à validade em §8.

### 2.1 Katas selecionados

Cada kata é um módulo Maven em `katas/kata-0X`, com enunciado (`README.md`), código
inicial em `src/main/java` (compila, mas falha propositalmente) e testes de aceitação
JUnit 5 em `src/test/java`. Todos usam apenas a biblioteca padrão do Java 21 e o pacote
padrão (sem `package`), seguindo `katas/smoke` como referência.

| Kata | Título | Domínio | Fonte |
|---|---|---|---|
| kata-01 | Normalizador de Etiquetas | Parsing de string + coleções | Autoral do grupo (spec própria) |
| kata-02 | Agrupador de Extrato | Agregação de dados | Autoral do grupo (spec própria) |
| kata-03 | Compressor de Corridas | Codificação de string (variação de run-length) | Autoral do grupo (variação com regra própria) |
| kata-04 | Validador de Agenda | Intervalos de tempo + lógica | Autoral do grupo (spec própria) |

**Fontes e baixa indexação.** Os quatro katas são enunciados autorais do grupo, e não
cópias de problemas catalogados. Quando a ideia subjacente é conhecida (por exemplo,
codificação por corridas no kata-03), o enunciado adota uma regra própria (corridas de
tamanho 1 permanecem literais, sem prefixo de contagem) e um contrato de entrada/saída
específico, de modo que a especificação exata e os testes não estão indexados. Isso reduz
a chance de a IA reproduzir uma solução memorizada em vez de efetivamente auxiliar.

### 2.2 Justificativa de comparabilidade

Os katas foram desenhados para dificuldade equivalente, adequada a um trial de 35 minutos:
uma única classe de solução, entrada determinística, poucas regras e saída ordenada/definida,
testável por asserções simples de JUnit. A tabela abaixo resume os critérios de comparabilidade.

| Kata | Conhecimentos exigidos | Nº de regras | Tamanho esperado da solução | Nº de testes | Adequação a 35 min |
|---|---|---|---|---|---|
| kata-01 | Split, trim, lowercase, deduplicação preservando ordem | 5 | ~20–30 LOC | 8 | Sim |
| kata-02 | Parsing `chave:valor`, agregação por soma, ordenação com desempate | 5 | ~25–35 LOC | 8 | Sim |
| kata-03 | Varredura de corridas consecutivas, formatação condicional | 5 | ~25–35 LOC | 8 | Sim |
| kata-04 | Parsing de horários `HH:MM`, detecção de sobreposição de intervalos, ordenação | 5 | ~30–40 LOC | 8 | Sim |

Todos compartilham a mesma forma — *ler entrada → aplicar poucas regras → produzir saída
ordenada/normalizada* — e a mesma faixa de esforço, mantendo a comparabilidade exigida pelo
desenho crossover within-subject. Cada suíte tem 8 testes de aceitação; os casos de borda
triviais (entrada vazia/nula) podem passar desde o início, mas a lógica central de cada kata
começa vermelha, tornando o *time-to-green* uma medida significativa para a RQ1.

## 3. Tratamentos e consultas

| Item | Decisão |
|---|---|
| Tratamento com IA | Claude pelo navegador |
| Modelo e esforço informados | “Sonnet 5”, esforço “alto”: nomenclatura e disponibilidade ainda devem ser confirmadas na interface |
| Conversa | Nova conversa por trial, sem histórico de tentativas anteriores |
| Prompts | Prompt inicial padronizado, seguido de interação livre |
| Evidência de uso | Resumo das perguntas enviadas, vinculado ao trial e redigido após o encerramento do cronômetro |
| Consultas nos dois tratamentos | Documentação, fóruns e tutoriais permitidos; busca ou consulta de soluções específicas do kata proibida |
| Tratamento sem IA | Assistentes de IA desativados; consultas permitidas não autorizam o uso de respostas de IA |

O mesmo assistente, modelo e configuração deverão ser utilizados em todos os trials com IA. Não haverá troca de assistente durante uma tentativa. O texto do prompt inicial será definido na preparação.

## 4. Distribuição e sessões

Cada integrante resolverá os quatro katas uma vez, com dois trials por tratamento: **12 trials no total**.

| Rodada | Integrante A | Integrante B | Integrante C |
|---|---|---|---|
| 1 | K1 sem IA | K1 com IA | K2 sem IA |
| 2 | K2 com IA | K2 sem IA | K3 com IA |
| 3 | K3 sem IA | K3 com IA | K4 sem IA |
| 4 | K4 com IA | K4 sem IA | K1 com IA |

Essa distribuição alterna tratamentos, inclui ambos para cada kata e mantém dois trials por tratamento para cada participante. Com três participantes, a distribuição por kata é de 2 para 1; o contrabalanceamento não é completo. Os nomes correspondentes a A, B e C serão registrados antes da execução.

- Duas sessões por integrante: rodadas 1–2 e rodadas 3–4.
- Intervalo fixo de **10 minutos** entre os trials de uma sessão, fora da medição.
- Até 2h20 de execução por integrante, mais intervalos e preparação.
- Familiarização padronizada antes dos trials oficiais, com exercício extra para praticar Docker, testes, cronômetro e Claude. Esses resultados não entrarão na análise.
- Enunciados, soluções, prompts e dificuldades só serão compartilhados após todos concluírem os trials oficiais. Dúvidas operacionais podem ser discutidas sem revelar conteúdo dos katas.

## 5. Cronometragem e ocorrências

- Limite fixo de **35 minutos por trial**, sem pausas.
- Início ao liberar o enunciado: leitura, compreensão, implementação e testes integram o tempo observado.
- Detecção automática de sucesso: comando padronizado executará os testes pelo Maven e o script identificará quando todos passarem.
- O tempo de sucesso será registrado no término da execução bem-sucedida dos testes, dentro do limite.
- O limite vale mesmo com testes em execução. Ao atingir 35 minutos, encerra-se a edição e preserva-se o código final.
- Trials que atingirem o limite sem sucesso serão registrados como **censurados em 35 minutos**, sem descarte.
- Falhas técnicas impeditivas serão registradas, preservando código, tempo e motivo, sem pausa nem repetição automática. Ficarão separadas dos trials censurados por esgotamento normal do tempo.
- Indisponibilidade impeditiva ou limite de uso do Claude seguirá a regra de ocorrência técnica, sem troca de assistente.

A medição usará relógio monotônico. A preparação deverá definir como capturar o código no limite e avaliar seus testes finais sem contar uma execução posterior como conclusão dentro do prazo. Falha do ambiente não deve ser confundida com falha funcional da solução.

## 6. Métricas e hipóteses

| RQ | Métricas adotadas | Hipóteses conceituais |
|---|---|---|
| RQ1 — Tempo | Tempo observado até sucesso ou limite; indicador de censura; quantidade de trials concluídos | H₀: a IA não reduz o tempo. H₁: a IA reduz o tempo. |
| RQ2 — Qualidade funcional | Total de testes, quantidade e percentual passando, número absoluto falhando | H₀: a IA não reduz a proporção de testes falhando. H₁: a IA reduz essa proporção. |
| RQ3 — Estrutura | Complexidade ciclomática média por método, percentual de linhas duplicadas e LOC | Para cada métrica estrutural de interesse: H₀: não há diferença entre tratamentos. H₁: há diferença. |

LOC será uma métrica de controle obrigatória para interpretar complexidade e duplicação. A coleta estrutural abrangerá o código produzido pelo participante, excluindo testes e infraestrutura.

Ferramentas escolhidas: **PMD para complexidade, CPD para duplicação e coleta complementar de LOC**. A integração deverá validar compatibilidade com Java 21 e definir versões, regras, limiares, denominadores e forma de agregação. A saída do CPD precisará ser processada para calcular o percentual de linhas duplicadas sem contar sobreposições repetidamente.

## 7. Análise planejada

- Estatística descritiva com **mediana e IQR por tratamento**.
- Comparação pareada por participante e **Wilcoxon pareado**, conforme orientação do enunciado.
- Hipóteses direcionais para RQ1/RQ2 e não direcionais para RQ3.
- Identificação explícita dos tempos censurados, acompanhada da quantidade de conclusões por tratamento. Um registro de 35 minutos sem sucesso não representa tempo de conclusão.
- Discussão da capacidade inferencial muito limitada com apenas três participantes; os 12 trials não serão tratados como 12 participantes independentes.

Antes da coleta oficial, o protocolo analítico deverá formalizar a agregação dos dois trials de cada tratamento por participante, o tratamento de censura e ocorrências técnicas, o nível de significância e os critérios dos testes. O Wilcoxon comum não trata censura diretamente; sua aplicação ao tempo exige definir claramente o que será comparado e as limitações. Ausência de significância não será interpretada como equivalência dos tratamentos.

## 8. Ameaças à validade

Consolidação das ameaças à validade do experimento, conforme o item H do Passo 1 do
[enunciado](enunciado.md). Várias já aparecem, de forma dispersa, em outras seções; aqui
são reunidas com a mitigação adotada e o risco residual.

### 8.1 Memorização pela IA (validade interna)

Se um kata for muito conhecido, a IA pode reproduzir uma solução vista no treinamento em
vez de efetivamente auxiliar, inflando artificialmente o efeito do tratamento com IA.

- **Mitigação:** uso de 4 katas autorais de baixa indexação, com specs e testes próprios; onde a ideia subjacente é conhecida, adota-se uma regra própria e um contrato de I/O específico (ver §2, §2.1). Registro do resumo de perguntas à IA por trial (§3) permite inspecionar sinais de resposta memorizada.
- **Risco residual:** a baixa indexação reduz, mas não elimina, o risco; ideias fundamentais podem estar implicitamente no treinamento da IA.

### 8.2 Exposição prévia de quem prepara os katas (validade interna)

O integrante que redige/prepara os katas conhece os enunciados e soluções antes do trial,
o que o beneficiaria indevidamente ao resolvê-los.

- **Mitigação:** a preparação ocorre antes de o participante acessar o enunciado e antes da medição; enunciados, soluções e dificuldades só são compartilhados após todos concluírem os trials oficiais (§4). A distribuição A/B/C será registrada antes da execução.
- **Risco residual:** a exposição de quem prepara não é totalmente eliminável; deve ser considerada na leitura dos resultados individuais desse integrante.

### 8.3 Efeito de aprendizado entre katas (validade interna)

Resolver katas em sequência pode gerar aprendizado (ferramenta, ambiente, padrões de
problema) que se transfere para os katas seguintes, confundindo-se com o efeito do tratamento.

- **Mitigação:** desenho crossover within-subject com **ordem contrabalanceada** entre integrantes (§4), de modo que a posição de cada kata e de cada tratamento varie entre os participantes; familiarização padronizada antes dos trials oficiais, cujos resultados não entram na análise (§4).
- **Risco residual:** com apenas três participantes, o contrabalanceamento não é completo (distribuição 2:1 por kata, §4), então o efeito de aprendizado não é totalmente neutralizado.

### 8.4 Familiaridade prévia com a ferramenta de IA (validade de construção)

Diferenças na experiência prévia de cada integrante com o Claude podem afetar o desempenho
no tratamento com IA, independentemente do efeito real da ferramenta.

- **Mitigação:** mesmo assistente, modelo e configuração em todos os trials, com prompt inicial padronizado (§3); exercício de familiarização padronizado antes dos trials oficiais (§4).
- **Risco residual:** a familiarização reduz, mas não uniformiza, a habilidade prévia com a ferramenta.

### 8.5 Vazamento de solução já vista (validade interna)

Um integrante pode ter resolvido antes um exercício equivalente, ou consultar uma solução
específica durante o trial, contaminando a medição.

- **Mitigação:** exercícios já resolvidos por algum integrante serão substituídos antes da execução (§2); consulta a soluções específicas do kata é proibida nos dois tratamentos, permitindo-se apenas documentação, fóruns e tutoriais (§3).
- **Risco residual:** o cumprimento da regra de não consultar soluções depende de conduta e não é tecnicamente forçado.

### 8.6 Baixo poder estatístico (validade de conclusão)

Com três participantes e 12 trials, a capacidade inferencial é muito limitada.

- **Mitigação:** uso de mediana e IQR e do teste não paramétrico de Wilcoxon pareado, consistente com o desenho within-subject (§6, §7); os 12 trials não serão tratados como 12 participantes independentes.
- **Risco residual:** ausência de significância não poderá ser interpretada como equivalência dos tratamentos; conclusões terão caráter exploratório.

## 9. Armazenamento e preservação

Será criada uma pasta exclusiva por tentativa, identificada por participante, kata e tratamento, contendo:

- Código final da solução, capturado no encerramento.
- JSON com identificação, configuração relevante, tempo e resultados.
- Relatórios dos testes e das métricas estruturais.
- Resumo das perguntas ao Claude, quando aplicável.
- Ocorrências técnicas, quando houver.

As métricas poderão ser calculadas após o trial, sobre o código preservado. Tentativas anteriores não serão sobrescritas. Um script produzirá o **CSV consolidado a partir dos JSONs individuais**.

## 10. Responsabilidades e rastreabilidade

Será seguida a divisão sugerida pelo professor para a S01:

| Integrante | Responsabilidade |
|---|---|
| Integrante 1 — Joaquim | Script de cronometragem e coleta de tempo, documentação de uso e integração com resultados dos testes |
| Integrante 2 | Ambiente Docker e execução/coleta de métricas estáticas |
| Integrante 3 | Pesquisa e validação dos katas, hipóteses e ameaças à validade; contribuição de código, como testes dos katas |
| Todos | Revisão conjunta do desenho experimental |

Cada integrante deve ser Assignee de pelo menos uma Issue com artefato de código commitado em **cada sprint**. Commits devem referenciar a Issue correspondente. Cada trial terá uma Issue individual atribuída ao responsável. Cartões de desenho e preparação devem constar no GitHub Projects.

## 11. Pendências de preparação

As decisões acima orientam a implementação. Ainda deverão ser concretizados e documentados:

- ~~Os quatro exercícios, suas fontes e a justificativa de comparabilidade.~~ **Concluído** — ver §2.1 e §2.2.
- Versões exatas das ferramentas e confirmação do modelo/esforço do Claude para todos.
- Prompt inicial, exercício e duração da familiarização.
- Comandos, esquema dos registros, captura no limite e cálculo das métricas.
- Protocolo estatístico detalhado, especialmente censura e agregação por participante.
- Identificação A/B/C, agenda, Issues e link do repositório/GitHub Projects.

Essas pendências devem ser resolvidas antes dos trials oficiais para evitar decisões influenciadas pelos resultados.
