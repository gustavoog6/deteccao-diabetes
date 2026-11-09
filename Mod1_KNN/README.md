# KNN

## Objetivo

Avaliar KNN para classificação de controle (0) e diabetes (1), seguindo o protocolo em [metodologia](../docs/METODOLOGIA.md).

## Situação atual

A versão com a escala definida em 06/11/2026 está em [02_Combinacoes_escala_padrao.ipynb](../Mod6_KNN_AD_RN/02_Combinacoes_escala_padrao.ipynb). Mantém K=11 e as demais decisões da primeira submissão, usando `(valor − média) / desvio padrão` nos atributos numéricos, com parâmetros ajustados no treinamento de cada parte. Na reserva, o F1 foi 75,94%; a versão anterior com quartis tinha 86,53%. O novo CSV é `resultados/submissao_knn_zscore.csv`.

As experiências anteriores com referência de aula estão em [04_Knn_aulas.ipynb](04_Knn_aulas.ipynb), com o exemplo inicial, e [05_Knn_selecao_aulas.ipynb](05_Knn_selecao_aulas.ipynb), com seleção de atributos. Elas registram as escalas e decisões usadas naquelas execuções.

Na execução de 05/11/2026, K igual a 11 teve o maior F1 macro médio, de 72,24%. Nas 104 amostras reservadas, o modelo acertou 67, com acurácia de 64,42% e F1 macro de 64,02%. Essas amostras já foram consultadas em experimentos anteriores e servem como referência local.

As fórmulas de aula e as decisões sobre a base estão distinguidas no notebook. O mapa de referências está em [ESCOPO_AULAS.md](../docs/ESCOPO_AULAS.md).

A seleção posterior comparou 32.704 combinações numéricas e 16.384 com categorias binarizadas. A candidata escolhida usa glicose, hemoglobina e triglicerídeos, mínimo e máximo, Manhattan e K igual a 9. A acurácia média foi de 86,06% nas cinco divisões de escolha e 85,10% na repetição com outra semente. Nas mesmas 104 amostras reservadas, acertou 88, com acurácia de 84,62% e F1 macro de 84,56%. A meta de 90% continua em aberto.

## Organização

- [04_Knn_aulas.ipynb](04_Knn_aulas.ipynb) — versão alinhada ao exemplo de aula, com explicações e saídas executadas.
- [05_Knn_selecao_aulas.ipynb](05_Knn_selecao_aulas.ipynb) — seleção de atributos, binarização de categorias e comparações de escala, distância e K.
- [03_Knn_busca_ampla.ipynb](03_Knn_busca_ampla.ipynb) — registro da busca ampla anterior à decisão de usar apenas conteúdo de aula.
- [02_Knn_numerico.ipynb](02_Knn_numerico.ipynb) — desenvolvimento anterior do KNN numérico e misto, com testes e submissões.
- [01_Knn.ipynb](01_Knn.ipynb) — desenvolvimento inicial com atributos categorizados.
- [experimentos/TEMPLATE.md](experimentos/TEMPLATE.md) — modelo de ficha de experimento.

## Questões específicas

Investigar número de vizinhos, distância, ponderação e escalonamento.

## Procedimento

1. Declarar hipótese e configuração antes de executar.
2. Usar os dados e as partições compartilhadas da raiz; não duplicar a base aqui.
3. Executar pré-processamento e ajuste apenas dentro do treinamento de cada divisão.
4. Registrar métricas e matriz de confusão por divisão, ambiente, sementes e duração.
5. Preencher a ficha e o catálogo, inclusive para execuções que falharem.
6. Atualizar a comparação consolidada quando houver resultados comparáveis.

Os caminhos do notebook devem ser relativos à raiz identificada explicitamente. Não depender de células executadas fora de ordem. Remover saídas sensíveis antes de compartilhar ou versionar o notebook fonte.


