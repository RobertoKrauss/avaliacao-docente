# Manual de Utilização — Sistema de Avaliação de Desempenho Docente (v1)

## Índice
1. Visão geral
2. Navegação principal
3. Dashboard
4. Atividades (nova e editar + evidências)
5. Regras de pontuação
6. Alertas e pendências
7. Check-ins / Revisões
8. Relatório anual
9. ChatGPT (MVP)
10. Importar / Exportar CSV
11. Sugestão de pontuação
12. Onde ficam as evidências no banco
13. Palavras‑chave úteis

---
## 1. Visão geral
Aplicação local em **Streamlit** com banco **SQLite**. Uso individual: registrar atividades, anexar evidências, aplicar regras de pontuação, revisar riscos/alertas, registrar check-ins, gerar relatório anual e salvar sugestões consultivas (MVP ChatGPT). Nenhuma automação externa é feita.

## 2. Navegação principal
Menu lateral (radio):
- Dashboard
- Atividades
- Regras
- Alertas
- Check-ins
- Relatório
- ChatGPT (MVP)
- Import/Export
- Ajuda (exibe este manual)

## 3. Dashboard
Objetivo: visão resumida do ano selecionado.
- Seletor de ano.
- Botões rápidos: Nova atividade, Gerar relatório, Analisar com ChatGPT, Registrar check-in.
- Cards por fator (Formação, Funcional, Produção): pontuação estimada/meta, faltante e badge de risco.
- Blocos: Alertas prioritários, Atividades recentes, Sugestões do ChatGPT (somente leitura).

## 4. Atividades (nova e editar + evidências)
### Nova atividade
Campos: título, data, fator (formacao/funcional/producao), regra, quantidade, carga horária, valor manual (se aplicável), status. Após salvar, é oferecido formulário para anexar evidência à última atividade criada.

### Editar atividade
- Seletor de atividade (usa título + data). Ao vir de um alerta, já abre na aba **Editar** e pré-seleciona a atividade.
- Edição dos mesmos campos (título, data, fator, regra, quantidade, carga, valor manual, status).
- **Evidências desta atividade**: tabela em card; cada linha mostra tipo, nome, caminho, datas, flags (obrigatória/aprovada) e botão **Apagar** (soft delete).
- **Anexar nova evidência**: tipo, nome, caminho/URL, descrição, data do documento, obrigatória?, aprovada?.

Observação: apenas metadados são gravados; os arquivos permanecem onde você salvá-los (disco/rede/nuvem) e o campo `caminho_arquivo` referencia o local.

## 5. Regras de pontuação
- **Regras padrão**: leitura das regras fixas (fator, tipo, base, unidade, teto).
- **Personalizadas**: lista, selecionar, desativar, duplicar e **editar** (formulário pré-preenchido). Regra desativada deixa de ser elegível para novas atividades.
- **Nova regra personalizada**: nome, fator, subtipo, descrição, justificativa (obrigatória), tipo de fórmula (fixo, por_unidade, por_hora, intervalo, manual), valor base, unidade/divisor, teto, evidência necessária, origem do documento, ativa. Prévia textual exibida antes de salvar.

## 6. Alertas e pendências
- Filtros: fator, tipo, severidade, status (abertos/resolvidos).
- Cada alerta mostra severidade, mensagem, fator, atividade (quando houver), recomendação e botões:
  - **Abrir atividade** → navega direto para **Atividades > Editar** com a atividade selecionada.
  - **Marcar resolvido** → persiste no banco.
- Alertas órfãos (atividade inexistente) são ocultados automaticamente.
- Exemplos de recomendações: evidência faltante, valor manual faltante, risco alto (meta <50%), pontuação baixa (50–80% da meta), revisão atrasada.

## 7. Check-ins / Revisões
- Histórico: data, fator/geral, pontuação acumulada, risco, pendências; gráfico de linha quando há dados.
- Formulário “Novo check-in”: data, fator (geral ou específico), pontuação acumulada, risco (baixo/médio/alto), pendências, nota. Check-in geral atualiza `ultima_revisao` do ano.

