# Plano de trabalho

## 1. Preparação

- [x] Organizar diretórios e documentação inicial.
- [ ] Confirmar integrantes, requisitos adicionais e prazo de apresentação.
- [ ] Obter a base pelo acesso autorizado à competição.
- [ ] Documentar arquivos, atributos, identificadores, rótulo e formato da submissão.
- [ ] Definir ambiente Python e registrar dependências efetivamente utilizadas.

## 2. Dados e validação

- [ ] Analisar somente o treinamento: dimensões, tipos, ausências, duplicatas e classes.
- [ ] Verificar se há múltiplas amostras por paciente ou outros grupos dependentes.
- [ ] Definir partições compartilhadas, sementes e identificadores estáveis das linhas.
- [ ] Documentar decisões de pré-processamento e suas justificativas.

## 3. Modelos

- [ ] Construir versões iniciais de KNN, árvore e rede neural.
- [ ] Comparar nas mesmas partições e métricas.
- [ ] Ajustar hiperparâmetros com orçamento de busca registrado.
- [ ] Definir e avaliar ensemble de árvore e rede neural.
- [ ] Analisar variação entre partições, erros e custo de execução.

## 4. Entrega

- [ ] Escolher configuração final com base na validação de treinamento.
- [ ] Congelar configuração e treinar no conjunto de treinamento completo.
- [ ] Gerar previsões no formato exigido pela competição.
- [ ] Registrar submissões separadamente dos resultados de validação.
- [ ] Preparar execução em Linux e fixar dependências.
- [ ] Validar execução do início ao fim em ambiente limpo.
- [ ] Finalizar README, comparação, limitações e slides.

## Critério de conclusão de um experimento

Uma execução está documentada quando possui identificador, hipótese, configuração, versão do código, ambiente, partições, sementes, métricas por divisão, resumo, artefatos e conclusão. Resultados ausentes não devem ser preenchidos com estimativas.
