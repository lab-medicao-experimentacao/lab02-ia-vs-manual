# LAB02 — IA vs. codificação manual

Estrutura inicial da S01: cronômetro Python, registros JSON/CSV e ambiente Docker com Java 21, Maven, JUnit e PMD/CPD. O protocolo está em [doc/decisoes.md](doc/decisoes.md).

## Preparação

Instale Docker com Docker Compose. Java, Maven e Python não precisam ser instalados na máquina. Execute os comandos abaixo na raiz do repositório.

```bash
docker compose build
docker compose run --rm lab python -m unittest discover -s tests -v
docker compose run --rm lab python scripts/prepare.py --kata smoke
docker compose run --rm lab python tests/integration_maven.py
```

No Windows, prefira executar no WSL2 com Docker integrado.

A preparação baixa dependências, executa testes numa cópia temporária e verifica a execução offline. Os testes do `smoke` falham propositalmente: o objetivo é verificar o ambiente, não resolver o exercício. Uma falha de compilação ou ausência de relatórios impede concluir a preparação. Repita a preparação para cada kata quando seus testes estiverem disponíveis. Essa atividade acontece **antes de o participante acessar o enunciado e antes da medição**; deve ser conduzida por quem prepara o ambiente.

Versões: Temurin 21.0.7, Maven 3.9.9, Python 3.12.11, JUnit 5.13.4, Surefire 3.5.4, PMD/CPD 7.17.0, pandas 2.2.3, numpy 2.1.3, Matplotlib 3.9.2 e Seaborn 0.13.2 (`requirements.txt`). As imagens base são fixadas por digest. A preparação registra as versões efetivamente executadas em `results/environment-<kata>.json`. Use a mesma imagem construída para o trio; pacotes do sistema instalados por apt não constituem um build bit a bit reproduzível.

## Validar um trial provisório

```bash
docker compose run --rm lab python scripts/trial.py start --participant A --kata smoke --treatment sem-ia --practice --seconds 60
```

O comando inicia o relógio e mostra o enunciado. Edite `katas/smoke/src/main/java/Sum.java` na sua IDE. No terminal do cronômetro, pressione **Enter** para executar os testes. Para concluir o exercício provisório, a implementação deve retornar `a + b`.

- O relógio continua enquanto você edita e enquanto o Maven executa.
- Cada execução usa uma cópia isolada do código, sem resultados antigos.
- Todos os testes devem passar, sem erros ou testes ignorados, e o Maven deve terminar com sucesso antes do limite.
- Se você editar enquanto os testes rodam, o sucesso corresponde à cópia testada, preservada em `final/`.
- No limite, o processo de testes é encerrado e o código é copiado para avaliação final. Um resultado verde nessa avaliação **não transforma o trial censurado em concluído**.
- Digite `incidente descrição do problema` ou use Ctrl+C para registrar uma interrupção técnica. Não há pausa ou repetição automática.
- Para testes automatizados sem terminal, `--auto-test` dispara uma execução inicial; não repete automaticamente testes que falharam.

O `smoke` serve apenas para verificar infraestrutura. Restaure seu código inicial após a prática. Os seis módulos oficiais (`kata-01` a `kata-06`) já têm enunciado, código inicial e testes; o cronômetro recusa iniciar um módulo enquanto não tiver testes.

## Trial oficial

Depois da preparação e da definição dos katas:

```bash
docker compose run --rm lab python scripts/trial.py start --participant A --kata kata-01 --treatment sem-ia
```

O limite oficial é 2100 segundos (35 minutos). Limites menores são aceitos apenas com `--practice`; o módulo `smoke` também exige essa opção. Cada tentativa recebe um identificador único; `--id` permite informar um identificador explícito, sem sobrescrever uma pasta existente.

Não altere testes, POMs ou scripts durante o trial. O procedimento exige encerrar a edição ao aviso do cronômetro; o Docker não bloqueia o editor nem oculta os outros módulos. A captura de arquivos é uma cópia sequencial, não um snapshot atômico do sistema de arquivos. Não inicie trials simultâneos sobre o mesmo módulo. Em queda abrupta da máquina/contêiner, o JSON pode permanecer como `running`: preserve-o e documente a ocorrência, sem inventar horário de encerramento ou resultado final.

## Resultados

```text
results/<trial_id>/
├── trial.json          # identificação, tempos, estado e resultados
├── runs/               # cópias testadas e logs Maven
├── final/              # código preservado e relatórios finais
└── perguntas.md        # somente com IA; preencher após encerrar
```

Estados: `completed` (sucesso no prazo), `censored` (limite sem sucesso) e `interrupted` (ocorrência técnica). `running` identifica uma tentativa ainda ativa ou que sofreu encerramento abrupto.

`elapsed_seconds` é a duração observada; `time_to_green_seconds` só existe quando houve sucesso dentro do prazo. `final_evaluation.tests` contém total, passando, falhas, erros, ignorados e percentual passando. Sem relatório válido, as contagens são nulas — não zero. Erros de compilação e de execução ficam como `build_or_execution_error`, acompanhados do log; a classificação detalhada da causa exige revisão. A avaliação final tem um limite operacional de 120 segundos, separado do tempo experimental.

Consolidar os trials oficiais:

```bash
docker compose run --rm lab python scripts/trial.py export
```

Use `--include-practice` apenas para conferir registros de prática. O CSV inclui estados e valores ausentes, sem descartar automaticamente ocorrências. As métricas estruturais de `metrics.json` (LOC, complexidade, duplicação) entram como colunas; rode `metrics.py collect-all` antes para preenchê-las.

