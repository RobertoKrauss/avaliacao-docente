# PRD.md — Sistema de Controle de Pontuação para Avaliação de Desempenho Docente

## 1. Objetivo

Criar um sistema pessoal de acompanhamento contínuo da avaliação de desempenho docente da UTFPR, focado em evitar perda de pontos nos fatores:

- Formação / Atualização Continuada
- Funcional–Pedagógico
- Produção Institucional

O sistema deverá funcionar como um “painel de controle anual”, permitindo:

1. Saber quantos pontos já foram obtidos.
2. Saber quais itens ainda faltam.
3. Detectar riscos de perda de pontuação antes do fechamento do ciclo.
4. Armazenar automaticamente evidências (PDFs, certificados, atas, comprovantes, links, portarias, prints).
5. Gerar relatórios prontos para SIAVI e para discussão com a chefia.

---

# 2. Contexto do Problema

No manual de avaliação docente da UTFPR, a pontuação individual é dividida em:

- Formação / Atualização Continuada — máximo 15 pontos
- Funcional–Pedagógico — máximo 35 pontos
- Produção Institucional — máximo 20 pontos

Os itens avaliados incluem:

## Formação / Atualização Continuada
- Participação em eventos
- Cursos de atualização
- Pós-graduação
- Participação em bancas

## Funcional–Pedagógico
- Orientações e estágios
- Desenvolvimento de material didático
- Aplicação de novas metodologias
- Participação em reuniões
- Entrega de documentação

## Produção Institucional
- Comissões, grupos de trabalho, colegiados, bancas
- Representação institucional
- Projetos institucionais
- Extensão e outras atividades institucionais

O problema atual é que essas evidências ficam espalhadas em:

- E-mails
- PDFs
- Certificados
- Pastas
- Moodle
- Planilhas
- Mensagens
- Memória pessoal

Resultado: pontos deixam de ser lançados porque a atividade foi esquecida ou não houve documentação adequada.

---

# 3. Visão Geral da Solução

Construir um sistema composto por:

1. Banco de atividades realizadas ao longo do ano.
2. Repositório de evidências.
3. Painel de pontuação em tempo real.
4. Alertas automáticos de itens faltantes.
5. Geração automática de relatório anual.

---

# 4. Padrões Externos Encontrados

## 4.1 Padrão “Evidence Portfolio”

Muito usado em universidades norte-americanas e australianas para tenure, promotion e faculty review.

Estrutura típica:

- Atividade
- Categoria
- Data
- Evidência
- Resultado
- Impacto
- Pontuação esperada

Exemplo:

| Campo | Exemplo |
|-------|----------|
| Categoria | Produção Institucional |
| Atividade | Participação na CPA-CM |
| Evidência | Portaria + ata + e-mail |
| Resultado | 12 reuniões realizadas |
| Impacto | Participação institucional relevante |
| Pontuação prevista | 4 pontos |

### Padrão a implementar
Cada atividade no sistema deverá possuir:

- título
- categoria
- subtipo
- data
- período
- descrição
- evidência anexada
- pontuação estimada
- status

Status:
- Planejada
- Em andamento
- Concluída
- Com evidência pendente
- Lançada na avaliação

---

## 4.2 Padrão “Gap Analysis Dashboard”

Usado em sistemas corporativos de RH e avaliação continuada.

O painel compara:

- Pontuação máxima
- Pontuação já atingida
- Pontuação faltante
- Risco

Exemplo:

| Fator | Máximo | Atual | Falta | Risco |
|-------|---------|--------|--------|--------|
| Formação | 15 | 6 | 9 | Alto |
| Funcional–Pedagógico | 35 | 28 | 7 | Médio |
| Produção Institucional | 20 | 18 | 2 | Baixo |

### Regra de risco

- Verde: >= 80% do máximo
- Amarelo: entre 50% e 79%
- Vermelho: < 50%

---

## 4.3 Padrão “Quarterly Review”

Universidades e empresas normalmente não esperam o final do ano.

Adotam revisão trimestral:

- Março
- Junho
- Setembro
- Novembro

Em cada revisão:

- atualizar atividades
- anexar certificados
- revisar pontos
- identificar lacunas
- planejar ações para o próximo trimestre

