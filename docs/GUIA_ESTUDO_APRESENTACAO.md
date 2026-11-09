# Guia de estudo — Apresentação Detecção de Diabetes

Atualizado em 08/11/2026.

## Como usar este guia

Este guia segue os 38 slides da versão Trab\_MDados.pptx, um bloco por slide. Cada bloco tem quatro partes:

- **O que mostra:** o que está na tela.
- **O que falar:** a ideia central, em poucas frases.
- **Para estudar:** os conceitos por trás, com os números que vale saber de cor.
- **Se perguntarem:** a pergunta mais provável do professor e uma resposta curta.

Os números de validação são da validação cruzada 5 partes × 4 repetições, só no treino. Os do Kaggle são do placar público. O resumo de uma linha da apresentação: **mexer no modelo levou a 0,84; mexer nos dados levou a 0,899.**

| Parte | Slides | Assunto |
| --- | --- | --- |
| Abertura | 1 e 2 | Equipe e o gráfico-resumo das submissões |
| 01 O problema e os dados | 3 a 6 | Tarefa, métrica F1-macro, sujeira da base |
| 02 Primeiras tentativas | 7 a 9 | Quatro envios abaixo do baseline e o sobreajuste |
| 03 Ajuste: olhar os dados | 10 a 24 | Unidades, exames ausentes, submodelos, voto, as 6 etapas |
| 04 Os três modelos e o voto | 25 a 36 | Validação cruzada, KNN, árvore, rede e matriz de confusão |
| Encerramento | 37 e 38 | Pontos de atenção e perguntas |

## Abertura e Parte 01: o problema e os dados (slides 1 a 6)

### Slide 1: Detecção de Diabetes

**O que mostra:** título, os três integrantes (Gustavo, Higor e Vitória), a disciplina e o professor.

**O que falar:** apresentar o grupo e o trabalho em cerca de 20 segundos. O trabalho é a competição "deteccao-de-diabetes" no Kaggle da turma.

### Slide 2: Pipeline

**O que mostra:** um vídeo com a nota no Kaggle de cada uma das 7 submissões, em ordem, e a linha tracejada do baseline do professor (0,872).

| # | Submissão | Kaggle | O que mudou |
| --- | --- | --- | --- |
| 1 | KNN K=11 | 0,829 | Peso maior para glicose e HbA1c |
| 2 | KNN sem glicose ausente | 0,806 | Glicose fora da distância quando faltava |
| 3 | Árvore | 0,830 | 4 atributos |
| 4 | KNN + árvore | 0,844 | Média dos apoios dos dois |
| 5 | KNN com unidades corrigidas | 0,857 | Glicose e HbA1c na mesma unidade |
| 6 | Média dos 3 | 0,866 | KNN, árvore e rede juntos |
| 7 | Voto por padrão de exames | **0,899** | Um submodelo para cada combinação de exames |

**O que falar:** este gráfico é o resumo do trabalho. Nas quatro primeiras mexemos no modelo e ficamos entre 0,80 e 0,85. Nas três últimas mexemos nos dados e passamos do baseline.

**Para estudar:** saiba a ordem das 7 submissões e por que a 2 piorou. Tirar a glicose da distância fazia o diabético sem glicose ser comparado só pela HbA1c e pelos clínicos, e ele parecia saudável.

**Se perguntarem** "qual foi o maior salto?": a correção das unidades (0,844 → 0,857) e o tratamento dos exames ausentes (0,866 → 0,899). Os dois foram mudanças nos dados, não no modelo.

### Slide 3: Seção 01, o problema e os dados

**O que mostra:** abertura da primeira parte, com os tópicos: a tarefa, como o desempenho é medido e como a base veio.

**O que falar:** uma frase de transição: primeiro, o que tinha que ser feito e como estavam os dados.

### Slide 4: Classificar 312 pacientes com só 520 de exemplo

**O que mostra:** quatro cartões (520 no treino, 312 no teste, 2 classes, F1-macro), as regras da competição e um quadro com a fórmula do F1.

**O que falar:** era classificar cada paciente em controle (0) ou diabetes (1). O placar usa o F1-macro, então o modelo só vai bem se acertar os doentes e os saudáveis. Regras: partir de KNN, árvore e rede, nunca usar o teste para escolher nada, e o professor ainda avalia num conjunto externo.

**Para estudar, as fórmulas do quadro:**

```latex
\text{precisão} = \frac{VP}{VP + FP} \qquad \text{recall} = \frac{VP}{VP + FN}
```

```latex
F1 = \frac{2 \times P \times R}{P + R} \qquad F1_{macro} = \frac{F1_{diabetes} + F1_{controle}}{2}
```

- **Precisão:** dos que o modelo chamou de diabetes, quantos são mesmo.
- **Recall:** dos diabéticos de verdade, quantos o modelo achou.
- **F1:** a média harmônica das duas. Ela puxa para o valor mais baixo, então só é alta se as duas forem altas. Forma equivalente: F1 = 2·VP ÷ (2·VP + FP + FN).
- **F1-macro:** calcula o F1 de cada classe, trocando quem é o "positivo", e tira a média simples. Cada classe pesa igual.

