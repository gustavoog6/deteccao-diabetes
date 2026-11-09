# Metodologia de experimentação

## Comparação justa

Todos os modelos devem usar as mesmas partições quando comparados diretamente. Os registros em `resultados/` guardam índices, partes, sementes e a identificação da base para as avaliações executadas. Não duplicar a base em cada pasta de modelo.

Na base padronizada atual, temos 520 amostras e um registro por paciente. A divisão estratificada de semente 42 mantém 416 amostras para escolha e 104 reservadas. Comparamos configurações por validação cruzada estratificada em cinco partes nas sementes declaradas por experimento. As 104 amostras já foram consultadas no projeto e são uma comparação local. Se surgirem várias medições do mesmo paciente, o paciente deve ficar inteiramente em um lado de cada divisão.

Experimentos com diferentes partições são permitidos e devem ser planejados e registrados. Não escolher uma semente apenas por produzir o melhor resultado. Uma configuração deve ser avaliada nas divisões previstas, com média e desvio padrão quando houver múltiplas divisões. Ajuste de hiperparâmetros e estimativa final de desempenho devem ser separados; caso adotemos validação cruzada para ambos, considerar validação aninhada.

## Prevenção de vazamento

- O teste da competição não participa de treinamento, validação ou escolha de configuração.
- Imputação, escalonamento, seleção de atributos, PCA e outras transformações aprendidas são ajustadas apenas no treinamento de cada divisão, preferencialmente dentro de um pipeline.
- Reamostragem, se necessária, ocorre somente no treinamento de cada divisão.
- Identificadores de paciente ou amostra não viram atributos automaticamente.
- Não buscar rótulos do teste em fontes externas.
- Se houver stacking, suas entradas de treinamento devem ser previsões fora da amostra, produzidas sem treinar no próprio exemplo previsto.

## Escala das entradas a partir de 06/11/2026

Por decisão do aluno, as novas versões usam `(valor − média) / desvio padrão` em todos os modelos. A média e o desvio padrão amostral, com `ddof=1`, são calculados somente nos valores disponíveis do treinamento de cada parte. Aplicamos esses mesmos parâmetros à avaliação e ao teste. Uma coluna constante é transformada em zero.

O preenchimento de valores ausentes continua sendo uma decisão separada da escala. O KNN e a rede usam mediana; a árvore simples usa média; a busca da floresta compara ambas. No teste com categorias binarizadas, suas colunas também recebem a fórmula, com parâmetros calculados no treinamento.

O CSV padronizado conserva as unidades da exploração. O ajuste da escala acontece dentro de cada treinamento, para acompanhar suas divisões. Os notebooks anteriores registram outras escalas como histórico. As novas versões e seus resultados são identificados separadamente.

## Métricas

Registrar F1-macro, precisão, recall de diabetes (classe 1), recall de controle (classe 0), matriz de confusão e suporte por classe. A proposta inicial é selecionar por F1-macro e analisar os recalls em conjunto.

Em 06/11/2026, conferimos a página da competição: a avaliação pede precisão, recall de diabetes, recall de controle e F1 macro, e a identificação do placar é `F-Score (Macro)`. Acurácia e pontuação do placar devem ser nomeadas separadamente. A agregação de “Precisão” continua sem detalhamento nessa descrição; registrar precisão por classe e macro, com nomes explícitos.

Registrar a ordem das classes na matriz de confusão como `[0, 1]`. Mudanças de limiar são hiperparâmetros e devem ser escolhidas somente dentro da validação apropriada.

## Reprodutibilidade

- Registrar sementes da divisão e dos modelos estocásticos separadamente.
- Salvar índices e associá-los à versão da base e a identificadores estáveis.
- Registrar versões de Python e bibliotecas, configuração completa e versão do código.
- Executar notebooks do início ao fim em kernel limpo.
- Medir tempo de treinamento e predição quando útil para comparação.
- Salvar resultados por divisão antes de calcular o resumo.
- Tratar pontuações de submissão como avaliação externa ao protocolo local; não usá-las como ciclo repetido de ajuste.

## Dados restritos

Não publicar dados, índices identificáveis, modelos treinados ou saídas contendo informações de pacientes. Arquivos de dados, partições, notebooks executados e artefatos experimentais foram excluídos do versionamento por padrão. A pasta de entrega deve ter acesso restrito ao público autorizado da disciplina. Revisar saídas antes de qualquer compartilhamento.
