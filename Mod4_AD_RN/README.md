# Árvore de decisão + rede neural

## Objetivo

Avaliar Árvore de decisão + rede neural para classificação de controle (0) e diabetes (1), seguindo o protocolo em [metodologia](../docs/METODOLOGIA.md).

## Situação atual

Estrutura inicial. Nenhum treinamento ou resultado disponível.

## Organização

- 01_desenvolvimento.ipynb: notebook fonte, organizado por etapas.
- experimentos/catalogo.csv: índice de todas as execuções.
- experimentos/TEMPLATE.md: ficha a copiar para cada execução.
- experimentos/EXP_001/: exemplo de nome para uma futura pasta local de execução, contendo ficha, configuração, métricas por divisão e gráficos.

## Questões específicas

Definir votação por probabilidades ou stacking. Justificar pesos e validar a combinação sem vazamento.

## Procedimento

1. Declarar hipótese e configuração antes de executar.
2. Usar os dados e as partições compartilhadas da raiz; não duplicar a base aqui.
3. Executar pré-processamento e ajuste apenas dentro do treinamento de cada divisão.
4. Registrar métricas e matriz de confusão por divisão, ambiente, sementes e duração.
5. Preencher a ficha e o catálogo, inclusive para execuções que falharem.
6. Atualizar a comparação consolidada quando houver resultados comparáveis.

Os caminhos do notebook devem ser relativos à raiz identificada explicitamente. Não depender de células executadas fora de ordem. Remover saídas sensíveis antes de compartilhar ou versionar o notebook fonte.