Carregar o CSV consolidado num DataFrame único (tipos convertidos, práticas descartadas, ausentes como NaN) para análise e dashboard:

```bash
docker compose run --rm lab python scripts/dataset.py
```

Em outro script: `from dataset import load; df = load()`. Dependências Python (pandas, numpy, Matplotlib, Seaborn) estão fixadas em `requirements.txt` e instaladas na imagem; rode `docker compose build` após atualizá-las.

## Dashboard

```bash
docker compose run --rm lab python scripts/dashboard.py
```

Gera `doc/dashboard/index.html` (página única, abre direto no navegador, sem servidor nem internet) e cada gráfico em `.svg` e `.png` para o relatório. Compara os tratamentos em tempo (RQ1), sucesso/testes falhando (RQ2) e métricas estruturais (RQ3). Apenas estatística descritiva. Rode `metrics.py collect-all` e `trial.py export` antes para usar dados atualizados.

O que o diferencia de um notebook com gráficos padrão:

- **Gráficos escolhidos pela pergunta, não pelo hábito.** Além da distribuição (pontos sobre boxplot fino), um *slope chart* liga a mediana sem IA à com IA de cada participante — a mesma lógica pareada do Wilcoxon — e *dumbbell charts* por kata mostram se o efeito se mantém em cada exercício, no tempo e na estrutura.
- **Número de destaque e cartões de resumo** no topo: razão entre as medianas de tempo, medianas por tratamento, trials analisados sobre os previstos e censurados.
- **Tooltip por trial**: passar o mouse sobre qualquer ponto mostra participante, kata, tratamento e valor.
- **Modo claro e escuro**: o SVG do Matplotlib é embutido com as cores trocadas por variáveis CSS, então o mesmo gráfico acompanha o tema do sistema (ou o botão "Alternar tema") sem ser redesenhado.
- **Cores acessíveis**: laranja (sem IA) e azul (com IA) validadas para daltonismo (protan/deutan/tritan) e contraste nos dois temas; a identidade nunca depende só da cor (rótulos no eixo, legenda e tooltip).
- **Sem gráfico vazio**: quando um indicador não varia (hoje, 100% de sucesso e 0% de duplicação em todos os trials), a página mostra uma nota no lugar do gráfico; o gráfico volta automaticamente quando houver diferença.
- **Transparência sobre os dados**: um bloco "Dados incompletos" lista participantes sem par e trials sem métricas, e some quando os dados estiverem completos; a tabela com todos os trials fica no fim da página.
- **Detalhes de acabamento**: números no formato brasileiro (vírgula decimal), layout responsivo até a largura de celular e figuras determinísticas (mesmos dados, mesmo SVG).

## Métricas estruturais

```bash
docker compose run --rm lab python scripts/metrics.py collect --trial results/<trial_id>
docker compose run --rm lab python scripts/metrics.py collect-all
```

Calcula complexidade ciclomática média por método (PMD), percentual de linhas
duplicadas (CPD) e LOC sobre `final/katas/<kata>/src/main/java` de cada trial, e grava
`results/<trial_id>/metrics.json`. `collect-all` processa todos os trials com código
final preservado, pulando os que já têm `metrics.json` (use `--force` para recalcular).
Regras, limiares e fórmulas usados estão documentados em [doc/metricas.md](doc/metricas.md).

`results/` é ignorado pelo Git para evitar commits acidentais de práticas e arquivos de build. Para entregar uma tentativa oficial revisada, adicione explicitamente seu JSON, código, logs/relatórios e resumo com `git add -f <caminhos>`. Não é necessário versionar arquivos compilados em `target/classes`. Referencie a Issue do trial no commit.

## Análise RQ3 (estrutura)

```bash
docker compose run --rm lab python scripts/rq3.py
```

Agrega complexidade, duplicação e LOC por participante × tratamento (mediana dos 3 trials) e aplica Wilcoxon pareado bilateral (α = 0,05) sobre os pares, conforme [doc/protocolo-estatistico.md](doc/protocolo-estatistico.md). Grava `results/rq3.csv` e `results/rq3_pares.csv`; a leitura dos resultados está em [doc/rq3.md](doc/rq3.md). Requer `scipy` (rode `docker compose build` se a imagem for anterior).

## Divisão da estrutura

- `scripts/trial.py`: cronômetro, testes e coleta JSON/CSV — integrante 1.
- `scripts/prepare.py`, `scripts/metrics.py`, `Dockerfile`, `compose.yaml` e `pom.xml`: ambiente e coleta de métricas estruturais — integrante 2.
- `katas/kata-01` a `kata-06`: espaços para exercícios e testes — integrante 3.
- `katas/smoke`: exercício provisório fora da amostra.
- `tests/`: testes do ciclo de vida do cronômetro e da coleta de métricas.

PMD e CPD estão instalados e disponíveis via `docker compose run --rm lab pmd --help`. Regras de complexidade, limiar de duplicação, cálculo de percentuais e LOC estão implementados em `scripts/metrics.py` e documentados em [doc/metricas.md](doc/metricas.md).

A integração interpreta os [relatórios do Maven Surefire](https://maven.apache.org/components/surefire-archives/surefire-3.5.4/maven-surefire-plugin/usage.html). A instalação do analisador segue a [distribuição e CLI do PMD 7](https://pmd.github.io/pmd/pmd_userdocs_migrating_to_pmd7.html).
