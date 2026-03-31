# Manual de Utilização — Sistema de Controle de Avaliação de Desempenho Docente (v1)

## Índice
1. Visão geral
2. Navegação principal
3. Dashboard
4. Evidências
5. Regras
6. Alertas
7. Check-ins
8. Relatório
9. ChatGPT (MVP)
10. Onde ficam as evidências no banco
11. Palavras‑chave úteis

---

## 1. Visão geral
Aplicação local em **Streamlit** com banco **SQLite**. Uso individual: registrar atividades, anexar evidências, aplicar regras de pontuação, revisar riscos/alertas, registrar check-ins, gerar relatório anual e obter sugestões consultivas (MVP ChatGPT).

## 2. Navegação principal
Na sidebar, escolha:
- Dashboard
- Evidências
- Regras
- Alertas
- Check-ins
- Relatório
- ChatGPT (MVP)

Cada item abre a respectiva tela descrita abaixo.

## 3. Dashboard
Objetivo: visão anual resumida.
- **Seletor de ano**: escolhe o ano ativo.
- **Cards por fator** (Formação, Funcional, Produção):
  - Pontuação estimada / meta
  - Faltante
  - Badge de risco (baixo/médio/alto)
- **Alertas e pendências prioritárias**: lista gerada automaticamente.
- **Atividades recentes**: últimas atividades do ano.
- **Sugestões do ChatGPT**: sugestões salvas (somente leitura).
- Botões rápidos (placeholders): Nova atividade, Gerar relatório, Analisar com ChatGPT, Registrar check-in.

## 4. Evidências
Objetivo: anexar e consultar evidências de atividades.
- Seletor de atividade (por título/data).
- Formulário:
  - Tipo (certificado, portaria, ata, email, declaração, pdf, imagem, link, material_didatico, print, outro)
  - Nome do arquivo (opcional)
  - Caminho/URL (opcional)
  - Descrição (opcional)
  - Obrigatória? / Aprovada?
  - Salva com data/hora atual
- Lista de evidências da atividade (tabela).
- Ao salvar, pendências/alertas são recalculados automaticamente.
- As evidências não são copiadas nem armazenadas pelo sistema; apenas os metadados ficam no banco SQLite (app/database.sqlite).

Tabela: evidencias
Coluna que guarda o caminho/URL do arquivo: caminho_arquivo (texto).
Ou seja: você salva o arquivo onde quiser (disco local, rede, nuvem) e registra o caminho/URL nessa coluna via tela de Evidências; o banco só referencia esse caminho.

## 5. Regras
Objetivo: consultar regras padrão e gerir regras personalizadas.
- Aba **Regras padrão**: tabela somente leitura (fator, tipo de fórmula, base, teto).
- Aba **Personalizadas**:
  - Lista de regras criadas.
  - Selecionar regra → desativar ou duplicar.
  - Regra desativada deixa de ser elegível para novas atividades.
- Aba **Nova regra personalizada**:
  - Campos: nome, fator, subtipo, descrição, justificativa (obrigatória), tipo de fórmula (fixo, por_unidade, por_hora, intervalo/manual), valor base, unidade/divisor, teto, evidência necessária, origem do documento, ativa.
  - Prévia textual da fórmula exibida antes de salvar.

## 6. Alertas
Objetivo: tratar pendências e riscos.
- Filtros: fator, tipo, severidade, status (abertos/resolvidos).
- Cada alerta em um “expander” mostrando:
  - Severidade, tipo, mensagem, fator, atividade relacionada.
  - Recomendação (quando existir).
  - Ação: “Abrir atividade” (mostra dados) ou “Marcar resolvido”.
- Estado “resolvido” fica salvo no banco.

## 7. Check-ins
Objetivo: registrar revisões periódicas e visualizar evolução.
- Tabela de histórico (data, fator/geral, pontuação acumulada, risco, pendências).
- Gráfico de linha da evolução de pontuação (quando houver dados).
- Formulário de novo check-in:
  - Data, fator (geral ou específico), pontuação acumulada, risco (baixo/médio/alto), pendências, nota.
  - Check-in “geral” atualiza `ultima_revisao` do ano.

## 8. Relatório
Objetivo: gerar relatório anual em Markdown/CSV.
- Seleciona o ano (primeiro ano disponível).
- Prévia em Markdown com:
  - Resumo por fator (estimada/confirmada)
  - Lista de atividades
  - Pendências abertas
  - Regras personalizadas usadas
  - Observações finais (campo livre no texto)
- Download:
  - `relatorio_<ano>.md`
  - `atividades_<ano>.csv`
  - PDF não incluído (mantido fora do escopo mínimo).

## 9. ChatGPT (MVP)
Objetivo: suporte consultivo (sem alterar dados automaticamente).
- Modos: análise do ano, por fator, por atividade, redação assistida.
- Consentimento: checkbox “usar meu perfil de escrita”; persiste em `configuracoes_usuario`.
- Privacidade: apenas dados selecionados pelo usuário; sem alterações automáticas no banco.
- Geração (stub) → exibe sugestão → botão “Salvar sugestão” grava em `sugestoes_chatgpt`.
- Lista de sugestões salvas (tabela).

## 10. Onde ficam as evidências no banco
- Tabela: `evidencias`
- Principais campos: `atividade_id`, `tipo`, `caminho_arquivo`, `descricao`, `data_anexacao`, `obrigatoria`, `aprovada`.
- Relacionamento: `evidencias.atividade_id` → `atividades.id`.

## 11. Palavras‑chave úteis (links internos)
- [Manual de Utilização — Sistema de Controle de Avaliação de Desempenho Docente (v1)](#manual-de-utilização--sistema-de-controle-de-avaliação-de-desempenho-docente-v1)
  - [Índice](#índice)
  - [1. Visão geral](#1-visão-geral)
  - [2. Navegação principal](#2-navegação-principal)
  - [3. Dashboard](#3-dashboard)
  - [4. Evidências](#4-evidências)
  - [5. Regras](#5-regras)
  - [6. Alertas](#6-alertas)
  - [7. Check-ins](#7-check-ins)
  - [8. Relatório](#8-relatório)
  - [9. ChatGPT (MVP)](#9-chatgpt-mvp)
  - [10. Onde ficam as evidências no banco](#10-onde-ficam-as-evidências-no-banco)
  - [11. Palavras‑chave úteis (links internos)](#11-palavraschave-úteis-links-internos)
