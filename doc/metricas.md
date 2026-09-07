# LAB02 — Métricas estruturais (RQ3)

Documenta as ferramentas, regras, limiares e cálculos usados por `scripts/metrics.py`
para coletar complexidade ciclomática, percentual de linhas duplicadas e LOC sobre o
código final preservado de cada trial (`results/<trial_id>/final/katas/<kata>/src/main/java`),
conforme [doc/decisoes.md](decisoes.md#6-métricas-e-hipóteses). A coleta abrange apenas o
código do participante: `src/main/java`, sem testes (`src/test/java`) nem infraestrutura
(POM, scripts).

## Ferramentas e versões

- **PMD 7.17.0** para complexidade ciclomática (regra `category/java/design.xml/CyclomaticComplexity`).
- **CPD 7.17.0** (subcomando `pmd cpd`) para duplicação de código.
- Ambas fixadas na imagem Docker (`Dockerfile`); a versão efetivamente usada em cada
  kata é registrada por `scripts/prepare.py` em `results/environment-<kata>.json`.

## LOC (linhas de código)

Contagem própria (`metrics.loc`), por não haver uma ferramenta já instalada dedicada a
isso: uma linha conta como LOC se, depois de remover comentários (`//`, `/* */`,
preservando o conteúdo de literais de string/char), sobrar algum caractere não-espaço.
Linhas em branco e linhas compostas somente por comentário não contam. O total por kata
é a soma do LOC de todos os `.java` em `src/main/java`.

LOC é métrica de controle obrigatória (§6 de `doc/decisoes.md`): serve de denominador
para o percentual de duplicação e de referência para interpretar a complexidade.

## Complexidade ciclomática

- Regra PMD `CyclomaticComplexity`, com `methodReportLevel=1` (limiar reduzido a 1 para
  que a regra reporte **todos** os métodos, não só os que excedem um limiar de alerta —
  o objetivo aqui é medir, não apenas alertar sobre métodos complexos).
- Cada violação com atributo `method` no relatório XML fornece a complexidade daquele
  método, extraída da mensagem (`"has a cyclomatic complexity of N"`). A violação de
  nível de classe (totais agregados, sem atributo `method`) é ignorada.
- Métrica reportada: **complexidade ciclomática média por método** = média aritmética
  simples dos valores por método do kata. Sem métodos, a média é `null` (não zero).

## Duplicação de código

- `pmd cpd -l java --minimum-tokens 50`. O limiar de 50 tokens é menor que o padrão da
  ferramenta (100): os katas têm soluções de até 35 minutos, então blocos duplicados
  tendem a ser curtos (nível de método), e um limiar alto deixaria de detectar boa parte
  deles.
- O relatório XML lista, para cada grupo de duplicação, os arquivos e faixas de linha
  (`line`/`endline`) envolvidos. Para cada arquivo, essas faixas são unidas em um
  conjunto de números de linha (`set`), evitando contar a mesma linha mais de uma vez
  quando ela participa de múltiplas duplicações sobrepostas.
- Percentual de duplicação = (linhas duplicadas ∩ linhas de LOC, somadas em todos os
  arquivos) ÷ (LOC total) × 100. A interseção com as linhas de LOC garante que o
  numerador e o denominador usem a mesma definição de "linha de código" (sem contar
  linhas em branco/comentário como duplicadas). Sem LOC, o percentual é `null`.

## Códigos de saída do PMD/CPD

Tanto `pmd check` quanto `pmd cpd` retornam `0` quando nada é encontrado e `4` quando há
violações/duplicações — **não** é um código de erro de execução. `scripts/metrics.py`
trata apenas códigos fora de `{0, 4}` como falha da ferramenta.

## Saída

`scripts/metrics.py collect --trial results/<trial_id>` grava `results/<trial_id>/metrics.json`:

```json
{
  "trial_id": "...",
  "kata": "...",
  "source": "...",
  "collected_at": "...",
  "loc": {"total": 0, "per_file": {"Arquivo.java": 0}},
  "complexity": {"per_method": [0], "method_count": 0, "average": 0.0},
  "duplication": {"minimum_tokens": 50, "duplicated_loc": 0, "percent": 0.0}
}
```

`scripts/metrics.py collect-all` processa todos os trials em `results/` que já tenham
`final/` preservado, pulando os que ainda não têm `metrics.json` (a menos que `--force`
seja usado) e ignorando trials sem código final localizável.

## Pendências

- A integração desse JSON ao CSV consolidado (`scripts/trial.py export`, integrante 1)
  ainda não foi feita — hoje os arquivos ficam paralelos por trial.
