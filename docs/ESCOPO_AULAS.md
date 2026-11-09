# Conteúdo de aula como referência do projeto

Em 05/11/2026, decidimos usar no trabalho apenas métodos apresentados nas aulas enviadas pelo professor. Essa é uma escolha de escopo do aluno. As referências abaixo indicam o que encontramos no material, sem atribuir ao professor restrições que ele não escreveu.

Os 12 PDFs recebidos estão em `docs/materiais_aula/`. As páginas citadas são as posições no arquivo PDF, contando a capa. A numeração no rodapé de alguns slides é diferente.

## Decisões de 06/11/2026

O aluno definiu a fórmula `(valor − média) / desvio padrão` para todos os modelos das novas comparações. Essa fórmula aparece na aula 10, página 16. Os parâmetros são calculados somente no treinamento de cada parte. O notebook [02_Combinacoes_escala_padrao.ipynb](../Mod6_KNN_AD_RN/02_Combinacoes_escala_padrao.ipynb) aplica a decisão ao KNN, à árvore e à rede e repete a comparação das misturas. As experiências anteriores ficam como histórico das outras escalas.

O aluno também solicitou testar Random Forest. Tratamos esse pedido como uma extensão do escopo das árvores, com referência técnica própria no [notebook da floresta](../Mod7_RF/01_Random_forest.ipynb). Identificamos separadamente o sorteio de atributos por nó e a variante que considera todos os atributos, chamada bagging. As escolhas da floresta são documentadas como decisões deste experimento.

## Referências para o KNN

| Parte do trabalho | O que aparece no material | Referência |
|---|---|---|
| Funcionamento do KNN | Guardar os exemplos, calcular a proximidade, buscar os K vizinhos e escolher a classe mais frequente | [Aula 5](materiais_aula/aula5_MD.pdf), páginas 11 a 14 |
| Normalização no exemplo de KNN | Subtrair o mínimo do atributo e dividir pela diferença entre máximo e mínimo | Aula 5, página 12 |
| Distância no exemplo de KNN | Euclidiana | Aula 5, página 12 |
| Outras distâncias | Manhattan e Minkowski, além da Euclidiana | [Aula 3](materiais_aula/aula3_MD.pdf), páginas 12 a 15 |
| Categorias binárias | Coeficiente de igualdade simples e Jaccard | Aula 3, páginas 19 a 22 |
| Conversão para variáveis binárias | Binarização de atributos contínuos ou categóricos | [Aula 2](materiais_aula/aula2_MD.pdf), página 91 |
| Valores ausentes | Eliminar registros ou atributos, estimar valores ou ignorar valores ausentes | Aula 2, páginas 44 a 47 e 52 |
| Seleção e criação de atributos | São abordadas no pré-processamento | Aula 2, seção de pré-processamento |
| Média e mediana | Medidas de localização, com observação sobre a sensibilidade da média a valores extremos | [Aula 4](materiais_aula/aula4_MD.pdf), página 9 |
| Outra normalização | Subtrair a média e dividir pelo desvio padrão, no exemplo de altura e peso | [Aula 10](materiais_aula/aula10_MD.pdf), página 16 |
| Avaliação | Holdout e validação cruzada em K partes | [Aula 7](materiais_aula/aula7_MD.pdf), páginas 7 e 8 |
| Métricas | Matriz de confusão, acurácia, precisão, recall e medida F | Aula 7, páginas 10 e 11 |

## Diferenças em relação às versões exploratórias

Os notebooks anteriores registram experimentos feitos antes desta decisão de escopo. Alguns componentes vieram de escolhas de implementação e de buscas exploratórias.

| Componente usado nos testes | Como fica no novo escopo |
|---|---|
| Escala MAD com fator 1,4826 | Não identificamos a fórmula específica nos slides. A aula 4 menciona outras medidas de dispersão, mas não apresenta essa normalização. Usar uma normalização explicitamente mostrada. |
| Escala pela diferença entre quartis | Não identificamos essa fórmula de normalização no material. Preferir mínimo e máximo ou média e desvio padrão. |
| Peso 2 ou 3 para exames | Não identificamos esses pesos no KNN apresentado. Começar com a fórmula de distância sem pesos especiais por atributo. |
| Conversão D / (1 + D) | Não identificamos essa fórmula específica nos slides. Usar diretamente a distância escolhida na versão inicial alinhada à aula. |
| Mistura numérica e categórica com 90% e 10% | Os slides apresentam medidas para tipos de dados, mas não identificamos essa combinação e esses pesos. Precisará de uma justificativa separada antes de entrar na versão de aula. |
| Nove votos em 19 para prever diabetes | A aula usa a classe mais frequente. Com 19 vizinhos e duas classes, a maioria exige pelo menos 10 votos. |
| Votos inversos à distância ou voto duplo | Não identificamos essas regras nos slides de KNN. Usar voto simples. |
| Validação cruzada aninhada e busca de 54.225 combinações | O material apresenta holdout e validação cruzada comum. A busca ampla fica registrada como exploração anterior à decisão de escopo. |