Exemplo para treinar: 50 diabéticos e 50 controles, VP = 40, FN = 10, FP = 5, VN = 45. Na classe diabetes, P = 40/45 = 0,889, R = 0,800 e F1 = 0,842. Na classe controle, P = 45/55 = 0,818, R = 0,900 e F1 = 0,857. O F1-macro fica em 0,850.

**Se perguntarem** "por que não acurácia?": com classes desbalanceadas, um modelo que diz "controle" para todos pode ter acurácia alta e F1-macro baixo. Na nossa base as classes são equilibradas (270 diabéticos e 250 controles), então os dois ficam quase iguais (0,912 nos dois no voto).

### Slide 5: A base veio bagunçada (slide cortável)

**O que mostra:** as grafias de sexo, histórico familiar e atividade física ligadas às categorias finais. Em laranja, as grafias com erro de digitação.

**O que falar:** sexo veio escrito de 12 jeitos, histórico familiar de 13 e atividade física de 18. Além disso, havia idade 999, pressão como texto ("120/80") e quase 30% dos pacientes sem algum exame.

**Para estudar:** isso é inconsistência de dados, da aula 2 (qualidade dos dados). A solução foi um mapa de grafias para categorias. Grafia desconhecida vira ausente e é tratada como ausente.

**Se perguntarem** "e se aparecer uma grafia nova no conjunto externo?": ela vira ausente e recebe a mediana do treino nos dados clínicos. O script de entrega não quebra.

### Slide 6: Altura em metros, peso em libras e triglicerídeos extremos (opcional)

**O que mostra:** à esquerda os valores como vieram, à direita depois da correção: altura, peso e triglicerídeos.

**O que falar:** use só se perguntarem das etapas 3 a 5 do tratamento.

**Para estudar:**

- **Altura:** 102 valores em metros (abaixo de 3) foram multiplicados por 100.
- **Peso:** 23 valores acima de 140 eram libras e foram divididos por 2,2046. Ficaram entre 64 e 110 kg.
- **Triglicerídeos:** 3 valores acima de 1000 foram limitados a 1000.
- **Idade:** 6 idades impossíveis (0, −1, 999) foram recalculadas pelo ano do exame menos o ano de nascimento.
- Todas essas regras são aplicadas linha a linha. Nenhuma usa estatística do conjunto, então não há vazamento do teste.

## Parte 02: primeiras tentativas (slides 7 a 9)

### Slide 7: Seção 02, primeiras tentativas

**O que mostra:** abertura da segunda parte: KNN e árvore como vimos em aula, combinações de modelos e por que a validação enganava.

**O que falar:** agora o que tentamos primeiro, mexendo só no modelo.

### Slide 8: Quatro tentativas mexendo no modelo, todas abaixo do baseline

**O que mostra:** quatro cartões com as notas no Kaggle: 0,829, 0,806, 0,830 e 0,844.

**O que falar:** começamos pelo que vimos em aula. KNN K=11 com peso maior para glicose e hemoglobina deu 0,829. Tirar a glicose da distância quando faltava piorou para 0,806. A árvore com 4 atributos deu 0,830, e KNN mais árvore chegou a 0,844. O baseline era 0,872. O estranho: na validação esses modelos davam entre 87% e 91%.

**Para estudar:**

- **KNN** (aulas 3 e 5): classifica pelos K vizinhos mais próximos. Dar "peso" a um atributo é multiplicar a escala dele, para ele contar mais na distância.
- **Árvore de decisão** (aula 5): perguntas de sim ou não sobre um atributo por vez.
- **Média dos apoios:** cada modelo dá um número entre 0 e 1 (a probabilidade de diabetes). Tira-se a média e compara com 0,5.
- **Baseline:** a nota de referência que o professor deixou no placar (0,872).

**Se perguntarem** "por que o 2 piorou?": o diabético sem glicose passava a ser comparado sem o exame que mais denunciava a doença, e parecia saudável. A solução certa só veio no slide 17.

### Slide 9: Mais combinações melhoravam a validação, não o Kaggle (slide cortável)

**O que mostra:** mais de 30 mil combinações testadas no KNN, cerca de 57 mil na árvore e cerca de 79 mil formas de juntar os 3. Embaixo, 91% na validação contra 84% no Kaggle.

**O que falar:** achamos que o problema era o modelo e testamos dezenas de milhares de variações. A validação subia até 91%, mas o Kaggle ficava em 84%. Estávamos sempre testando nas mesmas 416 pessoas, e o modelo se ajustava àquele grupo. Então paramos de mexer no modelo e fomos olhar os dados.

**Para estudar:**