### Recomendação
Criar um alerta recorrente automático:

- Revisão 1: 15 de março
- Revisão 2: 15 de junho
- Revisão 3: 15 de setembro
- Revisão final: 15 de novembro

---

# 5. Tecnologias Recomendadas

## Opção 1 — Implementação Mais Simples

### Stack
- Google Drive
- Google Sheets
- Google Forms
- Google Apps Script

### Funcionamento

1. Formulário para cadastrar atividade.
2. Dados vão para uma planilha.
3. Evidências ficam em uma pasta no Google Drive.
4. Apps Script calcula pontuação automaticamente.
5. Dashboard mostra:
   - total por fator
   - atividades pendentes
   - gráficos
   - alertas

### Vantagens
- Muito rápido de implementar
- Gratuito
- Funciona no celular
- Fácil de compartilhar
- Fácil anexar PDFs e certificados

### Estrutura da planilha

Abas:

1. Atividades
2. Evidências
3. Pontuação
4. Dashboard
5. Relatório Anual

Campos da aba Atividades:

| Campo |
|-------|
| ID |
| Data |
| Categoria |
| Subcategoria |
| Atividade |
| Descrição |
| Evidência |
| Pontos previstos |
| Pontos confirmados |
| Status |
| Observações |

---

## Opção 2 — Implementação Melhor / Mais Organizada

### Stack
- Notion
- Google Drive
- Automação via Zapier ou Make

### Estrutura Notion

Database “Atividades”

Campos:

- Nome
- Categoria
- Pontuação
- Status
- Data
- Link da evidência
- Prazo
- Instituição
- Comentários

Views:

- Kanban por status
- Calendário
- Dashboard por categoria
- Lista “faltando evidência”

### Padrão usado externamente
Esse modelo é muito parecido com os “Faculty Activity Reporting Systems” usados por universidades como:

- University of Michigan
- Arizona State University
- University of Texas

---

## Opção 3 — Sistema Próprio em Python

Como você já trabalha com Python, Raspberry Pi, Windows 11 e dashboards, a melhor solução de longo prazo é um sistema próprio.

### Stack sugerida
- Python
- SQLite
- Streamlit
- PDF parser
- OCR
- Upload de arquivos

### Arquitetura

```text
Usuário
   ↓
Tela Streamlit
   ↓
Banco SQLite
   ↓
Pasta Evidências/
   ↓
Relatório PDF e CSV
```

### Funcionalidades

- Cadastro manual de atividade
- Upload de certificado
- OCR para extrair automaticamente:
  - nome do evento
  - data
  - carga horária
- Sugestão automática da categoria
- Cálculo automático de pontos
- Geração do relatório final em PDF

### Funcionalidade avançada

Importar automaticamente:

- e-mails do Gmail
- certificados do Google Drive
- PDFs
- reuniões da agenda

E sugerir:

“Esta atividade parece valer 2 pontos em Formação / Atualização Continuada.”

---

# 6. Requisitos Funcionais

## RF-01 — Cadastro de Atividade
O usuário poderá registrar uma atividade e associá-la a um dos três fatores.

## RF-02 — Upload de Evidência
O sistema deverá aceitar:

- PDF
- JPG
- PNG
- Link
- Documento do Drive

## RF-03 — Cálculo de Pontuação
O sistema deverá somar automaticamente os pontos por categoria.

## RF-04 — Alerta de Falta de Pontos
Quando um fator estiver abaixo de 70% da meta esperada para o mês, o sistema deverá gerar um alerta.

Exemplo:

“Produção Institucional está com apenas 3/20 pontos. Considere registrar participação em colegiados, bancas ou projetos.”

## RF-05 — Sugestão de Ações
O sistema deverá sugerir atividades de baixo esforço e alta pontuação.

Exemplos:

| Situação | Sugestão |
|----------|-----------|
| Formação baixa | Fazer curso curto com certificado de 20h |
| Funcional baixo | Registrar novo material didático ou metodologia |
| Produção baixa | Formalizar participação em comissão ou banca |

## RF-06 — Geração de Relatório
Gerar automaticamente:

- tabela final
- lista de evidências
- resumo por categoria
- texto pronto para SIAVI