As regras de padronização da base, como converter altura para centímetros ou separar a pressão, são decisões sobre os dados do trabalho. Precisamos explicá-las como nossas decisões, em vez de apresentá-las como fórmulas específicas fornecidas pelo professor. O mesmo vale para escolher a mediana como estimativa de um valor ausente.

## Proposta para a próxima versão

Seguir primeiro o exemplo da aula 5, página 12, com atributos numéricos, normalização pelo mínimo e máximo calculados no treinamento, distância Euclidiana e voto simples. Comparar alguns valores de K por validação cruzada, como na aula 7. Manhattan pode entrar em uma comparação posterior, com referência à aula 3.

As métricas exigidas pela competição, incluindo F1 macro, continuam sendo registradas. O macro é a média dos resultados das duas classes. A decisão sobre estimativa dos valores ausentes deve ficar explícita e ser calculada apenas nas amostras de treinamento de cada divisão.

## Aplicação à árvore de decisão

No notebook `Mod2_AD/02_Arvore_busca_aulas.ipynb`, usamos ganho de informação e testes binários. A aula 5 apresenta árvores, a busca de árvores compactas e a escolha por ganho de informação. A aula 2 apresenta discretização supervisionada e binarização. A aplicação desses conceitos para varrer cortes numéricos em cada nó é uma adaptação da implementação, distinguida do ID3 categórico do primeiro notebook de árvore. O limite de profundidade, o mínimo de exemplos por folha e a simplificação de ramos com a mesma resposta também estão identificados como escolhas nossas.

## Aplicação à rede neural

No notebook [Mod3_RN/01_Rede_neural_aulas.ipynb](../Mod3_RN/01_Rede_neural_aulas.ipynb), construímos uma rede com uma camada oculta. A aula 6 apresenta a soma ponderada e o viés (página 6), a sigmoide (7), a alimentação direta (9, 10 e 12), a saída binária com limite 0,5 (11), o erro quadrático e o gradiente (15 e 16), as épocas (17), a escolha da quantidade de neurônios por validação cruzada (19) e a retropropagação (21 a 23).

O slide 17 descreve uma atualização dos pesos após cada exemplo. O notebook 01 calcula a média dos gradientes dos exemplos de treinamento e atualiza os pesos uma vez por época. Essa atualização em lote é uma diferença de processamento daquele experimento; não a apresentamos como a sequência literal do slide.

O notebook [Mod3_RN/02_Rede_neural_exemplo_a_exemplo.ipynb](../Mod3_RN/02_Rede_neural_exemplo_a_exemplo.ipynb) aplica a sequência de atualização após cada exemplo. Mantém uma camada oculta, a sigmoide, o erro quadrático e a retropropagação. A normalização pela média e desvio padrão e o preenchimento pela mediana são calculados somente no treinamento de cada divisão. Os grupos de atributos, a inicialização aleatória, o embaralhamento por época, as taxas e as quantidades de épocas comparadas são escolhas nossas para aplicar os conceitos.

## Combinações de KNN, árvore e rede neural

O [notebook de combinações](../Mod6_KNN_AD_RN/01_Combinacoes.ipynb) mantém os três componentes fixos e compara pares e trio. Usa a implementação do primeiro KNN K=11, a árvore de quatro atributos e a rede com atualização após cada exemplo. As escolhas exploratórias presentes no primeiro KNN continuam identificadas nos registros anteriores.

A busca compara médias ponderadas, limites de decisão, votação, mínimo, máximo e mediana dos apoios, regras de discordância e regras conforme a ausência de exames. Essas formas de combinar as respostas são hipóteses deste experimento, com autorização do aluno para comparar os modelos, e ficam identificadas como escolhas nossas. A referência das aulas permanece nos algoritmos componentes e no protocolo de avaliação.

Os apoios usados na combinação são a fração dos vizinhos de diabetes, a proporção de diabetes na folha e a saída sigmoide da rede. São respostas operacionais dos modelos e não probabilidades calibradas. A seleção e as conferências estão separadas no notebook, com registro completo das 79.326 configurações da grade.

## Material recebido

| Aula | Tema principal |
|---|---|
| 1 | Introdução à mineração de dados |
| 2 | Dados, qualidade e pré-processamento |
| 3 | Similaridade e dissimilaridade |
| 4 | Exploração dos dados |
| 5 | Classificação, KNN e árvore de decisão |
| 6 | Redes neurais |
| 7 | Avaliação de classificadores e regressores |
| 8 | Regras de associação |
| 9 | Agrupamento e K-médias |
| 10 | Agrupamento hierárquico |
| 11 | Agrupamento por densidade e DBSCAN |
| 12 | Avaliação de agrupamentos |