- **Sobreajuste (overfitting, aula 7):** o modelo aprende detalhes do grupo usado para avaliar, e não o padrão geral. Ele vai bem nesse grupo e mal em dados novos.
- **Como as combinações foram feitas:** laços em código que testavam automaticamente todas as opções de atributos, escala, distância e K (KNN), de profundidade e folha (árvore) e de pesos e limites (combinação). Cada uma recebia uma nota na mesma divisão, e ficava a maior.
- **Por que isso engana:** com dezenas de milhares de tentativas, alguma vai bem por sorte naquele grupo. Escolher a melhor nota de muitas tentativas superestima o resultado real.
- **O que mudamos depois:** validação cruzada com repetições (slide 26), poucas opções testadas por modelo e uma semente para escolher (2026) e outra para medir (777).

**Se perguntarem** "como vocês testaram 80 mil combinações?": com scripts em Python que rodavam em laço todas as variações e guardavam a nota de cada uma. Foi justamente isso que gerou o sobreajuste, e por isso abandonamos essa estratégia.

## Parte 03: ajuste, olhar os dados (slides 10 a 24)

### Slide 10: Seção 03, ajuste: olhar os dados

**O que mostra:** abertura da terceira parte: unidades da glicose e da hemoglobina, os exames que faltavam e todo o tratamento da base.

**O que falar:** a partir daqui paramos de mexer no modelo e voltamos para os dados. Atenção: a nota diz "quando voltei". Na apresentação, falem no plural.

### Slide 11: A glicose estava em duas unidades diferentes

**O que mostra:** um vídeo com o histograma da glicose como veio. Um grupo de 44 valores entre 3,1 e 21,3 (em laranja) fica separado dos outros, que vão de 47 a 500.

**O que falar:** a glicose tinha dois grupos sem nada no meio. 44 pacientes entre 3 e 21, sempre com casa decimal, e o resto entre 47 e 500, sempre inteiro. Era mmol/L misturado com mg/dL. Uma glicose de 7 mmol/L, que é 126 mg/dL e já o limite de diabetes, aparecia como um valor baixíssimo.

**Para estudar:**

- **Conversão:** mg/dL = mmol/L × 18,016. A regra no código: valor abaixo de 35 é multiplicado.
- **Como percebemos:** o histograma tinha um buraco entre 21 e 47. Nenhum ser humano vivo tem glicose de 5 mg/dL.
- **Por que isso destruía o modelo:** um diabético com 11 mmol/L (198 mg/dL) parecia ter a glicose mais baixa da base, ou seja, saudável.

**Se perguntarem** "como vocês decidiram o corte de 35?": pelo buraco no histograma. Não há valores entre 21,3 e 47, então qualquer corte nessa faixa dá o mesmo resultado.

### Slide 12: A hemoglobina glicada tinha o mesmo problema (antes)

**O que mostra:** o histograma da HbA1c. A maioria está em % (de 4,7 a 13), e 43 valores estão entre 27 e 116.

**O que falar:** com a HbA1c aconteceu o mesmo: 43 valores estavam em mmol/mol, que é a unidade IFCC.

### Slide 13: A hemoglobina glicada tinha o mesmo problema (depois)

**O que mostra:** o mesmo histograma depois da conversão. Os 43 valores (em azul) caem na mesma faixa dos outros.

**O que falar:** convertidos pela fórmula do NGSP, os 43 valores ficam na mesma escala.

**Para estudar:**

```latex
\text{HbA1c (\%)} = 0{,}09148 \times \text{HbA1c (mmol/mol)} + 2{,}152
```

A regra no código: valor acima de 20 é convertido. Referência médica: HbA1c de 6,5% ou mais indica diabetes.

### Slide 14: Corrigidas as unidades, controle e diabetes se separam

**O que mostra:** um vídeo com o gráfico de glicose × HbA1c antes e depois da correção, com controle em verde e diabetes em vermelho. Embaixo: Kaggle KNN 0,857 e média dos 3 0,866.

**O que falar:** depois da conversão, nenhum paciente controle tem HbA1c acima de 6,4%. Só com essa correção, um KNN simples com dois atributos foi para 0,857, e a média dos três para 0,866. Dois atributos bem tratados ganharam das dezenas de milhares de combinações.

**Se perguntarem** "então por que ainda estava abaixo do baseline?": por causa dos pacientes sem exame, que são os próximos slides.

### Slide 15: 31% dos pacientes não têm algum dos dois exames

**O que mostra:** um mapa de ausentes com os 520 pacientes (laranja = exame ausente), agrupados pelos exames que têm.

| Grupo | Pacientes no treino |
| --- | --- |
| Glicose e HbA1c | 357 |
| Só glicose | 104 |
| Só HbA1c | 41 |
| Nenhum exame | 18 |

**O que falar:** ainda abaixo do baseline, fomos ver onde o modelo errava. 163 dos 520 pacientes (31%) não têm glicose, HbA1c ou os dois.

### Slide 16: Preencher o exame com a mediana escondia os diabéticos

**O que mostra:** barras com a taxa de falsos negativos (diabéticos classificados como controle) em cada grupo. Laranja é antes (KNN com o exame ausente preenchido pela mediana), azul é depois (voto dos 3 com submodelo por padrão).

