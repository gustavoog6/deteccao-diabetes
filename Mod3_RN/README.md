# Rede neural

O desenvolvimento da versão que atualiza os pesos após cada exemplo está em [02_Rede_neural_exemplo_a_exemplo.ipynb](02_Rede_neural_exemplo_a_exemplo.ipynb). O notebook contém a implementação, a comparação das configurações e a preparação do arquivo para o Kaggle. As explicações ficam nas células Markdown e as saídas das execuções ficam salvas.

O [notebook 01](01_Rede_neural_aulas.ipynb) registra a comparação anterior, com atualização em lote. Cada versão gera seus próprios arquivos.

Construímos uma rede com uma camada oculta e uma saída, usando sigmoide, erro quadrático e retropropagação. A implementação usa NumPy para as contas, sem uma biblioteca de modelos prontos.

A rede já usa `(valor − média) / desvio padrão`, fórmula escolhida para todos os modelos das novas versões em 06/11/2026. Sua preparação e suas previsões foram conferidas na [comparação com escala comum](../Mod6_KNN_AD_RN/02_Combinacoes_escala_padrao.ipynb).

## Resultado da versão com atualização após cada exemplo

A configuração escolhida tem quatro entradas (`SYSTOLIC`, `GLUCOSE`, `HEMOGLOBIN` e `TRIGLYCERIDES`), 12 neurônios ocultos e uma saída. Usa mediana para os valores ausentes, normalização pela média e desvio padrão, taxa 0,1 e 800 épocas. A inicialização e o embaralhamento usam a semente 7.

O F1 macro médio foi **88,70%** na validação usada para escolher a configuração. Nas outras divisões e inicializações conferidas, ficou entre **88,20% e 88,67%**. Nas 104 amostras reservadas, acertou 89 casos: **85,58% de acurácia e de F1 macro**, com matriz `[[44, 6], [9, 45]]`. A meta de 0,87 no Kaggle ainda não foi verificada.

A busca teve 54 configurações iniciais e duas extensões de épocas. O resumo fica no começo do notebook e o registro está em [experimentos/EXP_001.md](experimentos/EXP_001.md).

## Referência das aulas

A [aula 6](../docs/materiais_aula/aula6_MD.pdf) apresenta a arquitetura, a sigmoide e a retropropagação. O notebook 02 segue a sequência de atualização após cada exemplo mostrada na página 17. No notebook 01, usamos a média dos gradientes dos exemplos e atualizamos os pesos uma vez por época; essa diferença está identificada como escolha de processamento daquele experimento.

Os grupos de atributos, as sementes, as taxas de aprendizado e as quantidades de épocas são escolhas desta implementação. As transformações e as referências das demais aulas estão registradas no próprio notebook e em [ESCOPO_AULAS.md](../docs/ESCOPO_AULAS.md).

## Dados e avaliação

- A base é `dados/treinamento_padronizado.csv`, com 520 amostras e um registro por paciente.
- Mantemos as mesmas 416 amostras de treinamento e 104 reservadas dos modelos anteriores.
- Escolhemos a configuração por F1 macro na validação cruzada com cinco partes, usando apenas as 416 amostras.
- O preenchimento dos vazios e os parâmetros de normalização são calculados somente no treinamento de cada divisão.
- Conferimos a escolha em outras divisões e inicializações, sem escolher a melhor semente pelo resultado.
- As 104 amostras reservadas já foram consultadas em outros experimentos. Seu resultado é uma comparação local.
- Depois de fixar a configuração, treinamos com as 520 amostras para prever as 312 linhas do teste do Kaggle.

## Arquivos gerados

| Arquivo em `resultados/` | Conteúdo |
|---|---|
| `rede_neural_exemplos_busca.npz` | Configurações e matrizes por divisão da atualização após cada exemplo |
| `rede_neural_exemplos_busca_inicial.npz` | Primeira comparação, antes de acrescentar 800 e 1.600 épocas |
| `rede_neural_exemplos_modelo.npz` | Pesos e preparação dos atributos dessa versão |
| `submissao_rede_neural_exemplos.csv` | Previsões da atualização após cada exemplo, no formato `id,class` |
| `rede_neural_aulas_busca.npz` | Busca da atualização em lote |
| `rede_neural_aulas_modelo.npz` | Pesos e preparação dos atributos da atualização em lote |
| `submissao_rede_neural_aulas.csv` | Previsões da atualização em lote para comparação |

## Como executar

Usamos Python e NumPy. Selecionamos no notebook um kernel que tenha NumPy instalado e executamos as células em ordem, a partir da raiz do projeto ou desta pasta. A busca completa pode demorar vários minutos. Os arquivos de entrada permanecem na pasta `dados/`.

O arquivo de submissão é gerado ao final. O notebook também reabre o modelo salvo e verifica se ele reproduz as previsões. O resultado no Kaggle só será conhecido depois do envio.


