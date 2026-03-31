# ui_flow.md

## 1. Objetivo

Este documento descreve o fluxo de interface da v1 do sistema de controle da avaliação de desempenho docente, a partir do `Spec_v3.md` e do `database_schema.md`.

O objetivo é definir:
- as telas principais;
- a navegação entre elas;
- os componentes de cada tela;
- os estados esperados;
- o fluxo do usuário para cadastro, revisão, análise de risco, exportação e apoio com ChatGPT.

A interface foi pensada para uso individual, recorrente e de baixo atrito, com foco em registrar atividades rapidamente e revisar o ano de forma estratégica. A estrutura funcional do sistema e os requisitos dos módulos vêm do `Spec_v3.md`. fileciteturn8file0 O desenho dos campos e relacionamentos utilizados nas telas foi baseado no esquema de banco proposto em `database_schema.md`, incluindo as entidades `atividades`, `evidencias`, `regras_pontuacao`, `alertas`, `checkins`, `sugestoes_chatgpt` e `configuracoes_usuario`. fileciteturn8file1

---

# 2. Princípios de interface

## 2.1 Princípios gerais
- registrar rápido;
- revisar com clareza;
- enxergar risco sem navegar demais;
- separar “dado estruturado” de “sugestão do ChatGPT”;
- nunca alterar pontuação automaticamente sem confirmação do usuário.

## 2.2 Padrões visuais sugeridos
- dashboard com cards de resumo;
- tabelas filtráveis para atividades e pendências;
- formulários curtos com campos opcionais recolhidos;
- painéis laterais ou modais para ações rápidas;
- alertas e sugestões em blocos separados;
- indicadores de cor para risco:
  - verde = baixo risco;
  - amarelo = médio risco;
  - vermelho = alto risco.

---

# 3. Estrutura global da navegação

## 3.1 Navegação principal

```text
Dashboard
├── Atividades
│   ├── Nova atividade
│   ├── Detalhe da atividade
│   └── Editar atividade
├── Evidências
│   ├── Adicionar evidência
│   └── Visualizar evidências da atividade
├── Regras de pontuação
│   ├── Regras padrão
│   ├── Regras personalizadas
│   └── Nova regra personalizada
├── Alertas e pendências
├── Check-ins / Revisões
├── Relatório anual
└── ChatGPT (MVP)
    ├── Análise do ano
    ├── Análise por fator
    └── Sugestões e oportunidades
```

## 3.2 Navegação contextual

A partir do dashboard, o usuário deve conseguir:
- abrir o ano atual;
- trocar o ano ativo;
- cadastrar atividade;
- revisar pendências;
- abrir sugestões do ChatGPT;
- gerar relatório.

---

# 4. Tela 1 — Dashboard principal

## 4.1 Objetivo
Ser a tela inicial do sistema e concentrar visão anual de:
- pontuação;
- risco;
- pendências;
- alertas;
- oportunidades.

## 4.2 Componentes

### Cabeçalho
- seletor de ano;
- botão “Nova atividade”;
- botão “Gerar relatório”;
- botão “Analisar com ChatGPT”;
- botão “Registrar check-in”.

### Cards de resumo geral
- total de atividades no ano;
- total com evidência anexada;
- total de pendências;
- total de alertas em aberto;
- última revisão realizada.

### Cards por fator
Um card para cada fator:
- Formação / Atualização Continuada;
- Funcional – Pedagógico;
- Produção Institucional.

Cada card deve mostrar:
- meta do fator;
- pontuação estimada acumulada;
- pontuação confirmada;
- faltante;
- risco;
- quantidade de atividades sem evidência;
- ação rápida “Ver detalhes”.

### Bloco “Pendências prioritárias”
Lista resumida:
- atividades sem evidência;
- atividades sem regra;
- atividades com valor manual faltante;
- atividades com potencial não explorado.

### Bloco “Sugestões do ChatGPT”
Lista curta com:
- indicadores sugeridos;
- atividades que podem ser formalizadas;
- recomendações de ação.

### Bloco “Atividades recentes”
Últimas atividades cadastradas, com:
- título;
- fator;
- data;
- pontuação estimada;
- status.

