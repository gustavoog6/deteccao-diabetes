# Combinações de KNN, árvore e rede neural

## Versão atual: média e desvio padrão

Por decisão de 06/11/2026, as novas comparações usam `(valor − média) / desvio padrão` nas medidas numéricas de todos os componentes. O desenvolvimento está em [02_Combinacoes_escala_padrao.ipynb](02_Combinacoes_escala_padrao.ipynb), com parâmetros calculados somente no treinamento de cada parte.

A nova seleção comparou 79.326 regras e levou 39 candidatas à segunda etapa. O trio escolhido usa **32,5% KNN, 42,5% árvore e 25% rede**, com limite de **45,5%**. O F1 macro médio na seleção foi **91,53%** e o da reserva foi **86,49%**, com matriz `[[42, 8], [6, 48]]` e 90 acertos em 104 amostras.

O KNN individual com essa escala teve F1 de **75,94%** na reserva, contra 86,53% na versão anterior com quartis. A árvore e a rede mantiveram suas previsões. A decisão de usar a fórmula comum está registrada junto com esse efeito observado.

O CSV desta mistura é [submissao_combinacao_zscore.csv](../resultados/submissao_combinacao_zscore.csv). Os registros usam o prefixo `resultados/combinacoes_zscore_*`. O CSV individual do KNN é `resultados/submissao_knn_zscore.csv`.

## Histórico: quartis no KNN

O [notebook 01_Combinacoes.ipynb](01_Combinacoes.ipynb) registra a busca, as regras, as métricas por divisão e a geração dos arquivos para o Kaggle. As explicações estão em Markdown, e as saídas estão salvas.

### Indicação da busca anterior

A regra usa 25% do apoio do KNN K=11, 42,5% do apoio da árvore de quatro atributos e 32,5% da saída da rede neural com quatro entradas e 12 neurônios ocultos. Se a média ponderada for maior que 0,455, a classe é diabetes; se for menor, controle. Na igualdade numérica, usamos o voto da árvore. Não tratamos os apoios como probabilidades calibradas.

O arquivo para essa indicação é [submissao_combinacao_escolhida.csv](../resultados/submissao_combinacao_escolhida.csv).

### Resultados anteriores

| Regra | F1 macro na seleção | F1 médio nas conferências 509 e 911 | F1 na reserva |
|---|---:|---:|---:|
| Mistura original | 90,74% | 90,48% | 87,49% |
| Trio, pesos iguais | 90,74% | 91,20% | 86,53% |
| Melhor dupla | 91,25% | 90,35% | 84,56% |
| Melhor trio | 91,37% | 90,95% | 88,44% |

A indicação principal acertou 92 de 104 amostras, com acurácia 88,46%, F1 macro 88,44% e matriz `[[44, 6], [6, 48]]`. A mistura original tinha 91 acertos. Corrigimos um erro sem perder acertos nessa reserva; o ganho é pequeno. A pontuação pública da mistura original é 0,84382. A nova regra ainda não foi enviada nesta execução.

### O que comparamos

- 69.822 médias ponderadas: pesos em passos de 2,5% e limites em passos de 0,5%, além da média exata de um terço por modelo.
- 7.074 votações com limites individuais, cobrindo todas as regras monotônicas não constantes de até três votos.
- 972 regras com mínimo, máximo e mediana dos apoios.
- 600 regras para discordâncias entre pares.
- 648 regras para discordâncias do trio.
- 210 regras conforme a ausência de glicose ou hemoglobina.

São 79.326 configurações, percorridas por completo nas primeiras três sementes. Regras diferentes podem produzir as mesmas previsões. Os três componentes ficam fixos durante a comparação das misturas; não mudamos K, os atributos da árvore ou a arquitetura da rede.

### Avaliação

Usamos a base padronizada de 520 amostras, com um registro por paciente. Mantemos 416 amostras para a escolha e 104 reservadas. O preenchimento e a normalização são ajustados apenas no treinamento de cada parte.

A busca ampla usa cinco partes de cada uma das sementes 42, 73 e 101. A segunda seleção compara 40 regras também nas sementes 21, 145 e 307. A indicação é escolhida pelo F1 macro médio das 30 partes das seis sementes. Empates favorecem menos componentes e regras mais simples.

As conferências usam as sementes 509 e 911 com inicialização 7 da rede, e a semente 42 com inicializações 19 e 31. A reserva é observada depois da escolha. Essas avaliações continuam usando pessoas da mesma base; a reserva também já foi consultada no projeto.

A busca por muitas regras favorece coincidências das divisões usadas na seleção. As conferências e os registros permitem acompanhar essa limitação, sem garantir o resultado no Kaggle.

### Registros da versão anterior

| Arquivo em `resultados/` | Conteúdo |
|---|---|
| `combinacoes_tres_cache.npz` | Apoios, votos, índices e partes de cada avaliação, além das previsões dos componentes no teste |
| `combinacoes_tres_busca.npz` | Catálogo completo das 79.326 regras e matrizes das primeiras 15 partes |
| `combinacoes_tres_selecao.npz` | Resultados das 40 candidatas nas 30 partes da seleção |
| `combinacoes_tres_escolha.json` | Regra escolhida, melhores pares e trio, protocolo e identificação da base |
| `combinacoes_tres_conferencias.npz` | Matrizes das conferências e da reserva |
| `combinacoes_tres_resumo.csv` | Resumo das regras de referência e selecionadas |
| `submissao_combinacao_escolhida.csv` | Indicação principal, com 312 linhas no formato `id,class` |
| `submissao_melhor_dupla.csv` | Melhor par da segunda seleção |
| `submissao_melhor_trio.csv` | Melhor trio; nesta execução é igual à indicação principal |

### Reprodução e referências

Usamos Python 3.12.14 e NumPy 2.3.5. As implementações estão incluídas no notebook. Executamos as células em ordem, a partir desta pasta ou da raiz do projeto. O registro das previsões evita repetir treinamentos idênticos. Se um componente mudar, precisamos mudar `versao_modelos` ou usar um novo registro.

Conferimos que os três componentes e a mistura original reproduzem os CSVs anteriores, linha por linha. As contagens da validação também coincidem com os registros anteriores dos componentes. A regra foi reaberta do JSON e reproduziu as 312 previsões da indicação principal.

As referências são a [mistura original](../Mod5_KNN_AD/01_Knn_arvore.ipynb), a [rede neural com atualização após cada exemplo](../Mod3_RN/02_Rede_neural_exemplo_a_exemplo.ipynb) e o [escopo das aulas](../docs/ESCOPO_AULAS.md). As novas misturas são propostas deste experimento, e não regras específicas atribuídas ao professor.