| Grupo | Antes | Depois |
| --- | --- | --- |
| Glicose e HbA1c | 12% | 10% |
| Só glicose | 36% | 15% |
| Só HbA1c | 23% | 10% |
| Nenhum exame | 100% | 39% |

**O que falar:** o erro estava nos diabéticos sem exame. Preenchíamos o exame que faltava com a mediana, que é um valor normal, e o diabético parecia saudável.

**Para estudar:** na aula 2, as opções para valor ausente incluem descartar, preencher (média, mediana, vizinhos) e ignorar o atributo. A mediana é um valor típico, e o paciente típico da base está na faixa normal. Por isso preencher puxa o diabético para o lado do controle.

**Se perguntarem** "por que não tirar esses pacientes?": no teste eles também existem e precisam de uma resposta. Tirar do treino não resolve a classificação deles.

### Slide 17: Cada paciente é classificado só com o que ele tem

**O que mostra:** um diagrama com o paciente à esquerda, quatro linhas (uma por padrão de exames) e, em cada linha, KNN, árvore e rede votando. Cada paciente passa por uma linha só.

| Linha | Atributos usados | No treino |
| --- | --- | --- |
| Glicose e HbA1c | Glicose + HbA1c (a rede usa também os 6 clínicos) | 357 |
| Só glicose | Glicose + 6 dados clínicos | 104 |
| Só HbA1c | HbA1c + 6 dados clínicos | 41 |
| Nenhum exame | Só os 6 dados clínicos | 18 |

Os 6 dados clínicos são triglicerídeos, pressão sistólica, IMC, idade, histórico familiar e atividade física.

**O que falar:** em vez de inventar o exame que falta, cada modelo virou quatro. Cada submodelo é treinado com todos os pacientes do treino que têm aqueles exames. Estimar o exame pelos vizinhos também foi testado e ficou pior. No Kaggle deu 0,899, a primeira vez acima do baseline.

**Para estudar:**

- É a opção "ignorar o atributo ausente" da aula 2, aplicada paciente a paciente.
- **Por que funciona:** o submodelo "só glicose" aprende com os 461 pacientes que têm glicose (357 + 104), e não só com os 104.
- Dado clínico ausente (são poucos) recebe a mediana do treino dentro de cada submodelo.

**Se perguntarem** "o submodelo de 18 pacientes não é fraco?": ele é treinado com os 520, porque todo paciente tem dados clínicos. Os 18 são só os que caem nessa linha.

### Slide 18: Como o voto decide: dois pacientes reais do teste

**O que mostra:** um vídeo com dois pacientes do teste passando pelo voto.

**O que falar:**

1. Olhamos quais exames o paciente tem, e isso escolhe a linha.
2. Os três modelos daquela linha dão um número entre 0 e 1. No KNN é a fração dos 11 vizinhos com diabetes. Na árvore, a fração de diabéticos na folha. Na rede, a saída da sigmoide.
3. Acima de 0,5, aquele modelo vota diabetes.
4. Vence a maioria (2 ou 3 votos).

**Os dois pacientes:**

- **Paciente 555:** tem os dois exames (glicose 148, HbA1c 5,2). KNN e árvore votam diabetes e a rede vota controle. Resultado: diabetes (2 × 1).
- **Paciente 268:** só tem glicose. Só a árvore vota diabetes. Resultado: controle (1 × 2).

**Se perguntarem** "por que voto e não média?": na validação os dois empatam (voto 0,912, média 0,915). O voto é mais fácil de explicar e foi o que tirou 0,899 no Kaggle.

### Slides 19 a 24: O tratamento da base em 6 etapas

**O que mostram:** os mesmos 6 cartões, acendendo um por slide.

| Slide | Etapa | Número | O que foi feito |
| --- | --- | --- | --- |
| 19 | 1. Duplicatas | 20 | Pacientes repetidos, iguais em tudo menos no id. O treino caiu de 540 para 520 |
| 20 | 2. Textos | 52 | 52 grafias viraram 11 categorias. Pressão separada em sistólica e diastólica |
| 21 | 3. Impossíveis | 108 | 102 alturas em metros para cm e 6 idades recalculadas |
| 22 | 4. Unidades | 110 | 44 glicoses, 43 HbA1c e 23 pesos em libras convertidos |
| 23 | 5. Extremos | 3 | Triglicerídeos acima de 1000 limitados a 1000 |
| 24 | 6. Ausentes | 163 | Pacientes sem algum exame vão para o submodelo do seu caso |

**O que falar:** tudo isso é da aula 2 (qualidade e pré-processamento dos dados). Qualquer média ou mediana é calculada só com o treino.

**Para estudar:**

- **Por que tirar duplicatas:** o mesmo paciente no treino e na parte de validação infla a nota, porque o modelo "já viu" a resposta.
- **Limitar extremos** (clipping): um valor de 3000 de triglicerídeos distorce a padronização do KNN e da rede.
- **Sem vazamento:** as regras das etapas 1 a 5 são linha a linha. A mediana dos ausentes é calculada dentro de cada rodada de treino.