## 8. Relatório anual
- Seleciona o ano ativo.
- Prévia em Markdown com resumo por fator, atividades, pendências, regras personalizadas usadas, observações finais.
- Downloads: `relatorio_<ano>.md` e `atividades_<ano>.csv`.

## 9. ChatGPT (MVP)
- Modos: análise do ano, por fator, por atividade, redação assistida.
- Consentimento: checkbox “usar meu perfil de escrita”; configurações salvas em `configuracoes_usuario`.
- Somente leitura/consulta: sugestões não alteram o banco automaticamente. Botão “Salvar sugestão” grava em `sugestoes_chatgpt`.

## 10. Importar / Exportar CSV
### Exportar
- Botão “Gerar ZIP com CSVs” gera um ZIP contendo um arquivo CSV por tabela do SQLite (todas as colunas). O cabeçalho do CSV segue exatamente os nomes das colunas da tabela.

### Importar
- Envie um ZIP com **um CSV por tabela**. O nome do arquivo deve ser exatamente `nome_da_tabela.csv` (ex.: `atividades.csv`, `evidencias.csv`, `regras_pontuacao.csv`, `anos_avaliacao.csv`, etc.).
- O cabeçalho do CSV precisa corresponder 1:1 aos nomes de colunas da tabela.
- Modos:
  - **Mesclar (merge)**: `INSERT OR REPLACE` linha a linha.
  - **Sobrescrever tudo**: apaga a tabela antes de inserir (cuidado: substitui todo o conteúdo daquela tabela).
- Campo de texto: use UTF-8; separador padrão `,` (vírgula); decimal em ponto.
- Ordem das colunas não é rígida, mas o nome precisa coincidir; colunas ausentes serão `NULL`.
- Recomendado exportar uma vez para pegar o modelo de CSV (estrutura e colunas) antes de preparar uma carga.

## 11. Sugestão de pontuação

**Sugestão de pontuação — referência de indicadores**

| PONTUAÇÃO DOS INDICADORES PARA A AVALIAÇÃO DO SERVIDOR DOCENTE                                               |        PONTOS |
| ------------------------------------------------------------------------------------------------------------ | ------------: |
| **Fator de Formação / Atualização Continuada (máximo de 15 pontos)**                                         |               |
| Participação em eventos com certificado de frequência (Palestras, Seminários...)                             | 2 pts./evento |
| Participação em eventos com certificado de frequência (Congressos...)                                        | 5 pts./evento |
| Participação em cursos de atualização e/ou estágios.                                                         |    5 pts./10h |
| Exercício de atividades profissionais externas correlatas à área de atuação.                                 |    5 pts./10h |
| Participação em cursos de pós-graduação - Especialização.                                                    |       15 pts. |
| Participação em cursos de pós-graduação - Mestrado / Doutorado.                                              |       15 pts. |
| Membro de banca de avaliação de Estágio Supervisionado (exceto orientador e co-orientador).                  |        3 pts. |
| Membro de banca de avaliação de Monografia e Trabalho de Final de Curso (exceto orientador e co-orientador). |        5 pts. |
| Membro de banca de dissertação de mestrado (exceto orientador e co-orientador).                              |       10 pts. |
| Membro de banca de tese de doutorado (exceto orientador e co-orientador).                                    |       15 pts. |
| Atualização das legislações vigentes para Chefias.                                                           |       15 pts. |