---

# 7. Requisitos Não Funcionais

- Deve funcionar em computador e celular.
- Deve permitir backup automático.
- Deve permitir exportação em PDF.
- Deve ser simples o suficiente para ser usado em menos de 2 minutos por atividade.
- Deve permitir localizar qualquer certificado em menos de 30 segundos.

---

# 8. Estrutura Recomendada de Pastas

```text
Avaliacao_Desempenho/
│
├── 2026/
│   ├── Formacao/
│   │   ├── Cursos/
│   │   ├── Eventos/
│   │   └── Bancas/
│   ├── Funcional_Pedagogico/
│   │   ├── Materiais/
│   │   ├── Metodologias/
│   │   ├── Reunioes/
│   │   └── Orientacoes/
│   ├── Producao_Institucional/
│   │   ├── CPA/
│   │   ├── Comissoes/
│   │   ├── Bancas/
│   │   └── Projetos/
│   └── Relatorio_Final/
```

---

# 9. Padrões de Nomeação

```text
2026-03-15_Curso_IA_Educacao_8h.pdf
2026-04-10_Reuniao_CPA_Ata.pdf
2026-06-21_Banca_TCC_JoaoSilva.pdf
2026-09-03_MaterialDidatico_ComunicacoesDigitais.pdf
```

---

# 10. Modelo de Pontuação Inicial

| Categoria | Meta sugerida |
|-----------|---------------|
| Formação / Atualização | 12–15 pontos |
| Funcional–Pedagógico | 30–35 pontos |
| Produção Institucional | 18–20 pontos |

---

# 11. Sugestão de Pontuação a Implementar no Sistema

O sistema deverá possuir uma tabela interna de regras de pontuação baseada na sugestão de pontuação utilizada pela avaliação docente.

## Formação / Atualização Continuada

| Atividade | Regra |
|-----------|--------|
| Participação em palestras, seminários e eventos com certificado | 2 pontos por evento |
| Participação em congressos com certificado | 5 pontos por evento |
| Cursos de atualização e/ou estágios | 5 pontos a cada 10h |
| Exercício de atividade profissional externa correlata | 5 pontos a cada 10h |
| Curso de especialização | 15 pontos |
| Mestrado ou doutorado | 15 pontos |
| Banca de estágio supervisionado | 3 pontos |
| Banca de monografia ou TCC | 5 pontos |
| Banca de dissertação de mestrado | 10 pontos |
| Banca de tese de doutorado | 15 pontos |
| Atualização de legislações vigentes para chefias | 15 pontos |

## Funcional–Pedagógico

| Atividade | Regra |
|-----------|--------|
| Orientação de estágio supervisionado | 10 pontos por orientado |
| Orientação de TCC | 20 pontos por trabalho |
| Orientação de mestrado | 30 pontos |
| Orientação de doutorado | 35 pontos |
| Orientação de iniciação científica da UTFPR | 20 pontos |
| Orientação de bolsista de desenvolvimento científico regional, recém-doutor ou pós-doutorado | 20 pontos |
| Orientação de bolsista mestre/doutor em projeto institucional | 20 pontos |
| Coorientação de iniciação científica | 10 pontos |
| Coorientação de mestrado | 10 pontos |
| Coorientação de doutorado | 10 pontos |
| Desenvolvimento de software didático | 35 pontos |
| Autoria de livro técnico/científico | 35 pontos por livro |
| Autoria de capítulo de livro técnico/científico | 20 pontos por capítulo |
| Organização/edição de livro ou anais científicos | 35 pontos por livro |
| Tradução de livro técnico/científico | 30 pontos por livro |
| Editor-chefe de revista científica internacional | 10 pontos |
| Editor associado de revista científica nacional | 5 pontos |
| Conselho científico/editorial de revista internacional | 5 pontos |
| Conselho científico/editorial de revista nacional | 3 pontos |
| Participação em reunião de departamento | 0 a 10 pontos |
| Entrega de documentação acadêmica no prazo | 0 a 10 pontos |

## Produção Institucional