## 4.3 Ações possíveis
- trocar de ano;
- abrir detalhe de fator;
- abrir atividade;
- abrir alerta;
- abrir sugestão;
- iniciar cadastro.

---

# 5. Tela 2 — Listagem de atividades

## 5.1 Objetivo
Permitir consulta, filtro, edição e navegação pelas atividades cadastradas.

## 5.2 Componentes
- filtro por ano;
- filtro por fator;
- filtro por status;
- filtro por regra;
- filtro “com pendência”;
- busca por texto;
- botão “Nova atividade”.

## 5.3 Colunas da tabela
- título;
- data;
- fator;
- subtipo;
- regra;
- pontuação estimada;
- pontuação confirmada;
- status;
- evidência;
- potencial não explorado;
- ações.

## 5.4 Ações por linha
- ver detalhe;
- editar;
- adicionar evidência;
- abrir sugestões do ChatGPT para a atividade;
- arquivar;
- marcar como revisada.

---

# 6. Tela 3 — Nova atividade

## 6.1 Objetivo
Cadastrar uma atividade potencialmente pontuável com o menor atrito possível.

## 6.2 Estrutura do formulário

### Bloco A — Identificação
- título da atividade;
- descrição breve;
- data da atividade;
- ano de referência;
- período letivo.

### Bloco B — Classificação
- fator;
- subtipo;
- regra de pontuação;
- item negociado? (sim/não).

### Bloco C — Dados de cálculo
- quantidade;
- carga horária;
- valor manual;
- pontuação estimada calculada em tempo real;
- pontuação confirmada opcional.

### Bloco D — Controle
- status;
- prioridade;
- tags;
- observações.

### Bloco E — Ações rápidas opcionais
- checkbox “Adicionar evidência agora”;
- checkbox “Pedir análise do ChatGPT após salvar”.

## 6.3 Regras de comportamento
- ao escolher a regra, o sistema deve exibir a fórmula;
- se a regra for manual, o campo `valor_manual` deve aparecer;
- se a regra for por hora, `carga_horaria` deve aparecer em destaque;
- o botão salvar deve funcionar mesmo sem evidência.

## 6.4 Saídas após salvar
- toast de sucesso;
- opção “Adicionar evidência”;
- opção “Abrir detalhe da atividade”;
- opção “Voltar ao dashboard”.

---

# 7. Tela 4 — Detalhe da atividade

## 7.1 Objetivo
Concentrar tudo o que se sabe sobre uma atividade específica.

## 7.2 Blocos da tela

### Resumo da atividade
- título;
- fator;
- subtipo;
- regra usada;
- data;
- pontuação estimada;
- pontuação confirmada;
- status;
- item negociado.

### Fórmula aplicada
- tipo de fórmula;
- base;
- unidade;
- cálculo realizado;
- teto aplicado, se houver.

### Evidências vinculadas
Lista com:
- tipo;
- nome do arquivo;
- data de anexação;
- validade;
- aprovada?;
- ações.

### Alertas relacionados
- sem evidência;
- sem regra;
- potencial não explorado;
- revisão pendente.

### Sugestões do ChatGPT para a atividade
Exemplo:
- “Esta apostila pode atender o indicador de material didático.”
- “Anexe PDF, disciplina e comprovante de uso.”
- “Avalie enquadramento no fator funcional-pedagógico.”

## 7.3 Ações possíveis
- editar atividade;
- adicionar evidência;
- alterar pontuação confirmada;
- marcar como contabilizada;
- abrir regra relacionada;
- arquivar.

---

# 8. Tela 5 — Adicionar evidência

## 8.1 Objetivo
Permitir anexar comprovação a uma atividade.

## 8.2 Campos
- atividade vinculada (pré-preenchida quando vier do detalhe);
- tipo;
- nome do arquivo;
- caminho/URL;
- descrição;
- data de anexação;
- validade status;
- data de validade;
- obrigatória?;
- aprovada?;
- observações.

## 8.3 Comportamentos
- múltiplas evidências para a mesma atividade;
- ao salvar, reprocessar pendências da atividade;
- se a atividade ficar sem pendência de evidência, atualizar status.

---