**Se perguntarem** "essa limpeza funciona no conjunto externo do professor?": sim. As regras são fixas e aplicadas paciente a paciente, e o script de entrega aplica a mesma limpeza a qualquer CSV.

## Parte 04: os três modelos e o voto (slides 25 a 35)

### Slide 25: Seção 04, os três modelos e o voto

**O que mostra:** abertura da quarta parte: como avaliamos sem usar o teste, como construímos cada modelo e por que o voto funciona.

**O que falar:** agora, como avaliamos e construímos cada modelo do voto.

### Slide 26: Avaliamos tudo com validação cruzada, sem tocar no teste

**O que mostra:** um vídeo com os 520 pacientes divididos em 5 partes de 104, e a parte de teste andando de rodada em rodada. Ao lado: 5 rodadas, × 4 repetições = 20, e o resultado é a média.

**O que falar:**

1. Dividimos os 520 pacientes em 5 partes de 104, cada uma com a mesma proporção de diabéticos.
2. Treinamos com 4 partes (416) e testamos na que sobrou (104).
3. Repetimos até cada parte ser testada uma vez: 5 rodadas.
4. Embaralhamos de outro jeito e fazemos tudo de novo, 4 vezes: 20 rodadas.
5. Cada número da apresentação é a média das 20.

**Para estudar:**

- **Validação cruzada estratificada repetida** (aula 7). "Estratificada" = cada parte mantém a proporção de diabéticos e controles.
- **Por que repetir:** uma divisão só pode dar sorte ou azar. A média de 20 rodadas é mais estável.
- **Duas sementes:** a semente é o número que fixa o sorteio das partes. Usamos a 2026 para escolher K, profundidade e neurônios, e a 777 para medir o resultado final. Assim não medimos nas mesmas divisões usadas para escolher.
- **Cada paciente é testado uma vez por repetição**, sempre por um modelo que não o viu no treino.

**Se perguntarem** "as 20 rodadas viram 20 modelos?": não. As rodadas servem só para dar nota a uma configuração. Depois de escolhida, treinamos um único modelo com os 520 e ele prevê o teste (slide 28).

### Slide 27: O voto dos três supera cada modelo sozinho

**O que mostra:** um gráfico com o F1-macro na validação de cada modelo e do voto. A marca do Kaggle aparece ao lado do voto.

| Modelo | F1-macro (validação) |
| --- | --- |
| Voto dos 3 | **0,912** (Kaggle 0,899) |
| KNN (K=11) | 0,896 |
| Árvore (profundidade 4) | 0,894 |
| Rede neural (8 neurônios) | 0,886 |

**O que falar:** cada modelo erra em pacientes diferentes, por isso o voto funciona. Sozinhos ficam perto de 0,89, juntos vão para 0,912.

**Para estudar:** combinar modelos (ensemble) só ajuda quando os erros são diferentes. Se os três errassem nos mesmos pacientes, o voto erraria junto. A média dos 3 dá 0,915, empatada com o voto.

**Se perguntarem** "por que o Kaggle ficou abaixo da validação?": a diferença é pequena (0,013) e o placar público usa só parte do teste, cerca de 70%. Cada paciente vale uns 0,003-0,005 na nota. Antes, a diferença era de 7 pontos (91% × 84%).

### Slide 28: Como a validação cruzada escolheu o K

**O que mostra:** quatro passos numerados. À esquerda, as 20 notas reais do K=11 (repetição × parte) e a média 0,900. À direita, a média de cada K, com o 11 destacado.

| K | 3 | 5 | 7 | 9 | **11** | 15 | 21 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Média das 20 notas | 0,887 | 0,893 | 0,895 | 0,898 | **0,900** | 0,896 | 0,892 |

**O que falar:**

1. Fixamos um K e rodamos a validação cruzada: 20 notas.
2. Tiramos a média das 20.
3. Repetimos para cada K e ficamos com a maior média.
4. Treinamos um modelo final com K=11 usando os 520 pacientes, e ele prevê o teste.

**Para estudar:**

- **Hiperparâmetro:** uma escolha feita antes do treino, como o K, a profundidade ou o número de neurônios. Ele fica fixo durante todas as 20 rodadas de uma configuração. O que muda de rodada para rodada são só os pacientes de treino e de teste.
- As notas do K=11 vão de 0,856 a 0,942 só por causa de quem caiu no teste. Por isso se escolhe pela média.
- O mesmo processo escolheu a profundidade da árvore e os neurônios da rede.

**Se perguntarem** "por que só ímpares?": com duas classes, K ímpar evita empate no voto dos vizinhos.

### Slide 29: KNN, o paciente é classificado pelos vizinhos mais parecidos

**O que mostra:** um vídeo em que o círculo cresce até pegar 11 vizinhos de um paciente novo (glicose 79, HbA1c 6,4): 6 diabéticos e 5 controles, então diabetes. Ao lado, os 4 passos.

