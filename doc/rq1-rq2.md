# LAB02 — RQ1 (tempo) e RQ2 (defeitos) (Issue #32)

**RQ1 — O uso do assistente de IA reduz o tempo até passar nos testes?** **RQ2 — O uso
do assistente de IA reduz a proporção de testes falhando?** Ambas com hipóteses
**direcionais** (H₁: a IA reduz), portanto teste **unilateral**
([protocolo-estatistico.md](protocolo-estatistico.md) §4, §6).

## Como reproduzir

```bash
docker compose run --rm lab sh -c "python scripts/trial.py export && python scripts/rq1_rq2.py"
```

Saídas: `results/rq1_rq2.csv` (teste por RQ) e `results/rq1_rq2_pares.csv` (pares por
participante). Ferramentas: pandas 2.2.3, numpy 2.1.3, scipy 1.14.1
(`scipy.stats.wilcoxon`, `method="exact"`, `alternative="less"`).

## Método

Segue o [protocolo estatístico](protocolo-estatistico.md) (Issue #30):

1. **Elegibilidade (§3).** RQ1 usa apenas trials `completed` (censurados não têm tempo de
   conclusão e são contados à parte); RQ2 usa trials com avaliação final válida
   (`total > 0`), inclusive censurados. Nos 18 trials oficiais, todos são `completed`.
2. **Agregação (§2).** Para cada participante, a **mediana** dos 3 trials de cada
   tratamento, formando um par `(sem-ia, com-ia)` — **n = 3 pares**.
3. **Teste (§6).** Wilcoxon dos postos sinalizados pareado, **unilateral**, α = 0,05,
   sobre as diferenças `com-ia − sem-ia`. `alternative="less"` testa se a diferença é
   negativa (com-ia < sem-ia, isto é, IA reduz). Pares com diferença zero são descartados
   antes dos postos.
4. **Tamanho de efeito.** Correlação rank-biserial pareada,
   `r = (W⁺ − W⁻) / (W⁺ + W⁻)`, de −1 (com-ia sempre menor) a +1 (com-ia sempre maior).

**Resolução do teste.** Com 3 pares, o menor p-valor **unilateral** possível é
1/2³ = **0,125** (as três diferenças no sentido esperado). Logo **nenhum** resultado pode
ser significativo a 5% neste desenho; o teste é reportado por rigor de protocolo, e a
leitura se apoia nos pares e na descritiva
([limitacao-inferencial.md](limitacao-inferencial.md)).

## Resultados

### RQ1 — Tempo até verde (s)

Pares por participante (mediana dos 3 trials):

| Participante | sem-ia | com-ia | Diferença (com − sem) |
|---|---|---|---|
| gabriel | 238,71 | 183,16 | −55,55 |
| joaquim_vilela | 999,05 | 290,67 | −708,38 |
| vitor | 1163,67 | 99,62 | −1064,05 |

| RQ | Pares (efetivos) | Mediana das dif. | W | p (unilateral) | r (rank-biserial) | Decisão |
|---|---|---|---|---|---|---|
| RQ1 | 3 (3) | −708,38 | 0 | 0,125 | −1,00 | Não rejeita H₁₀ |

Leitura por kata (mediana sem-ia / com-ia, em s):

| Kata | sem-ia | com-ia |
|---|---|---|
| kata-01 | 96,07 | 213,08 |
| kata-02 | 858,28 | 43,30 |
| kata-03 | 238,71 | 155,91 |
| kata-04 | 1172,03 | 183,16 |
| kata-05 | 550,49 | 316,34 |
| kata-06 | 1241,30 | 238,27 |

### RQ2 — Testes falhando (nº)

Todos os 18 trials terminaram com **8/8 testes passando** (0 falhando), nos dois
tratamentos. Assim, as três diferenças pareadas são zero, todos os pares são descartados
pelo método de Wilcoxon e o **teste não é aplicável**.

| RQ | Pares (efetivos) | Mediana das dif. | Decisão |
|---|---|---|---|
| RQ2 | 3 (0) | 0 | Teste não aplicável (sem variância) |

## Interpretação

- **RQ1 (tempo).** A direção é **totalmente consistente**: os três participantes foram
  mais rápidos com IA (todas as diferenças negativas), com efeito máximo possível
  (r = −1,00) e mediana das diferenças de −708 s (≈ 12 min). Ainda assim, **p = 0,125**,
  acima de α = 0,05 — o valor mínimo alcançável com n = 3 num teste unilateral. Ou seja:
  há uma **tendência forte e uniforme** de redução de tempo com IA, mas o desenho de três
  participantes **não tem poder** para confirmá-la estatisticamente. A magnitude é
  expressiva e cresce com a dificuldade do kata: nos katas mais longos sem IA (kata-04 e
  kata-06, > 1170 s de mediana), o tratamento com IA cai para a faixa de 180–240 s. A
  única inversão pontual é o kata-01, curto, em que o tempo com IA ficou acima do sem-ia.
- **RQ2 (defeitos).** Não há o que testar: ambos os tratamentos atingiram qualidade
  funcional **máxima** (8/8) em todos os trials dentro do time-box. A métrica **não
  discrimina** neste experimento — não porque os tratamentos sejam comprovadamente
  equivalentes, mas porque os katas foram resolvidos por completo em todos os casos. Uma
  leitura possível: o time-box de 35 min foi suficiente para chegar ao verde nas duas
  condições; a diferença entre tratamentos apareceu no **tempo** (RQ1), não no acerto
  final (RQ2).

## Limitações específicas

- **Poder nulo a 5%.** Com n = 3 pares, nem um efeito perfeitamente consistente atinge
  significância unilateral (p mínimo 0,125). Ausência de significância **não** é
  equivalência ([decisoes.md](decisoes.md) §8.6); a conclusão é exploratória.
- **RQ2 sem variância.** O piso/teto de 8/8 em todos os trials impede qualquer teste;
  interpretar RQ2 apenas descritivamente.
- **Tratamento confundido com participante dentro de cada kata** (contrabalanceamento
  2:1, [decisoes.md](decisoes.md) §8.3): a leitura por kata mistura efeito do tratamento
  com estilo/experiência do participante.
