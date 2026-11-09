# Dados

Dados da competição Kaggle "deteccao-de-diabetes" (GBC-212, UFU). **Uso restrito à disciplina:** os arquivos não estão no repositório. Coloque-os nas pastas indicadas abaixo para executar os modelos.

| Arquivo | Papel | Linhas | Observação |
|---|---|---|---|
| `kaggle-training/train.csv` | Treino | 540 (520 sem duplicados) | Tem a coluna `class` (0 = controle, 1 = diabetes) |
| `kaggle-test/test.csv` | Teste do Kaggle | 312 | Sem rótulo. Não foi usado em nenhuma escolha |
| `treinamento_padronizado.csv` | Treino com grafias padronizadas | 520 | Gerado ao executar `01_exploracao_padronizacao.ipynb`; usado só pelos Modelos 1 a 7 |
| `01_exploracao_padronizacao.ipynb` | Exploração inicial da base | | Grafias, duplicatas, ausentes |

Os Modelos 8 a 11 leem os arquivos originais do Kaggle e aplicam o tratamento completo pelo `limpeza.py` de cada pasta.

Colunas usadas: `GENDER`, `AGE`, `BIRTH_YEAR`, `EXAM_DATE`, `HEIGHT`, `WEIGHT`, `BLOOD_PRESSURE`, `SMOKER`, `PHYSICAL_ACTIVITY`, `FAMILY_HISTORY`, `GLUCOSE`, `HEMOGLOBIN`, `TRIGLYCERIDES`, `SODIUM`. Colunas administrativas (`PATIENT_CODE`, `COLLECTION_SITE`, `LAB_DEVICE`, `STUDY_PROTOCOL`, `BLOOD_TYPE`) não entram nos modelos.
