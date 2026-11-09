# Combinação de KNN e árvore

O notebook [01_Knn_arvore.ipynb](01_Knn_arvore.ipynb) combina o primeiro KNN K=11 enviado ao Kaggle, com pontuação pública 0,82897, e a árvore de quatro atributos, com pontuação pública 0,83018.

O apoio do KNN é a fração dos 11 vizinhos da classe diabetes. O apoio da árvore é a fração de exemplos de diabetes na folha alcançada. A regra escolhida tira a média dos dois apoios. Acima de 0,5, prevê diabetes. Abaixo de 0,5, prevê controle. Em empate, usa a classe do KNN.

A regra de combinação é uma proposta deste experimento. O notebook distingue essa escolha dos algoritmos apresentados separadamente nas aulas.

## Resultado no Kaggle

O arquivo `submissao_knn11_arvore.csv` recebeu **0,84382** no placar público, conforme a captura enviada pelo aluno. Superou o primeiro KNN K=11 (0,82897) e a árvore separada (0,83018), mas ficou abaixo da meta de 0,87. Essa pontuação corresponde à mistura original, com metade do peso para cada modelo e limite de 50%, e não à rede neural.

## Resultados locais

| Avaliação | KNN K=11 | Árvore | Combinação |
|---|---:|---:|---:|
| Acurácia média nas divisões de escolha | 86,66% | 90,39% | 91,11% |
| F1 macro médio nas divisões de escolha | 86,63% | 90,37% | 91,09% |
| Acurácia na semente de conferência 101 | 86,07% | 88,24% | 89,21% |
| Acurácia nas 104 amostras reservadas | 86,54% | 84,62% | 87,50% |
| Acertos nas 104 amostras reservadas | 90 | 88 | 91 |

As amostras e as divisões já foram usadas nos experimentos anteriores. A reserva é uma comparação local já consultada. A combinação corrigiu sete erros do KNN e perdeu seis acertos, com saldo de um acerto a mais.

## Ajustes posteriores

O notebook compara mais 25 regras de mistura, variando o peso da árvore, o limite para prever diabetes, a preferência por apoio mais forte e a disponibilidade de glicose e hemoglobina. A regra escolhida nessa etapa mantém metade do peso para cada modelo e usa limite de 45%.

A acurácia média nas divisões usadas para escolher passou de 91,11% para 91,95%. A média de três conferências passou de 90,40% para 90,72%. Nas 104 amostras reservadas, porém, caiu de 87,50% para 84,62%, com três novos erros de controle. A mistura original com limite de 50% continua como referência local. O registro completo desse teste está em `resultados/knn11_arvore_ajustes.npz`.

## Reprodução e submissão

As saídas estão salvas no notebook. Para reexecutar, usar um kernel Python com NumPy e executar as células em ordem a partir da raiz do projeto ou da pasta deste modelo.

O notebook confere que as previsões individuais no teste são idênticas aos arquivos anteriormente enviados. Depois grava `resultados/submissao_knn11_arvore.csv`, com 312 previsões e as colunas `id,class`. Cada componente é reajustado com as 520 amostras rotuladas. O registro das regras, pesos e métricas por divisão está em `resultados/knn11_arvore.npz`.
