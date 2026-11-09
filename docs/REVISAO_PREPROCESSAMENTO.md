# Revisão do pré-processamento e da avaliação — 06/11/2026

Pausamos a busca de modelos para revisar os dados e o processo. Esta auditoria reconstruiu o pré-processamento em memória, leu os registros já existentes e conferiu os CSVs locais. Os arquivos de dados e os modelos foram preservados. Os números abaixo são diagnósticos; as hipóteses ainda precisam ser discutidas antes de novas transformações.

## Conferências concluídas

| Conferência | Resultado |
|---|---|
| Reconstrução do notebook de exploração, do início, sem exportar | Reproduziu byte a byte `treinamento_padronizado.csv` |
| Base original e padronizada | 540 linhas e 21 colunas; 520 linhas e 25 colunas após as transformações |
| Remoção de repetições | 20 pares do mesmo paciente, idênticos em todas as colunas exceto `id` |
| Classes após padronização | 270 registros da classe 1 e 250 da classe 0; nenhum rótulo alterado nos registros mantidos |
| Pacientes presentes tanto no treinamento como no teste | Nenhum código em comum |
| Regras de inferência comparadas com a padronização do treinamento | Nenhuma diferença nas nove medidas e seis categorias examinadas |
| CSVs locais examinados | Cabeçalhos, 312 IDs, ordem e classes 0/1 corretos |

O SHA-256 da base padronizada permanece `bc1a686d83c06e2d7667a6089e82b54b4bff2ca6467b81155f1246ac4719a032`. A conferência dos CSVs foi local; não comparamos o conteúdo binário dos arquivos hospedados no Kaggle.

## Pontos confirmados que afetam a análise

### A escala alterou o peso relativo dos atributos do KNN

O KNN manteve K, atributos, imputação e fórmula de distância, mas mudou os divisores usados para colocar os valores em escala. Na reserva, passou de 90 para 79 acertos: F1 macro de 86,53% para 75,94%.

Na referência de 416 amostras, a contribuição de uma mesma diferença numérica à parte Manhattan da distância mudou assim:

| Atributo | Divisor anterior, Q3 − Q1 | Divisor novo, desvio padrão | Fator da contribuição nova em relação à anterior |
|---|---:|---:|---:|
| Glicose | 45,25 | 65,00 | 0,70 |
| Hemoglobina | 3,30 | 12,89 | 0,26 |
| Triglicerídeos | 98,75 | 218,03 | 0,45 |
| Sódio | 4,00 | 2,55 | 1,57 |

Isso comprimiu as diferenças de hemoglobina e triglicerídeos e ampliou a contribuição do sódio. O fator descreve a parte numérica da distância, não uma importância estimada do atributo. A mudança também pode trocar quem são os vizinhos mais próximos. A fórmula comum, sozinha, não garante o mesmo equilíbrio entre atributos.

### A avaliação de escolha foi muito explorada

As buscas compararam milhares de configurações nas mesmas 416 pessoas. As novas sementes alteram as partes, mas continuam usando essas pessoas. As melhores médias da busca podem incorporar coincidências desse grupo. As 104 amostras reservadas também já foram consultadas repetidamente.

As médias das partes usadas para escolher devem ser apresentadas como resultados de seleção. As conferências ajudam a acompanhar a variação, mas não criam novas pessoas nem recuperam uma reserva intocada. Isso pode explicar parte da diferença para o Kaggle; não quantificamos quanto.

## Premissas e decisões que precisam voltar à discussão

| Campo ou tratamento | O que encontramos no treinamento padronizado | Situação |
|---|---|---|
| `GLUCOSE` | 461 preenchidos, de 3,1 a 500; 44 valores abaixo de 40 | A interpretação de todos os valores como mg/dL foi uma premissa |
| `HEMOGLOBIN` | 398 preenchidos, de 4,7 a 116; 43 valores a partir de 20 | A interpretação como HbA1c foi uma premissa |
| Regra `HEMOGLOBIN > 100` | O CSV conserva o valor; os leitores dos modelos o tratam como ausente | Afeta um registro e depende da interpretação da coluna |
| `WEIGHT` | 507 preenchidos, de 41,3 a 242,1 | Quilogramas continuam sendo uma premissa |
| `TRIGLYCERIDES` | Mediana 150; máximo 2.880 | Investigar valores extremos antes de decidir qualquer tratamento |
| Ausências de exames | 59 glicoses vazias e 122 hemoglobinas vazias; o leitor dos modelos acrescenta uma hemoglobina ausente pela regra acima | A imputação por média ou mediana reduz a informação disponível nesses registros |

Os intervalos observados não comprovam unidades misturadas ou erros. Eles mostram decisões ainda dependentes de interpretação. Não aplicamos novas conversões, exclusões ou cortes nesta auditoria.