| **Fator Funcional - Pedagógico (máximo de 35 pontos)**                                                                                                |                   |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------: |
| Orientação de Estágio Supervisionado curricular                                                                                                       | 10 pts./orientado |
| Orientação de Trabalho Final de Curso.                                                                                                                |  20 pts./trabalho |
| Orientação de aluno de mestrado.                                                                                                                      |           30 pts. |
| Orientação de aluno de doutorado.                                                                                                                     |           35 pts. |
| Orientação de alunos inscritos nos programas de iniciação científica da UTFPR.                                                                        |           20 pts. |
| Orientação de bolsista de programa de Desenvolvimento Científico Regional, de Recém-Doutor e de Pós-Doutoramento.                                    |           20 pts. |
| Orientação de bolsista com titulação de mestre ou doutor, participante de projetos institucionais (PADCT, CNPq).                                      |           20 pts. |
| Co-orientação de alunos inscritos nos programas de iniciação científica da UTFPR.                                                                     |           10 pts. |
| Co-orientação de aluno de mestrado.                                                                                                                   |           10 pts. |
| Co-orientação de aluno de doutorado.                                                                                                                  |           10 pts. |
| Desenvolvimento de software didático.                                                                                                                 |           35 pts. |
| Autor de livro técnico/científico publicado por Editora.                                                                                              |     35 pts./livro |
| Autor de capítulo de livro técnico/científico publicado por Editora.                                                                                  |  20 pts./capítulo |
| Editoração ou organização de livro técnico/científico ou Anais de Congressos de Sociedades Científicas (pontos divididos entre editores).             |     35 pts./livro |
| Autoria de tradução de livro técnico/científico publicado por Editora.                                                                                |     30 pts./livro |
| Editor-chefe de revista científica de circulação internacional.                                                                                       |           10 pts. |
| Editor associado de revista científica de circulação nacional.                                                                                        |            5 pts. |
| Membro de Conselho Científico e Editorial de revista científica de circulação internacional.                                                          |            5 pts. |
| Membro de Conselho Científico e Editorial de revista científica de circulação nacional.                                                               |            3 pts. |
| Participação em reunião de departamento.                                                                                                              |       0 a 10 pts. |
| Entrega da documentação acadêmica no prazo.                                                                                                           |       0 a 10 pts. |

| **Fator de Produção Institucional (máximo de 20 pontos)**                                                                                   |                      |
| ------------------------------------------------------------------------------------------------------------------------------------------- | -------------------: |
| Cargos nomeados por Portaria.                                                                                                               |              10 pts. |
| Chefe de grupos de disciplinas.                                                                                                             |              10 pts. |
| Presidência de Comissão designada por Portaria.                                                                                             |               5 pts. |
| Membros de Comissão designada por Portaria de Diretoria.                                                                                    |               5 pts. |
| Membro de banca de concurso público para provimento de cargo de Professor.                                                                  |               5 pts. |
| Membro de banca de teste seletivo para provimento de cargo de Professor Substituto.                                                         |               5 pts. |
| Membro de Conselho Departamental e Colegiado.                                                                                               |               5 pts. |
| Participação da organização de eventos da UTFPR.                                                                                            |    10 pts./atividade |
| Responsável pelos Laboratórios.                                                                                                             |              10 pts. |
| Responsável pelas Atividades Complementares.                                                                                                |              10 pts. |
| Responsável pela Orientação de Estágio.                                                                                                     |              10 pts. |
| Responsável pelo Trabalho de Diplomação.                                                                                                    |              10 pts. |
| Assessor de Coordenação.                                                                                                                    |              10 pts. |
| Participação em eventos, representando a Instituição ou com apresentação de trabalho ou como palestrante em evento de abrangência nacional. | 10 pts./participação |

## 12. Onde ficam as evidências no banco
- Tabela: `evidencias`
- Campos principais: `atividade_id`, `tipo`, `caminho_arquivo`, `descricao`, `data_anexacao`, `obrigatoria`, `aprovada`, `data_validade`.
- Relacionamento: `evidencias.atividade_id` → `atividades.id`.
- Apenas metadados são armazenados; os arquivos ficam no local/URL informado.

## 13. Palavras‑chave úteis (links internos)
- [Visão geral](#1-visão-geral)
- [Navegação principal](#2-navegação-principal)
- [Dashboard](#3-dashboard)
- [Atividades](#4-atividades-nova-e-editar--evidências)
- [Regras](#5-regras-de-pontuação)
- [Alertas](#6-alertas-e-pendências)
- [Check-ins](#7-check-ins--revisões)
- [Relatório](#8-relatório-anual)
- [ChatGPT](#9-chatgpt-mvp)
- [Import/Export](#10-importar--exportar-csv)
- [Sugestão de pontuação](#11-sugestão-de-pontuação)
- [Evidências no banco](#12-onde-ficam-as-evidências-no-banco)
