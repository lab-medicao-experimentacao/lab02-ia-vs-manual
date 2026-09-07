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

Versões: Temurin 21.0.7, Maven 3.9.9, Python 3.12.11, JUnit 5.13.4, Surefire 3.5.4 e PMD/CPD 7.17.0. As imagens base são fixadas por digest. A preparação registra as versões efetivamente executadas em `results/environment-<kata>.json`. Use a mesma imagem construída para o trio; pacotes do sistema instalados por apt não constituem um build bit a bit reproduzível.

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

O `smoke` serve apenas para verificar infraestrutura. Restaure seu código inicial após a prática. Os quatro módulos oficiais estão vazios e o cronômetro recusa iniciá-los enquanto não tiverem testes.

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

Use `--include-practice` apenas para conferir registros de prática. O CSV inclui estados e valores ausentes, sem descartar automaticamente ocorrências.

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

## Divisão da estrutura

- `scripts/trial.py`: cronômetro, testes e coleta JSON/CSV — integrante 1.
- `scripts/prepare.py`, `scripts/metrics.py`, `Dockerfile`, `compose.yaml` e `pom.xml`: ambiente e coleta de métricas estruturais — integrante 2.
- `katas/kata-01` a `kata-04`: espaços para exercícios e testes — integrante 3.
- `katas/smoke`: exercício provisório fora da amostra.
- `tests/`: testes do ciclo de vida do cronômetro e da coleta de métricas.

PMD e CPD estão instalados e disponíveis via `docker compose run --rm lab pmd --help`. Regras de complexidade, limiar de duplicação, cálculo de percentuais e LOC estão implementados em `scripts/metrics.py` e documentados em [doc/metricas.md](doc/metricas.md).

A integração interpreta os [relatórios do Maven Surefire](https://maven.apache.org/components/surefire-archives/surefire-3.5.4/maven-surefire-plugin/usage.html). A instalação do analisador segue a [distribuição e CLI do PMD 7](https://pmd.github.io/pmd/pmd_userdocs_migrating_to_pmd7.html).