**O que falar:** o KNN não treina nada, ele guarda os pacientes do treino. Para classificar alguém novo:

1. Padroniza os atributos: (valor − média) ÷ desvio.
2. Mede a distância Euclidiana até cada paciente do treino.
3. Pega os 11 mais próximos.
4. A classe que mais aparece entre os 11 ganha.

**Para estudar:**

```latex
z = \frac{x - \text{média}}{\text{desvio}} \qquad d(a, b) = \sqrt{(g_a - g_b)^2 + (h_a - h_b)^2}
```

- **Por que padronizar:** a glicose vai até 500 e a HbA1c até 13. Sem padronizar, a glicose dominaria a distância sozinha.
- **Lazy learner:** o KNN não tem fase de aprendizado. Todo o custo fica na hora de classificar.
- O "apoio" do KNN no voto é a fração de vizinhos diabéticos (6/11 = 0,55 no exemplo).

### Slide 30: KNN, o que menos gera falsos positivos

**O que mostra:** como construímos, a curva do F1 por K e o resultado na validação: F1 0,896, recall de diabetes 0,854 e recall de controle 0,942.

**O que falar:** padronizamos pela média e desvio e usamos distância Euclidiana. Com os dois exames, o KNN usa só glicose e HbA1c: colocar os dados clínicos piorou, porque no KNN todo atributo pesa igual na distância. K pequeno segue o ruído e K grande mistura gente diferente. O melhor foi 11.

**Para estudar:**

- **Ponto forte:** poucos falsos positivos (FP), cerca de 14 dos 250 controles.
- **Ponto fraco:** mais falsos negativos (FN), cerca de 40 dos 270 diabéticos.
- Testamos mín-máx no lugar da padronização (0,885, pior) e Manhattan no lugar da Euclidiana (empate).

**Se perguntarem** "por que o KNN é conservador?": o diabético com exames pouco alterados fica no meio dos controles, e a maioria dos vizinhos dele é controle.

### Slide 31: Árvore, perguntas de sim ou não até chegar numa folha

**O que mostra:** a árvore aprendida para quem tem os dois exames e um vídeo com dois pacientes percorrendo o caminho.

| Folha (caminho) | Pacientes do treino | % diabetes | Voto |
| --- | --- | --- | --- |
| HbA1c > 6,38 | 152 | 99% | diabetes |
| HbA1c ≤ 6,38 e glicose > 144 | 19 | 100% | diabetes |
| HbA1c ≤ 6,38, glicose ≤ 122 | 171 | 5% | controle |
| Glicose entre 122 e 144, HbA1c ≤ 5,95 | 7 | 71% | diabetes |
| Glicose entre 122 e 144, HbA1c > 5,95 | 8 | 12% | controle |

**O que falar:** cada caixa azul é uma pergunta. Respondemos e seguimos o sim ou o não até uma folha, e o percentual da folha é o voto da árvore. O paciente 555 (HbA1c 5,2 e glicose 148): sim e não, folha de 100%, vota diabetes. O paciente 478 (HbA1c 5,8 e glicose 115): sim, sim, sim, folha de 5%, vota controle.

**Se perguntarem** "a folha de 7 pacientes com 71% não é estranha?": é uma região pequena e ambígua. O mínimo de 5 pacientes por folha impede folhas ainda menores, que seriam decoreba.

### Slide 32: As mesmas perguntas, vistas no gráfico

**O que mostra:** um vídeo com os cortes da árvore dividindo o gráfico glicose × HbA1c em retângulos. A região verde é onde ela responde controle.

**O que falar:** a árvore testa todos os atributos e todos os cortes e fica com o que mais separa as classes, medido pelo ganho de informação. A primeira pergunta que ela escolheu sozinha foi HbA1c acima de 6,38, muito perto do critério médico de 6,5%.

**Para estudar:**

```latex
H = -p \log_2 p - (1-p) \log_2 (1-p) \qquad \text{Ganho} = H_{pai} - \sum \frac{n_{filho}}{n_{pai}} H_{filho}
```

- **Entropia:** é 0 quando o grupo é todo de uma classe e 1 quando está meio a meio.
- **Ganho de informação:** quanto a entropia cai depois do corte. Ganha o corte que mais deixa os grupos puros.
- Cada corte é uma linha reta paralela a um eixo, por isso as regiões são retângulos.

### Slide 33: Árvore, a que mais acerta os diabéticos

**O que mostra:** como construímos, a curva do F1 por profundidade e o resultado: F1 0,894, recall de diabetes 0,881 e recall de controle 0,907.

**O que falar:** a árvore não precisa de padronização, porque cada corte olha um atributo só. Usamos entropia (o Gini empatou). Testamos profundidades de 2 a 6 e sem limite, com 1, 5 e 10 pacientes por folha. Sem limite e com folhas de 1 paciente, ela decora o treino e cai para 0,874. Profundidade 4 com folha 5 empatou com a melhor e é a mais simples de ler.

**Para estudar:**