| Atividade | Regra |
|-----------|--------|
| Cargo nomeado por portaria | 10 pontos |
| Chefia de grupo de disciplinas | 10 pontos |
| Presidência de comissão por portaria | 5 pontos |
| Membro de comissão por portaria | 5 pontos |
| Membro de banca de concurso público | 5 pontos |
| Membro de banca de teste seletivo | 5 pontos |
| Participação em conselho departamental ou colegiado | 5 pontos |
| Organização de evento da UTFPR | 10 pontos por atividade |
| Responsável por laboratório | 10 pontos |
| Responsável por atividades complementares | 10 pontos |
| Responsável pela orientação de estágio | 10 pontos |
| Responsável pelo trabalho de diplomação | 10 pontos |
| Assessor de coordenação | 10 pontos |
| Participação em evento representando a instituição, apresentando trabalho ou como palestrante em evento nacional | 10 pontos por participação |

### Requisito adicional de flexibilidade

O sistema deverá permitir o cadastro de regras de pontuação que não estejam previstas nem no manual nem na tabela acima.

Campos adicionais obrigatórios para regras personalizadas:

| Campo | Descrição |
|-------|------------|
| Categoria Principal | Formação, Funcional–Pedagógico ou Produção Institucional |
| Nome da Atividade | Nome livre informado pelo usuário |
| Descrição da Regra | Explicação textual da atividade e do motivo da pontuação |
| Fórmula de Pontuação | Ex.: 3 pontos por atividade, 2 pontos por hora, valor fixo etc. |
| Pontuação Máxima Permitida | Limite opcional |
| Evidência Necessária | Certificado, portaria, ata, e-mail, PDF, link etc. |
| Observações | Campo livre |

Exemplo:

| Categoria | Atividade | Descrição | Fórmula |
|-----------|------------|------------|----------|
| Funcional–Pedagógico | Desenvolvimento de apostila própria | Produção de apostila técnica utilizada em disciplina | 10 pontos por apostila |
| Produção Institucional | Participação em grupo informal de apoio ao curso | Atividade não prevista formalmente no manual, mas relevante para a coordenação | 5 pontos por semestre |

Essas regras personalizadas deverão ficar armazenadas em uma tabela separada chamada `regras_personalizadas`, para que possam ser reutilizadas nos próximos anos.

---

# 12. Atividades de “Baixo Esforço / Alto Retorno” Identificadas

## Formação / Atualização Continuada
- Cursos rápidos com certificado
- Participação em webinars
- Participação em bancas
- Mini-cursos online

## Funcional–Pedagógico
- Registrar formalmente novos materiais didáticos
- Registrar uso de IA, Moodle, POGIL, CDIO e novas metodologias
- Guardar evidências de reuniões e entregas
- Criar apostilas, slides, listas, vídeos, softwares e tutoriais

Observação: você já produz diversos materiais didáticos, apostilas, dashboards, laboratórios, páginas Moodle, atividades CDIO e novas metodologias. O sistema deve registrar automaticamente essas evidências, porque provavelmente há perda de pontos por falta de documentação, não por falta de atividade.

## Produção Institucional
- Guardar portarias e atas de participação em:
  - CPA
  - colegiados
  - NDE
  - bancas
  - grupos de trabalho
  - projetos institucionais

No seu caso, a participação na CPA, em bancas, em materiais didáticos e em projetos institucionais parece ser a principal fonte de pontos perdidos por não haver consolidação centralizada.

---

# 12. MVP Recomendado

Implementar primeiro uma versão mínima em Google Sheets + Google Drive.

### MVP v1
- Cadastro manual
- Upload de evidência
- Soma automática
- Dashboard simples
- Alerta visual

Tempo estimado: 1 semana.

### MVP v2
- Integração com Gmail e Google Drive
- Extração automática de PDFs
- Sugestão de pontos

Tempo estimado: 2 a 4 semanas.

### MVP v3
- Sistema próprio em Streamlit
- Relatório automático
- Histórico multi-ano
- Predição de risco de perda de pontos

---

# 13. Próxima Etapa Recomendada

Próximo artefato a produzir:

- data model
- tabela de categorias e regras de pontuação
- wireframe do dashboard
- estrutura SQL
- fluxo de cadastro de atividade
- algoritmo de cálculo de pontos

