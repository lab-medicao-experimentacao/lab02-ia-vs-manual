# LAB02 — Validação fim a fim dos katas oficiais (S01)

Registro da validação da issue **#19** — *Validar cronômetro e coletor de métricas
sobre os katas oficiais*. O objetivo foi confirmar a integração fim a fim de
`scripts/prepare.py`, `scripts/trial.py` e `scripts/metrics.py` sobre os quatro katas
oficiais (kata-01 a kata-04), e não apenas sobre o módulo `smoke`, antes da execução
oficial da S02.

Toda a validação rodou dentro do contêiner Docker (`docker compose run --rm lab ...`),
que padroniza Java 21, Maven, Python e PMD/CPD conforme `Dockerfile` e `compose.yaml`.

## Ambiente

- Execução via Docker, atrás de proxy corporativo (Zscaler). O certificado raiz do proxy
  foi adicionado ao truststore do sistema (curl) e do Java (`cacerts`) no `Dockerfile`,
  permitindo o download do PMD e o download de dependências pelo Maven.
- PMD/CPD 7.17.0 sobre Java 21.0.7 (Temurin), confirmado com `pmd --version` no contêiner.

## Etapa 1 — `prepare.py` (preparação e validação offline)

`docker compose run --rm lab python scripts/prepare.py --kata kata-0N` para cada kata.
Todos concluíram com "Ambiente preparado e validado offline", gravando
`results/environment-kata-0N.json`. Os testes falham propositalmente (código inicial é um
stub); a preparação valida o ambiente, não a solução.

| Kata | Preparação | Registro |
|---|---|---|
| kata-01 | OK | `results/environment-kata-01.json` |
| kata-02 | OK | `results/environment-kata-02.json` |
| kata-03 | OK | `results/environment-kata-03.json` |
| kata-04 | OK | `results/environment-kata-04.json` |

## Etapa 2 — `trial.py` (cronômetro e captura)

Trial curto de prática por kata, não interativo:

```
docker compose run --rm lab python scripts/trial.py start \
  --participant valida --kata kata-0N --treatment sem-ia \
  --practice --auto-test --seconds 30
```

Todos encerraram no estado **`censored`** (o stub não passa nos testes dentro do limite —
resultado correto para um trial não resolvido), com código final preservado em
`results/valida_kata-0N_semia/final/` e avaliação final registrada em `trial.json`.

Contagens de teste capturadas na avaliação final (RQ2 — qualidade funcional):

| Kata | Total | Passando | Falhando | % sucesso |
|---|---|---|---|---|
| kata-01 | 8 | 3 | 5 | 37,5% |
| kata-02 | 8 | 2 | 6 | 25,0% |
| kata-03 | 8 | 1 | 7 | 12,5% |
| kata-04 | 8 | 3 | 5 | 37,5% |

As contagens conferem com a verificação local via Maven, confirmando que a leitura dos
relatórios do Surefire funciona sobre os katas oficiais.

## Etapa 3 — `metrics.py` (métricas estruturais)

`docker compose run --rm lab python scripts/metrics.py collect --trial results/valida_kata-0N_semia`
para cada kata. Todos gravaram `metrics.json` com valores válidos (não nulos); PMD
reportou violações com `Errors:0`.

| Kata | LOC | Complexidade média/método | Métodos | Duplicação % |
|---|---|---|---|---|
| kata-01 | 6 | 1,0 | 1 | 0,0% |
| kata-02 | 6 | 1,0 | 1 | 0,0% |
| kata-03 | 5 | 1,0 | 1 | 0,0% |
| kata-04 | 6 | 1,0 | 1 | 0,0% |

Os valores são baixos porque foram medidos sobre o **stub** (código inicial), não sobre
uma solução real. O que a validação confirma é que a coleta de LOC, complexidade
(PMD `CyclomaticComplexity`) e duplicação (CPD) executa e produz saída estruturada válida
sobre os katas oficiais.

## Conclusão

A integração fim a fim está confirmada sobre os quatro katas oficiais:

- `prepare.py` valida o ambiente offline para cada kata;
- `trial.py` conduz o trial cronometrado, preserva o código final e captura tempo,
  censura e contagens de teste;
- `metrics.py collect` produz métricas estruturais (LOC, complexidade, duplicação) válidas
  sobre o código preservado.

Os artefatos gerados nesta validação ficam sob `results/` (ignorado pelo Git) e são
descartáveis: são trials de prática (`--practice`), fora da amostra oficial.