- **Ponto forte:** mais verdadeiros positivos (VP), 238 dos 270 diabéticos, e as regras são legíveis.
- **Ponto fraco:** mais falsos positivos (FP) que o KNN, cerca de 23 dos 250 controles.
- **Poda prévia:** limitar a profundidade e o tamanho da folha evita o sobreajuste.

### Slide 34: Rede neural, os pesos são aprendidos com o erro

**O que mostra:** um vídeo com a rede de 8 entradas, 8 neurônios ocultos e 1 saída. Primeiro a ida (azul), depois a volta do erro (vermelho).

**O que falar:**

1. Cada neurônio soma as entradas multiplicadas pelos pesos, mais o viés.
2. A sigmoide transforma essa soma num valor entre 0 e 1.
3. Na saída, valor de 0,5 ou mais significa diabetes.
4. No treino, o erro da saída volta pela rede (retropropagação) e ajusta os pesos, por até 3000 épocas.

**Para estudar:**

```latex
z = \sum_i w_i x_i + b \qquad \sigma(z) = \frac{1}{1 + e^{-z}}
```

- As 8 entradas são os 2 exames e os 6 dados clínicos.
- **Época:** uma passada completa por todos os pacientes do treino.
- **Retropropagação** (aula 6): calcula quanto cada peso contribuiu para o erro e o ajusta no sentido que diminui o erro (gradiente descendente).

### Slide 35: Rede neural, a melhor quando falta exame

**O que mostra:** como construímos, a curva do F1 por número de neurônios e o resultado: F1 0,886, recall de diabetes 0,870 e recall de controle 0,904.

**O que falar:** a rede usa os dados clínicos mesmo quando o paciente tem os dois exames, porque aprende quanto peso dar a cada entrada. O otimizador é o Adam, uma variação do gradiente descendente. A versão igual à do slide 17 da aula deu 0,874. Testamos 2, 4, 8 e 16 neurônios, deu empate e ficamos com 8. Com 5 inicializações diferentes, o resultado ficou entre 0,888 e 0,894.

**Para estudar:**

- **Ponto forte:** menos erros quando falta exame, com 15% de erro em quem só tem glicose (KNN e árvore: 20%).
- **Ponto fraco:** mais falsos positivos (FP) em quem tem os dois exames, cerca de 14 dos 173 controles.
- **Adam:** ajusta o tamanho do passo de cada peso sozinho. Converge mais rápido que o gradiente simples.
- **Inicialização:** os pesos começam sorteados. Testar 5 sorteios mostra que o resultado não depende de sorte.

**Se perguntarem** "por que a rede tem nota menor e mesmo assim entra no voto?": porque erra em pacientes diferentes, principalmente nos sem exame, e isso desempata o KNN e a árvore.

## Avaliação e encerramento (slides 36 a 38)

### Slide 36: O voto erra cerca de 45 dos 520 pacientes na validação

**O que mostra:** a matriz de confusão do voto (média por repetição da validação cruzada) e as métricas ao lado.

|  | Previsto controle | Previsto diabetes |
| --- | --- | --- |
| **Real controle (250)** | 236 (VN) | 14 (FP) |
| **Real diabetes (270)** | 31 (FN) | 239 (VP) |

| Métrica | Conta | Valor |
| --- | --- | --- |
| F1-macro | Média do F1 das duas classes | 0,912 |
| Acurácia | (VP + VN) ÷ total | 0,912 |
| Precisão (macro) | Média da precisão das duas classes | 0,914 |
| Recall de diabetes | VP ÷ (VP + FN) = 239 ÷ 270 | 0,885 |
| Recall de controle | VN ÷ (VN + FP) = 236 ÷ 250 | 0,942 |

**O que falar:** a classe positiva é diabetes. Erramos cerca de 45 pacientes: 14 controles marcados como diabetes e 31 diabéticos marcados como controle. Testamos também Manhattan, Gini, tirar e colocar atributos e Random Forest, e nada melhorou de forma consistente. No placar público ficamos em 13º de 19, a uns 5 pacientes do primeiro.

**Para estudar:**

- **VP:** diabético previsto como diabetes. **VN:** controle previsto como controle.
- **FP:** controle previsto como diabetes. **FN:** diabético previsto como controle.
- Em saúde, o FN costuma ser o erro mais grave, porque o doente vai embora sem diagnóstico.
- **Onde estão os erros que sobram:** 17,5 dos \~45 são diabéticos com glicose e HbA1c normais, e 15 são pacientes só com glicose. Nos primeiros, os exames dizem "saudável" e os dados clínicos não trazem sinal suficiente.
- Os números têm casa decimal (por exemplo, 235,5) porque são a média das 4 repetições. No slide estão arredondados.

**Se perguntarem** "por que não baixar o corte de 0,5 para achar mais diabéticos?": testamos. Com corte 0,45, o recall de diabetes sobe para 0,896, mas o de controle cai para 0,918, e o F1-macro cai para 0,907. Com 0,40 cai para 0,905. O corte de 0,5 já é o melhor equilíbrio.

