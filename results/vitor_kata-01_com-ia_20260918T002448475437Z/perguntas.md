# Resumo das perguntas ao Claude

- Modelo/esforço: Claude Sonnet 5, esforço High (Claude Code / terminal).
- Após colar o enunciado do kata-01, pedi que a IA propusesse a abordagem de implementação de `TagNormalizer.normalize`.
- A IA sugeriu: `split(",")` → `trim()` → colapsar espaços internos com `replaceAll("\\s+", " ")` → `toLowerCase()` → descartar vazios → deduplicar preservando ordem com `LinkedHashSet`.
- Aprovei a abordagem sem alterações; a IA implementou o método diretamente no arquivo.
- Rodei os testes uma única vez (ENTER no cronômetro): 8/8 passaram de primeira, sem necessidade de correções adicionais.
