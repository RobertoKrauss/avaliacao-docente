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
11. Onde ficam as evidências no banco
12. Palavras‑chave úteis

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
- **Exportar base**: botão “Gerar ZIP com CSVs” gera um ZIP com um CSV por tabela do SQLite (todas as colunas).
- **Importar base**: envie um ZIP com arquivos `nome_da_tabela.csv` (colunas idênticas às da tabela) e escolha:
  - **Mesclar (merge)**: `INSERT OR REPLACE` linha a linha.
  - **Sobrescrever tudo**: apaga a tabela e insere o conteúdo do CSV.
- Útil para backup, migração ou carga massiva.

## 11. Onde ficam as evidências no banco
- Tabela: `evidencias`
- Campos principais: `atividade_id`, `tipo`, `caminho_arquivo`, `descricao`, `data_anexacao`, `obrigatoria`, `aprovada`, `data_validade`.
- Relacionamento: `evidencias.atividade_id` → `atividades.id`.
- Apenas metadados são armazenados; os arquivos ficam no local/URL informado.

## 12. Palavras‑chave úteis (links internos)
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
- [Evidências no banco](#11-onde-ficam-as-evidências-no-banco)
