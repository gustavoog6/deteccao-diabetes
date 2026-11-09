# Comparação consolidada

`comparacao.csv` terá uma linha por configuração e protocolo de validação. Incluir somente execuções rastreáveis nos catálogos dos modelos e comparáveis sob o mesmo protocolo. Manter resultados por divisão dentro da pasta do experimento.

Campos de desvio padrão ficam vazios quando houver uma única divisão. Pontuações de submissões devem ser registradas separadamente, com data, arquivo, configuração e descrição da avaliação.

## Combinações de KNN, árvore e rede neural

O registro desta busca está em [Mod6_KNN_AD_RN](../Mod6_KNN_AD_RN/README.md). A indicação principal é [submissao_combinacao_escolhida.csv](submissao_combinacao_escolhida.csv). O catálogo completo das regras e as matrizes estão nos arquivos `combinacoes_tres_*`; o resumo legível está em [combinacoes_tres_resumo.csv](combinacoes_tres_resumo.csv).

## Versões com média e desvio padrão — 06/11/2026

A nova comparação dos três modelos está em `combinacoes_zscore_*`, com o CSV [submissao_combinacao_zscore.csv](submissao_combinacao_zscore.csv). Os arquivos `combinacoes_tres_*` registram a experiência anterior com quartis no KNN.

A floresta está documentada em [Mod7_RF](../Mod7_RF/README.md). Os CSVs são [Random Forest](submissao_random_forest.csv) e [bagging](submissao_bagging.csv). A indicação pela validação está em [submissao_floresta_escolhida.csv](submissao_floresta_escolhida.csv), que nesta execução é igual ao bagging. Os registros das buscas e conferências estão nos arquivos `random_forest_*`.
