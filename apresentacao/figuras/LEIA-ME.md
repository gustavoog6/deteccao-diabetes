# Figuras da apresentação

Todas as figuras foram geradas a partir dos dados do treino (520 pacientes), com os mesmos números dos notebooks. O estilo é escuro (fundo `#0B1220`), com fontes Poppins nos títulos e Inter no texto. Para combinar, use esse mesmo fundo nos slides.

As imagens não têm título: o título fica no slide. Cada uma ocupa a área abaixo do título (proporção próxima de 16:9).

## Qual figura vai em qual slide

| Slide | Arquivo | Como animar |
|---|---|---|
| 2. Gráfico das submissões | `anim_01_submissoes.mp4` ou `res_01_submissoes_1.png` a `_7.png` | vídeo com reprodução automática, ou os 7 PNGs em 7 slides com transição Morph |
| 4. Os dados / grafias | `pre_01_grafias.png` | aparecer (fade) |
| 7. Glicose em duas unidades | `anim_02_glicose.mp4`, ou `pre_02_glicose_antes.png` → `pre_02_glicose_depois.png` | vídeo, ou dois slides com Morph |
| 7. HbA1c (opcional) | `pre_02_hba1c_antes.png` → `pre_02_hba1c_depois.png` | dois slides com Morph |
| 8. Efeito da correção | `anim_03_separacao.mp4`, ou `res_02_separacao_antes.png` → `res_02_separacao_depois.png` | vídeo (é a animação mais impactante) |
| 9. Onde o modelo errava | `res_03_diabeticos_perdidos.png` | aparecer |
| 9. Mapa de ausentes | `pre_04_mapa_ausentes.png` | aparecer |
| 10. Um modelo para cada caso | `res_04_submodelos.png` | aparecer |
| 11. Tratamento da base | `pre_05_pipeline_passo1.png` a `_passo6.png` | 6 slides com Morph: cada etapa acende |
| 11. Valores impossíveis (opcional) | `pre_03_valores_impossiveis.png` | aparecer |
| 12. Modelo final | `res_07_modelos.png` | aparecer |
| 13. Como construí o KNN | `mod_01_knn.png` | aparecer: primeiro o desenho dos vizinhos, depois os passos e a curva de K |
| 14. Como construí a árvore | `mod_02_arvore.png` e `res_05_arvore.png` | as regiões de decisão; num segundo clique (ou slide), a árvore desenhada |
| 15. Como construí a rede | `mod_03_rede.png` | aparecer: a rede, depois os passos e a curva de neurônios |
| 16. Avaliação | `res_06_matriz_confusao.png` | aparecer |

## Como animar

**PowerPoint (recomendado):**

- **Vídeo:** Inserir → Vídeo → Este dispositivo. Em "Reprodução", marque "Iniciar: automaticamente".
- **Morph (antes → depois, passo a passo):** coloque a imagem "antes" num slide, duplique o slide e troque pela imagem "depois" na mesma posição e tamanho. No segundo slide, use Transições → Morph. Para o pipeline, faça 6 slides seguidos, um por passo.
- **Aparecer:** Animações → Esmaecer, com "Iniciar: ao clicar".

**Google Slides:** aceita vídeo (do Google Drive) e transição "Dissolver" entre slides, que funciona como um Morph simples para as imagens antes/depois.

**Canva:** aceita os MP4 e tem a transição "Combinar", parecida com o Morph.

## Prompts para imagens ilustrativas (GPT ou Gemini)

Use só para capa e divisórias. Peça sempre sem texto na imagem: as IAs erram letras.

1. **Capa:** "Ilustração digital em proporção 16:9, fundo azul-marinho muito escuro (#0B1220). Uma gota de sangue estilizada formada por pontos e linhas de dados luminosos em azul (#3B8BEB) e um pouco de laranja, como uma rede de partículas. Estilo minimalista, tecnológico, alto contraste, sem texto, sem pessoas."
2. **Divisória "os dados estavam sujos":** "Ilustração 16:9, fundo azul-marinho escuro. Planilhas e números flutuando de forma desorganizada, alguns em laranja brilhante, como peças fora do lugar. Estilo flat minimalista, iluminação suave, sem texto legível."
3. **Divisória "a virada":** "Ilustração 16:9, fundo azul-marinho escuro. Dois grupos de pontos laranja e cinza se reorganizando em uma única distribuição azul ordenada, como partículas se alinhando. Estilo minimalista, sensação de ordem surgindo do caos, sem texto."
4. **Divisória "modelo final":** "Ilustração 16:9, fundo azul-marinho escuro. Três caminhos luminosos azuis (representando três modelos) convergindo para um único ponto brilhante. Estilo abstrato e tecnológico, sem texto."
5. **Fundo neutro:** "Textura de fundo 16:9, azul-marinho muito escuro (#0B1220), com uma grade sutil de pontos e linhas finas em azul quase invisível, para usar atrás de gráficos. Sem texto, sem elementos no centro."

## Cores, para manter tudo igual

| Uso | Cor |
|---|---|
| Fundo | `#0B1220` |
| Texto | `#F1F5F9` |
| Texto secundário | `#94A3B8` |
| Destaque (dados corrigidos, modelo final) | `#3B8BEB` |
| Problema / antes | `#F07A3E` |
| Controle | `#22B07D` |
| Diabetes | `#E5606A` |
