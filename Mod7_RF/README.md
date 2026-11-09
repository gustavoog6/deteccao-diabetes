# Random Forest e bagging

O [notebook 01_Random_forest.ipynb](01_Random_forest.ipynb) contém a implementação com NumPy, explicações, busca e saídas executadas. Usamos média e desvio padrão para a escala de todas as entradas, com ajuste apenas no treinamento de cada parte.

## Resultados

| Variante | F1 na seleção | F1 médio nas conferências 509 e 911 | F1 na reserva |
|---|---:|---:|---:|
| Random Forest, sorteio de atributos | 89,73% | 89,38% | 82,63% |
| Bagging, todos os atributos por nó | 90,30% | 89,51% | 87,49% |

Random Forest: 300 árvores; nove medidas; vazios pela mediana; mínimo de 2 por folha; profundidade sem limite fixo; apoio por folha; limite 50%. Bagging: 100 árvores; quatro medidas; vazios pela mediana; mínimo de 2 por folha; profundidade 6; apoio por folha; limite 50%.

A Random Forest sorteia os atributos por nó. A variante bagging considera todos os atributos por nó e sorteia os exemplos com reposição. A seleção indicou **bagging**, conforme o F1 macro médio das 15 partes usadas para escolher. A reserva não trocou a escolha.

## Arquivos para envio

- [submissao_random_forest.csv](../resultados/submissao_random_forest.csv): variante com sorteio de atributos.
- [submissao_bagging.csv](../resultados/submissao_bagging.csv): variante com todos os atributos por nó.
- [submissao_floresta_escolhida.csv](../resultados/submissao_floresta_escolhida.csv): cópia da variante indicada pela seleção.

Cada arquivo tem 312 linhas, cabeçalho `id,class` e os IDs do teste na ordem original. Os modelos foram reabertos e reproduziram as previsões.

## Comparação e protocolo

A busca inicial contém 64 trajetórias: quatro grupos de atributos, média ou mediana para os vazios, mínimo de duas ou oito amostras por folha, profundidade 6 ou sem limite e duas opções de atributos por nó. Observamos 30 e 100 árvores, dois tipos de apoio e limites 0,45, 0,5 e 0,55, totalizando 768 configurações iniciais.

A segunda seleção inclui candidatas de destaque, o melhor grupo de cada conjunto de atributos e quatro candidatas com sorteio. Estendemos para 300 árvores as quatro trajetórias mais bem avaliadas e a melhor com sorteio quando ela ainda não estava no grupo.

Usamos 416 amostras para selecionar e 104 reservadas. A busca inicial usa a semente 42; a segunda seleção usa 42, 73 e 101. As conferências usam 509 e 911, além da divisão 42 com semente 97 da floresta. A semente final da floresta permanece 7. Essas divisões usam as mesmas pessoas; a reserva já foi consultada em outros experimentos.

## Registros e reprodução

- `resultados/random_forest_busca_inicial.npz`: configurações, previsões da validação e matrizes iniciais.
- `resultados/random_forest_selecao.npz`: candidatas e matrizes da segunda seleção.
- `resultados/random_forest_conferencias.npz`: conferências e reserva das duas variantes.
- `resultados/random_forest_modelo.json` e `bagging_modelo.json`: preparação, árvores e configuração de cada variante.
- `resultados/floresta_escolhida.json`: identificação da indicação pela seleção.

Usamos Python 3.12.14 e NumPy 2.3.5. As células devem ser executadas em ordem, a partir da raiz do projeto ou desta pasta. Os cortes foram conferidos contra cálculo independente do ganho de informação. Verificamos conservação dos exemplos nos nós, profundidade, reprodução das sementes, prefixo das florestas e a fórmula da escala.

## Referências e escolhas

O teste da floresta foi solicitado pelo aluno como uma extensão das árvores do trabalho. A [documentação técnica](https://scikit-learn.org/stable/modules/ensemble.html#forest) descreve o método, e a [referência de parâmetros](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) apoia a comparação das configurações. A implementação própria usa entropia, amostragem com reposição e seleção de atributos por nó. Cada aparição no sorteio conta como exemplo na árvore.

As aulas 5, 7 e 10 sustentam as árvores, a avaliação e a fórmula da escala. As regras e os resultados estão detalhados no notebook.