### Slide 37: Pontos de atenção

**O que mostra:** quatro lições numeradas.

1. **Olhar os dados antes do modelo:** a correção das unidades rendeu mais que 79 mil combinações.
2. **Valor ausente não é valor normal:** preencher com a mediana escondia justamente os doentes.
3. **Desconfiar de validação boa demais:** 91% na validação e 84% no Kaggle. O modelo aprendia o grupo, não o problema.
4. **Simples e bem preparado vence complexo:** K=11, árvore de profundidade 4 e rede de 8 neurônios.

**O que falar:** começamos tentando melhorar o modelo e terminamos melhorando os dados. Foi aí que o resultado veio.

**Se perguntarem** "o que fariam diferente?": começar pela análise exploratória (histogramas e mapa de ausentes) antes de testar modelos, e montar a validação cruzada com repetições desde o início.

### Slide 38: Obrigado

**O que falar:** agradecer e abrir para perguntas.

## Glossário e perguntas prováveis

### Glossário

| Termo | Significado | Slide |
| --- | --- | --- |
| Baseline | Nota de referência do professor no placar (0,872) | 2, 8 |
| VP / VN / FP / FN | Verdadeiro positivo / verdadeiro negativo / falso positivo / falso negativo (positivo = diabetes) | 36 |
| Precisão | Dos que o modelo chamou de diabetes, quantos são | 4 |
| Recall | Dos diabéticos reais, quantos o modelo achou | 4 |
| F1 | Média harmônica de precisão e recall | 4 |
| F1-macro | Média simples do F1 de cada classe | 4 |
| Sobreajuste | Aprender o grupo de avaliação e não o padrão geral | 9 |
| Validação cruzada | Dividir o treino em partes e revezar qual delas é o teste | 26 |
| Estratificada | Cada parte mantém a proporção das classes | 26 |
| Semente | Número que fixa o sorteio, para os resultados se repetirem | 26 |
| Hiperparâmetro | Escolha feita antes do treino (K, profundidade, neurônios) | 28 |
| Padronização (z-score) | (valor − média) ÷ desvio | 29 |
| Distância Euclidiana | Raiz da soma dos quadrados das diferenças | 29 |
| Entropia | Mede a mistura de classes num grupo (0 = puro, 1 = meio a meio) | 32 |
| Ganho de informação | Quanto a entropia cai depois de um corte | 32 |
| Sigmoide | Função que leva qualquer número para entre 0 e 1 | 34 |
| Retropropagação | O erro volta pela rede e ajusta os pesos | 34 |
| Época | Uma passada completa pelo treino | 34 |
| Apoio | Número entre 0 e 1 que cada modelo dá para diabetes | 18 |
| Voto da maioria | Diabetes quando 2 ou 3 modelos dizem diabetes | 18 |
| Submodelo por padrão | Um modelo para cada combinação de exames disponíveis | 17 |

### Perguntas prováveis do professor

1. **"Vocês usaram o teste para escolher alguma coisa?"** Não. Toda escolha foi feita por validação cruzada só no treino. O Kaggle só serviu para conferir as submissões.
2. **"Como o modelo vai rodar no meu conjunto externo?"** Pela pasta `Mod8_Unidades`: `python3 prever.py externo.csv`. O script treina com os 520, aplica a mesma limpeza e devolve id e class. Se o arquivo tiver a coluna class, ele já mostra as métricas.
3. **"Por que KNN, árvore e rede, e não Random Forest?"** As regras pediam esses três como ponto de partida. A Random Forest foi testada e não melhorou de forma consistente.
4. **"De onde veio o 0,5 do corte?"** É o padrão. Testamos 0,45, 0,40, 0,35 e 0,30, e todos pioraram o F1-macro.
5. **"Qual modelo vocês escolheriam se fosse só um?"** O KNN (0,896), por ser o mais estável. Se o objetivo fosse não perder diabético, a árvore, que tem o maior recall de diabetes (0,881).
6. **"Como vocês usam a mediana sem vazar informação do teste?"** Ela é calculada dentro de cada rodada, só com os pacientes de treino daquela rodada. No modelo final, só com os 520 do treino.
7. **"O que mais daria para melhorar?"** O erro que sobra está nos diabéticos com exames normais. Para esse grupo, os atributos disponíveis não separam as classes. Mais ajuste fino arriscaria repetir o sobreajuste do início.

### Números para saber de cor

- 540 → 520 pacientes no treino (20 duplicatas) e 312 no teste.
- 270 diabéticos e 250 controles no treino.
- 163 pacientes (31%) sem algum exame: 104 só glicose, 41 só HbA1c, 18 nenhum.
- 44 glicoses (× 18), 43 HbA1c (fórmula NGSP) e 23 pesos (÷ 2,2046) convertidos.
- K = 11, profundidade 4 com folha 5, 8 neurônios.
- Voto: 0,912 na validação e 0,899 no Kaggle. Baseline: 0,872.
