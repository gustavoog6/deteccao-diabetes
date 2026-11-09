# Registro de decisões

| ID | Data | Decisão | Motivo / situação |
| --- | --- | --- | --- |
| D001 | 2026-11-01 | Este diretório será a fonte de verdade | Pedido do responsável pelo projeto |
| D002 | 2026-11-01 | Separar os quatro modelos em pastas | Facilitar navegação e documentação específica |
| D003 | 2026-11-01 | Desenvolver inicialmente em notebooks Python | Facilitar exploração e explicação das etapas |
| D004 | 2026-11-01 | Compartilhar dados e partições entre modelos | Evitar cópias divergentes e permitir comparação justa |
| D005 | 2026-11-01 | Usar `Mod4_AD_RN` para árvore + rede neural | Simplificar caminhos; método de combinação pendente |
| D006 | 2026-11-01 | Propor F1-macro como critério principal local | Pendente confirmação após verificar avaliação e requisitos |
| D007 | 2026-11-05 | Desenvolver a rede neural com uma camada oculta, sigmoide, erro quadrático e retropropagação | Pedido do aluno, com a aula 6 como referência; comparação em `Mod3_RN/` |
| D008 | 2026-11-05 | Preparar a versão com atualização após cada exemplo para o próximo teste no Kaggle | Notebook 02; quatro entradas, 12 neurônios ocultos, uma saída, taxa 0,1 e 800 épocas, escolhidos por validação cruzada; a versão em lote fica registrada separadamente |
| D009 | 2026-11-05 | Comparar pares e trio mantendo os componentes fixos e escolher pela validação local | Pedido do aluno; busca registrada em `Mod6_KNN_AD_RN/`, com seleção, conferências e reserva separadas; indicação 25% KNN, 42,5% árvore e 32,5% rede, limite 45,5% |
| D010 | 2026-11-06 | Usar média e desvio padrão para a escala das novas versões de todos os modelos | Pedido do aluno; parâmetros ajustados somente no treinamento de cada parte; as experiências anteriores ficam como histórico |
| D011 | 2026-11-06 | Testar Random Forest e comparar com a variante bagging | Pedido do aluno; extensão documentada das árvores, com referência técnica própria e avaliação nas mesmas divisões |
| D012 | 2026-11-06 | Identificar a pontuação do placar como F1 macro e separar da acurácia | Página oficial conferida no navegador durante a auditoria; o enunciado também pede precisão e recalls por classe |

| D013 | 2026-11-06 | Corrigir unidades misturadas: glicose < 35 em mmol/L (× 18,016) e HbA1c > 20 em mmol/mol (fórmula NGSP) | Resolve a premissa aberta na revisão do pré-processamento; aula 2 (inconsistência); `Mod8_Unidades/` |
| D014 | 2026-11-06 | Corrigir peso > 140 como libras e limitar triglicerídeos a 1000 | Valores implausíveis de IMC e extremos; afeta só atributos clínicos |
| D015 | 2026-11-06 | Um submodelo por padrão de exames ausentes, em vez de preencher pela mediana | Os erros se concentravam nos diabéticos sem exame; aula 2 (ignorar o atributo ausente); validação 0,899 → 0,914 |
| D016 | 2026-11-07 | Random Forest testada no mesmo esquema e não adotada | Empatou ou ficou abaixo da média dos 3 em 3 sorteios; fora do material das aulas |
| D017 | 2026-11-07 | Modelo final: voto dos 3 por padrão de exames (`Mod8_Unidades/modelo_padroes.py`) | Validação 0,913; Kaggle público 0,89900; média dos 3 como segunda opção para o placar final |
| D018 | 2026-11-08 | Separar os componentes do voto nos Modelos 9 (KNN), 10 (árvore) e 11 (rede), cada um com notebook e submissão própria | Pedido do aluno; hiperparâmetros revalidados (K=11; profundidade 4 e folha 5); rede mantida em 8 neurônios (2 neurônios: +0,003, dentro do desvio de 0,03) para reproduzir o voto |
| D019 | 2026-11-08 | Corrigir as grafias `Moderat` e `Intensive` da atividade física; na árvore, escolher profundidade 4 e folha 5 entre as configurações empatadas, por ser a mais compacta | 3 pacientes no treino viravam ausentes; voto muda 1 paciente no teste; números da validação mudam na terceira casa |

## Pendências

- Estratégia de validação, número de divisões e sementes.
- Resultado da rede neural no Kaggle após o envio.
- Estratégia de combinação AD + RN.
- Esclarecer a agregação de precisão solicitada no enunciado; o placar está identificado como F1 macro.
- Ambiente e versões das dependências.
- Integrantes e requisitos adicionais do professor.

Acrescentar novas decisões com justificativa. Se uma decisão mudar, registrar a substituição sem apagar o histórico.