# 9. Tela 6 — Regras de pontuação

## 9.1 Objetivo
Permitir consulta das regras padrão e gestão das personalizadas.

## 9.2 Abas
- Regras padrão
- Regras personalizadas

## 9.3 Tabela de regras
Colunas:
- nome;
- categoria principal;
- subtipo;
- origem;
- tipo de fórmula;
- valor base;
- pontuação máxima;
- exige valor manual;
- ativa.

## 9.4 Ações
- visualizar detalhe;
- duplicar regra;
- editar regra personalizada;
- desativar regra personalizada;
- criar nova regra.

---

# 10. Tela 7 — Nova regra personalizada

## 10.1 Objetivo
Permitir cadastrar novas formas de pontuação que não estejam no manual nem na tabela padrão.

## 10.2 Campos
- nome;
- categoria principal;
- subtipo;
- descrição da regra;
- justificativa;
- tipo de fórmula;
- valor base;
- unidade;
- divisor;
- pontuação máxima;
- exige valor manual?;
- evidência necessária;
- origem do documento;
- observações.

## 10.3 Comportamentos
- se origem = personalizada, justificativa obrigatória;
- mostrar prévia textual da fórmula;
- permitir salvar e já usar a regra no cadastro de atividade.

---

# 11. Tela 8 — Alertas e pendências

## 11.1 Objetivo
Concentrar todos os problemas operacionais do ano.

## 11.2 Filtros
- ano;
- fator;
- tipo de alerta;
- severidade;
- resolvido / em aberto.

## 11.3 Tabela
- severidade;
- tipo;
- fator;
- atividade relacionada;
- mensagem;
- recomendação;
- data;
- resolvido.

## 11.4 Ações
- abrir atividade;
- marcar como resolvido;
- ignorar;
- enviar para análise do ChatGPT.

---

# 12. Tela 9 — Check-ins / Revisões

## 12.1 Objetivo
Registrar revisões periódicas e acompanhar evolução do risco.

## 12.2 Componentes
- lista de check-ins anteriores;
- gráfico simples de evolução;
- botão “Novo check-in”.

## 12.3 Formulário de novo check-in
- ano;
- fator específico ou geral;
- data;
- pontuação acumulada;
- status de risco;
- quantidade de atividades pendentes;
- nota.

## 12.4 Uso esperado
O usuário entra nesta tela quando quer registrar:
- revisão mensal;
- revisão bimestral;
- revisão antes de negociação;
- revisão antes de exportar relatório.

---

# 13. Tela 10 — Relatório anual

## 13.1 Objetivo
Gerar consolidação do ano para uso pessoal e apoio à avaliação.

## 13.2 Componentes
- seletor de ano;
- opção de formato:
  - Markdown;
  - PDF simples;
  - CSV.
- opção incluir:
  - atividades;
  - evidências;
  - regras personalizadas;
  - alertas;
  - sugestões do ChatGPT;
  - observações finais.

## 13.3 Pré-visualização
A tela deve exibir:
- resumo por fator;
- lista resumida das atividades;
- pendências ainda abertas;
- texto final opcional.

## 13.4 Ações
- gerar;
- baixar;
- abrir em tela;
- mandar para análise textual com ChatGPT.

---

# 14. Tela 11 — ChatGPT (MVP)

## 14.1 Objetivo
Oferecer apoio interpretativo e consultivo sem alterar automaticamente os dados.

## 14.2 Submodos

### A. Análise do ano
Pergunta central:
- “O que está faltando para eu reduzir meu risco neste ano?”

Saída esperada:
- resumo dos fatores;
- prioridades de revisão;
- atividades com potencial não explorado;
- sugestões de formalização.

### B. Análise por fator
Exemplo:
- “Como aumentar a pontuação do fator Funcional – Pedagógico?”

Saída esperada:
- indicadores possíveis;
- atividades já feitas que podem ser aproveitadas;
- evidências necessárias;
- ações recomendadas.

### C. Análise por atividade
Exemplo:
- “Esta apostila pode gerar pontuação?”

Saída esperada:
- indicador possível;
- enquadramento sugerido;
- evidências recomendadas;
- próximos passos.

