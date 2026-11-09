# Detecção de Diabetes

Trabalho da disciplina **GBC-212 Mineração de Dados** (UFU), Prof. Murillo G. Carneiro. Competição Kaggle "deteccao-de-diabetes": classificar cada paciente em **controle (0)** ou **diabetes (1)**.

**Equipe:** Gustavo Oliveira Guimarães, Higor Pereira Martins e Vitória Ferreira Ramos de Lima.

**Modelo final:** voto da maioria entre KNN, árvore de decisão e rede neural, cada um com um submodelo por padrão de exames disponíveis. F1-macro de **0,912** na validação cruzada (só no treino) e **0,89900** no placar público do Kaggle, acima do baseline do professor (0,872).

## Executar (Linux / Fedora)

```bash
# 1. Python 3 (o Fedora normalmente já vem com ele)
sudo dnf install -y python3 python3-pip git

# 2. Baixar o repositório
git clone https://github.com/gustavoog6/deteccao-diabetes.git
cd deteccao-diabetes

# 3. Colocar os dados da competição (não estão no repositório, ver "Dados" abaixo)
#    dados/kaggle-training/train.csv  e  dados/kaggle-test/test.csv

# 4. Ambiente isolado com as bibliotecas
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 5. Modelo final: classificar um arquivo no formato do Kaggle
cd Mod8_Unidades
python3 prever.py /caminho/para/externo.csv --saida previsoes_externo.csv
```

- **Tratamento automático:** `prever.py` treina com `dados/kaggle-training/train.csv` e aplica o mesmo tratamento da base ao treino e ao arquivo classificado.
- **Métricas:** se o arquivo tiver a coluna `class`, o script também mostra F1-macro, precisão, recall de cada classe e a matriz de confusão.
- **Conferência:** `python3 prever.py ../dados/kaggle-test/test.csv` deve gerar 143 pacientes com diabetes e 169 controles, idênticos a `submissao_voto3_padroes.csv`.
- **Validação cruzada:** `python3 validar.py` refaz a validação cruzada e mostra os números deste README (cerca de 25 s).

Os Modelos 9, 10 e 11 funcionam do mesmo jeito: entre na pasta e rode `python3 prever.py ARQUIVO.csv` ou `python3 validar.py`.

## Modelos executáveis

Cada pasta é independente e traz o próprio tratamento da base (`limpeza.py`), a lógica de submodelos (`padroes.py`), a definição do modelo (`modelo_final.py`), os scripts `prever.py` e `validar.py`, a submissão gerada e um README detalhado.

| Pasta | Modelo | F1-macro (validação) | Recall diabetes | Recall controle | Kaggle |
|---|---|---|---|---|---|
| [`Mod8_Unidades`](Mod8_Unidades/README.md) | **Voto dos 3 (modelo final)** | **0,912** | 0,885 | 0,942 | **0,89900** |
| [`Mod9_KNN_Padroes`](Mod9_KNN_Padroes/README.md) | KNN, K = 11 | 0,896 | 0,854 | 0,942 | |
| [`Mod10_AD_Padroes`](Mod10_AD_Padroes/README.md) | Árvore: entropia, profundidade 4, folha 5 | 0,894 | 0,881 | 0,907 | |
| [`Mod11_RN_Padroes`](Mod11_RN_Padroes/README.md) | Rede neural: 8 neurônios sigmoide | 0,886 | 0,870 | 0,904 | |

A validação é cruzada e estratificada, com 5 partes × 4 repetições, feita só no treino. Usamos a semente 2026 para escolher os hiperparâmetros e a 777 para medir. O teste do Kaggle não foi usado em nenhuma escolha.

## Tratamento da base (aula 2)

O mesmo `limpeza.py` está em cada pasta de modelo. Todas as regras são aplicadas paciente a paciente. Medianas são calculadas só com o treino.

