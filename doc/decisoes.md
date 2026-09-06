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

- Serão selecionados na internet **4 katas de boa qualidade e pouco conhecidos**, evitando clássicos muito difundidos.
- A seleção combinará classificação de dificuldade e critérios comuns: conhecimentos exigidos, quantidade de regras, tamanho esperado da solução e adequação ao limite de 35 minutos.
- Serão priorizados problemas de lógica, coleções e manipulação de dados, sem frameworks ou algoritmos especializados.
- Exercícios já resolvidos por algum integrante serão substituídos antes da execução.
- Todos os testes de aceitação serão visíveis e executáveis desde o início do trial, iguais para todos os participantes de um mesmo kata e não poderão ser alterados.
- A preparação deverá evitar acesso antecipado aos próximos enunciados. A separação em módulos, por si só, não restringe esse acesso.

A escolha de exercícios pouco conhecidos reduz, mas não elimina, o risco de memorização pela IA. A exposição do integrante que prepara os katas será documentada como ameaça à validade.

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

## 8. Armazenamento e preservação

Será criada uma pasta exclusiva por tentativa, identificada por participante, kata e tratamento, contendo:

- Código final da solução, capturado no encerramento.
- JSON com identificação, configuração relevante, tempo e resultados.
- Relatórios dos testes e das métricas estruturais.
- Resumo das perguntas ao Claude, quando aplicável.
- Ocorrências técnicas, quando houver.

As métricas poderão ser calculadas após o trial, sobre o código preservado. Tentativas anteriores não serão sobrescritas. Um script produzirá o **CSV consolidado a partir dos JSONs individuais**.

## 9. Responsabilidades e rastreabilidade

Será seguida a divisão sugerida pelo professor para a S01:

| Integrante | Responsabilidade |
|---|---|
| Integrante 1 — Joaquim | Script de cronometragem e coleta de tempo, documentação de uso e integração com resultados dos testes |
| Integrante 2 | Ambiente Docker e execução/coleta de métricas estáticas |
| Integrante 3 | Pesquisa e validação dos katas, hipóteses e ameaças à validade; contribuição de código, como testes dos katas |
| Todos | Revisão conjunta do desenho experimental |

Cada integrante deve ser Assignee de pelo menos uma Issue com artefato de código commitado em **cada sprint**. Commits devem referenciar a Issue correspondente. Cada trial terá uma Issue individual atribuída ao responsável. Cartões de desenho e preparação devem constar no GitHub Projects.

## 10. Pendências de preparação

As decisões acima orientam a implementação. Ainda deverão ser concretizados e documentados:

- Os quatro exercícios, suas fontes e a justificativa de comparabilidade.
- Versões exatas das ferramentas e confirmação do modelo/esforço do Claude para todos.
- Prompt inicial, exercício e duração da familiarização.
- Comandos, esquema dos registros, captura no limite e cálculo das métricas.
- Protocolo estatístico detalhado, especialmente censura e agregação por participante.
- Identificação A/B/C, agenda, Issues e link do repositório/GitHub Projects.

Essas pendências devem ser resolvidas antes dos trials oficiais para evitar decisões influenciadas pelos resultados.
