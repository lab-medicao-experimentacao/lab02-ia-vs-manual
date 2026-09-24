# LAB02 — Limitação inferencial da amostra (Issue #35)

Discussão dedicada à **capacidade inferencial limitada** do experimento, dado o desenho
com **apenas três participantes**. Complementa a §7 do [protocolo estatístico](protocolo-estatistico.md)
e alimenta a discussão final do relatório (§4, Issue #40). Registra explicitamente por
que os trials **não** são tratados como observações independentes.

## 1. Por que a amostra é pequena para inferência

O desenho é **within-subject (crossover)** com 3 participantes × 6 katas, 3 trials por
tratamento por participante — **18 trials** no total (ver [decisoes.md](decisoes.md) §4).
A tentação é ler 18 (ou 9 por tratamento) como o tamanho amostral. Isso está **errado**
para inferência: os três trials de um mesmo participante e tratamento são **medidas
repetidas** do mesmo indivíduo, correlacionadas entre si, e não observações
independentes.

Conforme o protocolo (§2 de [protocolo-estatistico.md](protocolo-estatistico.md)), a
**unidade de análise é o participante**. Os três trials de cada tratamento são agregados
(por mediana) num único valor por participante, e o teste pareado opera sobre esses
pares. Logo, o n efetivo para o **Wilcoxon pareado é n = 3 pares** por métrica — não 9,
não 18.

## 2. Consequências para o poder estatístico

- **Poder muito baixo.** Com n = 3 pares, o Wilcoxon dos postos sinalizados tem pouquíssimas
  configurações de sinal possíveis. Mesmo um efeito consistente (as três diferenças no
  mesmo sentido) atinge apenas os menores p-valores que o teste consegue produzir com
  n = 3; efeitos reais moderados podem não alcançar significância só por falta de dados.
- **p-valor mínimo alcançável.** Para um teste **unilateral** com n = 3 pares, o menor
  p-valor possível (todas as diferenças no sentido esperado) é da ordem de **0,125**
  (1/2³) — **acima** de α = 0,05. Ou seja, para RQ1 e RQ2 (unilaterais), **nenhum**
  resultado com apenas 3 pares completos consegue ser significativo a 5% no Wilcoxon
  exato. Isso precisa ser dito abertamente: o teste é reportado por rigor de protocolo,
  mas o desenho não tem resolução para rejeitar H₀ a α = 0,05 com n = 3.
- **Sensibilidade a um único par.** Com n = 3, um par afetado por censura ou por
  ocorrência técnica (que reduz o n utilizável) ou um outlier pode inverter a leitura.

## 3. Implicações de interpretação

- **Ausência de significância ≠ equivalência.** Não rejeitar H₀ com n = 3 **não** é
  evidência de que os tratamentos são equivalentes; é, em boa medida, consequência do
  baixo poder ([decisoes.md](decisoes.md) §8.6).
- **Ênfase na estatística descritiva.** Dada a limitação do teste, o peso da análise
  recai sobre **mediana, IQR e a inspeção dos pares por participante** (Issue #31), com os
  testes de hipótese como complemento formal, não como veredito.
- **Caráter exploratório.** Todas as conclusões são exploratórias e geradoras de
  hipóteses para estudos maiores, não confirmatórias.

## 4. Fatores que agravam a limitação

- **Contrabalanceamento incompleto.** Com 3 participantes, a distribuição de tratamento é
  2:1 por kata, então o efeito de aprendizado entre katas não é totalmente neutralizado
  ([decisoes.md](decisoes.md) §8.3).
- **Exposição de quem preparou os katas** e **familiaridade prévia com a IA** introduzem
  variabilidade entre participantes que, com n = 3, não pode ser isolada
  estatisticamente ([decisoes.md](decisoes.md) §8.2, §8.4).
- **Censura em RQ1** reduz ainda mais os pares utilizáveis para o tempo, pois trials
  censurados não têm tempo de conclusão (protocolo §3).

## 5. O que seria necessário para inferência robusta

Registrado como direção para replicação (não como crítica ao escopo da disciplina): um
número substancialmente maior de participantes, ou um desenho com mais réplicas
independentes por condição, permitiria estimar tamanhos de efeito com intervalos de
confiança úteis e aplicar testes com poder adequado. No escopo atual, o valor do estudo
está na **descrição cuidadosa** dos pares observados e na documentação do método
reprodutível, não na generalização estatística.