| Etapa | O que foi feito | Quantos |
|---|---|---|
| 1. Duplicatas | Pacientes repetidos, iguais em tudo menos no `id` | 20 (540 → 520) |
| 2. Textos | Grafias unificadas (sexo, histórico familiar, atividade, fumo); pressão `120/80` separada em sistólica e diastólica | 52 grafias → 11 categorias |
| 3. Impossíveis | Alturas em metros → cm; idades 0, −1 ou 999 recalculadas pelo ano do exame − ano de nascimento | 102 alturas, 6 idades |
| 4. Unidades | Glicose mmol/L × 18,016; HbA1c IFCC → %: 0,09148 × v + 2,152; peso em libras ÷ 2,2046 | 44 + 43 + 23 |
| 5. Extremos | Triglicerídeos limitados a 1000 | 3 |
| 6. Ausentes | Cada paciente vai para o submodelo dos exames que tem (glicose e HbA1c / só glicose / só HbA1c / nenhum), sem inventar o exame | 163 pacientes |

## Estrutura do repositório

```
Trab_MDados/
├── README.md                  este arquivo
├── requirements.txt           bibliotecas Python
├── dados/                     onde colocar train.csv e test.csv do Kaggle (não versionados)
├── Mod8_Unidades/             MODELO FINAL: voto dos 3, executável
├── Mod9_KNN_Padroes/          KNN do voto, executável + notebook
├── Mod10_AD_Padroes/          árvore do voto, executável + notebook
├── Mod11_RN_Padroes/          rede neural do voto, executável + notebook
├── Mod1_KNN/ … Mod7_RF/       histórico: tentativas anteriores (notebooks e READMEs)
├── resultados/                buscas e submissões do histórico (Modelos 1 a 7)
├── apresentacao/              slides (.pptx), figuras e vídeos
└── docs/                      decisões, histórico, metodologia e guia de estudo
```

## Histórico das submissões

| # | Submissão | Pasta | Kaggle |
|---|---|---|---|
| 1 | KNN K=11 com peso maior para glicose e HbA1c | `Mod1_KNN` | 0,82897 |
| 2 | KNN sem glicose na distância quando ausente | `Mod1_KNN` | 0,80570 |
| 3 | Árvore com 4 atributos | `Mod2_AD` | 0,83018 |
| 4 | KNN + árvore (média dos apoios) | `Mod5_KNN_AD` | 0,84382 |
| 5 | KNN com unidades corrigidas | `Mod8_Unidades` (v1) | 0,85692 |
| 6 | Média dos 3 com unidades corrigidas | `Mod8_Unidades` (v1) | 0,86649 |
| 7 | **Voto dos 3 por padrão de exames** | `Mod8_Unidades` (v2) | **0,89900** |

As tentativas 1 a 4 mexiam só no modelo: dezenas de milhares de combinações (Modelos 1 a 7) chegavam a 91% na validação, mas ficavam em 84% no Kaggle (sobreajuste). Os saltos vieram dos dados: unidades misturadas e exames ausentes. A história completa está em [`docs/HISTORICO.md`](docs/HISTORICO.md) e [`docs/DECISOES.md`](docs/DECISOES.md).

Os notebooks dos Modelos 1 a 7 ficam como registro. Eles leem `dados/treinamento_padronizado.csv` (gerado por `dados/01_exploracao_padronizacao.ipynb` a partir do `train.csv`) e os arquivos de `resultados/`, e devem ser abertos a partir da própria pasta.

## Documentação

- [Decisões](docs/DECISOES.md) e [histórico](docs/HISTORICO.md) do projeto
- [Metodologia](docs/METODOLOGIA.md), [escopo das aulas](docs/ESCOPO_AULAS.md) e [revisão do pré-processamento](docs/REVISAO_PREPROCESSAMENTO.md)
- [Guia de estudo da apresentação](docs/GUIA_ESTUDO_APRESENTACAO.md), slide a slide
- [Apresentação](apresentacao/README.md)

## Dados

Os dados são da competição da turma no Kaggle e de **uso restrito à disciplina**, por isso **não estão neste repositório**. Para executar, coloque os arquivos da competição em:

```
dados/kaggle-training/train.csv
dados/kaggle-test/test.csv
```

O `.gitignore` impede que arquivos `.csv` da pasta `dados/` sejam enviados por engano. As saídas dos notebooks que mostravam linhas individuais de pacientes foram removidas; ficaram só tabelas agregadas e gráficos.