### D. Redação assistida
Exemplo:
- observações finais;
- justificativas para regra personalizada;
- texto para relatório;
- resumo para negociação.

## 14.3 Componentes da tela
- seletor de ano;
- seletor de fator opcional;
- seletor de atividade opcional;
- checkbox “usar meu perfil de escrita do ChatGPT”;
- bloco explicando privacidade;
- botão “Gerar análise”.

## 14.4 Resultado da análise
Blocos sugeridos:
- resumo;
- riscos identificados;
- oportunidades;
- indicadores sugeridos;
- evidências sugeridas;
- ações recomendadas;
- texto pronto.

## 14.5 Regras de segurança
- o sistema deve mostrar claramente que a análise é sugestiva;
- nenhuma sugestão altera o banco automaticamente;
- o uso do perfil do usuário deve exigir consentimento explícito.

---

# 15. Fluxos ponta a ponta

## 15.1 Fluxo principal — registrar uma atividade e revisar depois

```text
Dashboard
→ Nova atividade
→ Salvar atividade
→ Adicionar evidência (opcional)
→ Voltar ao dashboard
→ Alertas/Pendências
→ Check-in
```

## 15.2 Fluxo de consolidação anual

```text
Dashboard
→ Revisar cards por fator
→ Abrir alertas
→ Corrigir pendências
→ Gerar relatório anual
→ Analisar com ChatGPT
→ Exportar versão final
```

## 15.3 Fluxo de oportunidade detectada pelo ChatGPT

```text
Dashboard
→ ChatGPT (MVP)
→ Análise do fator
→ Sugestão: “apostila pode gerar pontuação”
→ Abrir atividade existente ou criar nova atividade
→ Adicionar evidências
→ Revisar enquadramento
→ Atualizar pontuação
```

---

# 16. Estados vazios e mensagens

## 16.1 Dashboard vazio
Mensagem:
- “Nenhuma atividade cadastrada para este ano ainda.”

Ações:
- botão “Cadastrar primeira atividade”.

## 16.2 Sem evidências
Mensagem:
- “Esta atividade ainda não possui evidências vinculadas.”

Ação:
- botão “Adicionar evidência”.

## 16.3 Sem regras personalizadas
Mensagem:
- “Você ainda não criou regras personalizadas.”

Ação:
- botão “Nova regra personalizada”.

## 16.4 Sem sugestões do ChatGPT
Mensagem:
- “Nenhuma análise foi gerada ainda.”

Ação:
- botão “Analisar com ChatGPT”.

---

# 17. Prioridade de implementação das telas

## Prioridade 1
- Dashboard principal
- Nova atividade
- Listagem de atividades
- Detalhe da atividade
- Adicionar evidência

## Prioridade 2
- Regras de pontuação
- Nova regra personalizada
- Alertas e pendências
- Check-ins

## Prioridade 3
- Relatório anual
- ChatGPT (MVP)

---

# 18. Mapeamento entre telas e tabelas do banco

| Tela | Tabelas principais |
|------|--------------------|
| Dashboard | `anos_avaliacao`, `atividades`, `alertas`, `checkins`, `sugestoes_chatgpt` |
| Listagem de atividades | `atividades`, `regras_pontuacao` |
| Nova atividade | `atividades`, `regras_pontuacao`, `anos_avaliacao` |
| Detalhe da atividade | `atividades`, `evidencias`, `alertas`, `sugestoes_chatgpt` |
| Adicionar evidência | `evidencias`, `atividades` |
| Regras | `regras_pontuacao` |
| Check-ins | `checkins`, `anos_avaliacao` |
| Alertas | `alertas`, `atividades` |
| Relatório anual | `atividades`, `evidencias`, `alertas`, `regras_pontuacao`, `sugestoes_chatgpt` |
| ChatGPT (MVP) | `atividades`, `alertas`, `sugestoes_chatgpt`, `configuracoes_usuario` |

---

# 19. Próxima etapa natural

Com este fluxo de interface definido, a próxima saída natural é:

- `implementation_plan.md`

Ele deverá transformar:
- `Spec_v3.md`,
- `database_schema.md`,
- `ui_flow.md`

em uma sequência de implementação técnica para o Codex.