Em 164 das 520 amostras falta glicose ou hemoglobina para o modelo. O efeito nos erros varia: na divisão 42, a mistura anterior acertou 94,68% das 282 amostras com ambos disponíveis e 85,07% das 134 com algum ausente. Na reserva, foram 87,84% de 74 e 90,00% de 30, respectivamente. Essa inversão impede atribuir toda a queda apenas à ausência dos exames.

## Métrica oficial

Conferimos a página da competição na sessão do navegador. A seção de avaliação pede precisão, recall de diabetes, recall de controle e F1 macro. A identificação da competição traz `F-Score (Macro)`. O placar deve ser distinguido da acurácia. [Enunciado e avaliação](https://www.kaggle.com/competitions/deteccao-de-diabetes/overview).

O enunciado também informa que a base contém informações reais e artificiais. Não encontramos uma especificação de unidade na descrição dos dados consultada.

## Como retomar

Primeiro, revisar a interpretação de glicose e hemoglobina e listar quais regras são apenas de formato e quais dependem de uma premissa. Depois, fechar uma única preparação de entradas por experimento, incluindo ausências e extremos. Por fim, planejar uma comparação pequena, com critérios definidos antes de executar.

Qualquer nova subdivisão das mesmas 520 pessoas deve ser descrita como uma reorganização de dados já explorados. Uma avaliação externa nova continua dependendo de dados não usados no processo.

O registro numérico desta auditoria está em `tmp/auditoria_preprocessamento.json`. Nenhum novo classificador foi treinado nesta revisão.

## Aprofundamento dos pontos 3 e 4

### Formatos e hipótese de unidades

Voltamos aos textos dos valores no arquivo original, antes da conversão para `float`.

| Campo | Primeiro grupo | Segundo grupo |
|---|---|---|
| `GLUCOSE` | 44 valores de 3,1 a 21,3, todos escritos com ponto decimal | 417 valores de 47 a 500, todos escritos como inteiros |
| `HEMOGLOBIN` | 355 valores de 4,7 a 13,1, todos escritos com ponto decimal | 43 valores de 27 a 116, todos escritos como inteiros |

Essa separação é compatível com a hipótese de unidades diferentes. Formato e magnitude não confirmam a unidade de cada registro. A descrição consultada da competição não fornece essa confirmação. A premissa anterior de unidade única permanece como uma decisão a reabrir; esta análise não a substituiu automaticamente.

Para glicose, a documentação do [CDC](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2015/DataFiles/GLU_i.htm) usa `mmol/L = mg/dL × 0,05551`. Sob a hipótese de que o grupo de 44 valores esteja em mmol/L, 5,5 corresponderia a aproximadamente 99,08 mg/dL. O intervalo desse grupo se tornaria 55,85 a 383,71 mg/dL.

Se mantivermos a hipótese de que `HEMOGLOBIN` representa HbA1c, existem as apresentações NGSP em porcentagem e IFCC em mmol/mol. A equação publicada pelo [NGSP](https://ngsp.org/ifccngsp.asp) é `NGSP (%) = 0,09148 × IFCC (mmol/mol) + 2,152`. Sob essa hipótese, 38 corresponderia a 5,63% e 116 a 12,76%. O grupo de 43 inteiros passaria ao intervalo de 4,62% a 12,76%, próximo ao intervalo do grupo decimal.

Simulamos essas conversões somente em memória. Considerando os 398 valores preenchidos de hemoglobina, antes do filtro dos modelos, a média iria de 11,01 a 6,80 e o desvio padrão de 13,41 a 1,94. Essa coerência numérica reforça o interesse da hipótese, mas não comprova as unidades nem demonstra melhoria de classificação. Os arquivos e os modelos foram preservados.

### Ausências reais e valores que o modelo tornou ausentes

| Situação no CSV padronizado | Quantidade |
|---|---:|
| Glicose e hemoglobina preenchidas | 357 |
| Glicose vazia e hemoglobina preenchida | 41 |
| Glicose preenchida e hemoglobina vazia | 104 |
| Ambas vazias | 18 |

Portanto, há 59 glicoses e 122 hemoglobinas vazias. São 163 amostras com pelo menos um desses campos vazio. O número 164 usado no diagnóstico dos modelos inclui mais um registro: a hemoglobina 116, tratada como ausente pela regra `HEMOGLOBIN > 100`.

Se aquele valor estiver em IFCC, a regra de descartá-lo antes de converter precisa ser revista. Se não confirmarmos essa interpretação, sua situação continua pendente. Isso mostra a importância de resolver a unidade antes de classificar valores como inválidos e estimar os ausentes.

Uma opção a discutir depois das unidades é combinar a mediana do treinamento com um indicador de ausência. Assim, um valor medido e um valor preenchido podem ser distinguidos pelo modelo. A coluna de ausência deve registrar o estado original, antes do preenchimento. Essa opção ainda não foi implementada nesta revisão, e sua utilidade precisará ser avaliada separadamente.
