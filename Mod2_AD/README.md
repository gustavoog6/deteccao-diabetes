# Árvore de decisão

## Objetivo

Avaliar Árvore de decisão para classificação de controle (0) e diabetes (1), seguindo o protocolo em [metodologia](../docs/METODOLOGIA.md).

## Situação atual

A versão com média e desvio padrão, definida em 06/11/2026, está em [02_Combinacoes_escala_padrao.ipynb](../Mod6_KNN_AD_RN/02_Combinacoes_escala_padrao.ipynb). Os parâmetros são calculados no treinamento de cada parte. As previsões reproduzem as da árvore anterior, com os cortes expressos na nova escala.

O desenvolvimento da árvore está em [02_Arvore_busca_aulas.ipynb](02_Arvore_busca_aulas.ipynb). Ele usa uma única árvore com ganho de informação e testes binários, aplicando os conceitos de binarização, seleção de atributos e árvores compactas das aulas. A varredura de cortes numéricos e os limites de tamanho são escolhas da implementação, identificadas no notebook.

A grade inicial comparou 576 configurações. A busca ampliada comparou 57.232 combinações de atributos, preenchimento, mínimo de exemplos por folha e profundidade. A candidata usa pressão sistólica, glicose, hemoglobina e triglicerídeos, preenchimento pela média, mínimo de 15 exemplos por folha e profundidade máxima 6.

| Avaliação da candidata | Acurácia | F1 macro |
|---|---:|---:|
| Média das divisões usadas na escolha, sementes 42 e 73 | 90,39% | 90,37% |
| Conferência com semente 101 | 88,24% | 88,23% |
| Reserva de 104 amostras | 84,62% | 84,61% |

A candidata acertou 88 das 104 amostras reservadas. Após juntar caminhos que retornam a mesma classe, a árvore tem seis perguntas e sete folhas, com no máximo cinco perguntas por previsão. As previsões foram conferidas antes e depois dessa simplificação. O registro completo das configurações está em `resultados/arvore_busca_aulas.npz`.

O notebook também registra a inclusão de tabagismo, atividade física, histórico familiar e IMC binário, que manteve os resultados com os limites de tamanho fixos. A seção final gera `resultados/submissao_arvore_4_atributos.csv` com as 520 amostras rotuladas como referência e 312 previsões para o teste. Os limites da árvore são recalculados nesse ajuste final.

## Primeira implementação

O notebook [01_Arvore_aulas.ipynb](01_Arvore_aulas.ipynb) implementa uma árvore do zero com ganho de informação, seguindo o ID3 da aula 5. As medidas numéricas são discretizadas em faixas de mesma largura, uma escolha de implementação baseada no conceito de discretização da aula 2. As categorias permanecem como atributos categóricos.

Na execução de 05/11/2026, foram comparados quatro grupos de atributos e quatro quantidades de faixas, nas mesmas cinco divisões do KNN. A configuração escolhida usou glicose, hemoglobina e triglicerídeos, com dez faixas por medida. Nas 104 amostras reservadas, a árvore acertou 66, com acurácia de 63,46% e F1 macro de 63,12%. O KNN comparado acertou 88, com acurácia de 84,62%.

A árvore acertou apenas uma amostra que o KNN errou. O notebook registra essa comparação para discutir a combinação. As amostras reservadas já foram consultadas em experimentos anteriores e servem como referência local.

## Organização

- [02_Arvore_busca_aulas.ipynb](02_Arvore_busca_aulas.ipynb): busca de cortes e atributos, avaliações, explicações e árvore final em texto.
- [01_Arvore_aulas.ipynb](01_Arvore_aulas.ipynb): construção, comparação de configurações e avaliação da árvore, com referências às aulas e explicações em Markdown.
- [experimentos/TEMPLATE.md](experimentos/TEMPLATE.md): modelo de ficha de experimento.

## Questões específicas

Investigar profundidade, critério, tamanho mínimo das folhas e regularização.

## Procedimento

1. Declarar hipótese e configuração antes de executar.
2. Usar os dados e as partições compartilhadas da raiz; não duplicar a base aqui.
3. Executar pré-processamento e ajuste apenas dentro do treinamento de cada divisão.
4. Registrar métricas e matriz de confusão por divisão, ambiente, sementes e duração.
5. Preencher a ficha e o catálogo, inclusive para execuções que falharem.
6. Atualizar a comparação consolidada quando houver resultados comparáveis.

Os caminhos do notebook devem ser relativos à raiz identificada explicitamente. Não depender de células executadas fora de ordem. Remover saídas sensíveis antes de compartilhar ou versionar o notebook fonte.


