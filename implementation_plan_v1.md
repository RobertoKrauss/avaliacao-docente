# implementation_plan.md

## 1. Objetivo

Este documento transforma o `Spec_v3.md`, o `database_schema.md` e o `ui_flow.md` em um plano de implementação sequencial, pronto para ser executado no Codex.

O foco da v1 é entregar um sistema funcional, local, baseado em SQLite e interface web moderna, cobrindo:
- cadastro de atividades;
- vínculo de evidências;
- regras de pontuação padrão e personalizadas;
- cálculo de pontuação;
- dashboard anual com risco;
- alertas e pendências;
- relatório anual;
- módulo MVP de apoio com ChatGPT.

A definição funcional do produto, módulos, regras de negócio, risco, sugestões e uso opcional do ChatGPT vem do `Spec_v3.md`. fileciteturn9file0 O desenho de interface, telas, fluxos ponta a ponta, prioridades e estados da UI vem do `ui_flow.md`. fileciteturn9file1 A estrutura técnica das tabelas, relacionamentos, constraints e índices vem do `database_schema.md`. fileciteturn9file2

---

## 2. Diretriz visual obrigatória

A interface da v1 deve ter aparência moderna, limpa e profissional.

### Requisitos visuais mínimos
- dashboard visual baseado em cards;
- boa hierarquia tipográfica;
- espaçamento consistente;
- visual refinado em formulários e tabelas;
- indicadores de risco bem destacados;
- navegação simples e clara;
- experiência agradável em desktop e tablet;
- evitar aparência de CRUD cru ou sistema administrativo antigo.

### Consequência prática para implementação
A etapa de frontend não deve se limitar a “funcionar”. Ela deve:
- aplicar consistência visual entre as telas;
- usar componentes reutilizáveis;
- manter padrão de cores, títulos, bordas e estados;
- priorizar clareza e leitura frequente ao longo do ano.

---

## 3. Estratégia geral

### 3.1 Princípio de implementação
A implementação deve seguir esta ordem:

1. base de dados;
2. camada de acesso aos dados;
3. motor de cálculo e regras;
4. telas principais;
5. dashboard e risco;
6. alertas e revisões;
7. exportação do relatório;
8. módulo MVP de ChatGPT;
9. refinamento visual final.

### 3.2 Abordagem recomendada
Como a v1 é individual e de baixo atrito, a stack recomendada é:
- Python
- SQLite
- Streamlit

### 3.3 Resultado esperado da v1
Ao final da v1, o usuário deve conseguir:
- abrir o sistema;
- criar ou selecionar um ano;
- cadastrar atividades;
- anexar evidências;
- aplicar regras de pontuação;
- visualizar risco e faltantes;
- revisar pendências;
- gerar relatório;
- obter sugestões opcionais do ChatGPT.

---

## 4. Fora do escopo desta implementação

Não implementar nesta etapa:
- login multiusuário;
- SIAVI;
- OCR;
- integração automática com Google Drive;
- importação automática de e-mails;
- sincronização com calendário;
- app mobile nativo;
- automação institucional de submissão;
- qualquer alteração automática de pontuação baseada em IA.

---

## 5. Estrutura sugerida do projeto

```text
app/
├── main.py
├── db/
│   ├── schema.sql
│   ├── seed.py
│   ├── connection.py
│   └── repositories/
│       ├── anos_repository.py
│       ├── atividades_repository.py
│       ├── evidencias_repository.py
│       ├── regras_repository.py
│       ├── alertas_repository.py
│       ├── checkins_repository.py
│       └── sugestoes_repository.py
├── services/
│   ├── calculo_pontuacao.py
│   ├── calculo_risco.py
│   ├── alertas_service.py
│   ├── relatorio_service.py
│   └── chatgpt_service.py
├── ui/
│   ├── dashboard.py
│   ├── atividades.py
│   ├── atividade_form.py
│   ├── atividade_detail.py
│   ├── evidencias.py
│   ├── regras.py
│   ├── regra_form.py
│   ├── alertas.py
│   ├── checkins.py
│   ├── relatorio.py
│   ├── chatgpt.py
│   └── theme.py
├── models/
│   ├── enums.py
│   └── dto.py
├── utils/
│   ├── formatters.py
│   ├── validators.py
│   └── dates.py
└── exports/
```

---

## 6. Fases de implementação

## Fase 1 — Base de dados e bootstrap

### 6.1 Objetivo
Criar o banco SQLite e garantir que o sistema inicie com estrutura pronta.

### 6.2 Entregas
- arquivo `schema.sql`;
- script de criação do banco;
- script de seed inicial;
- registro automático do ano atual;
- regras padrão inseridas;
- configurações iniciais inseridas.

### 6.3 Itens a implementar

#### 6.3.1 Criar tabelas
Implementar conforme `database_schema.md`:
- `anos_avaliacao`
- `regras_pontuacao`
- `atividades`
- `evidencias`
- `checkins`
- `alertas`
- `sugestoes_chatgpt`
- `configuracoes_usuario`

#### 6.3.2 Criar constraints e índices
Replicar:
- checks de categoria, origem e fórmula;
- foreign keys;
- índices por ano, fator, status e tipo.

#### 6.3.3 Seed inicial
Inserir:
- ano atual;
- metas padrão 15/35/20;
- regras padrão do spec;
- `usar_perfil_chatgpt = false`.

### 6.4 Critérios de aceite
- banco é criado sem erro;
- todas as tabelas existem;
- ano atual é criado automaticamente;
- regras padrão são carregadas;
- configuração inicial é persistida.

---

## Fase 2 — Camada de acesso aos dados

### 7.1 Objetivo
Criar funções e repositórios para leitura e escrita no banco.

### 7.2 Entregas
- conexão centralizada com SQLite;
- CRUD de anos;
- CRUD de atividades;
- CRUD de evidências;
- CRUD de regras personalizadas;
- CRUD de alertas;
- CRUD de check-ins;
- leitura e gravação de sugestões do ChatGPT.

### 7.3 Itens a implementar

#### 7.3.1 Repositório de anos
Funções:
- obter ano atual;
- listar anos;
- criar ano;
- atualizar metas;
- atualizar `ultima_revisao`.

#### 7.3.2 Repositório de atividades
Funções:
- listar por ano;
- filtrar por fator, status e regra;
- obter por id;
- criar;
- editar;
- exclusão lógica;
- atualizar pontuação e status.

#### 7.3.3 Repositório de evidências
Funções:
- listar por atividade;
- adicionar;
- editar;
- exclusão lógica.

#### 7.3.4 Repositório de regras
Funções:
- listar padrão;
- listar personalizadas;
- criar personalizada;
- editar personalizada;
- desativar personalizada.

#### 7.3.5 Repositório de alertas, check-ins e sugestões
Funções:
- listar por ano;
- criar;
- atualizar resolução;
- registrar análise.

### 7.4 Critérios de aceite
- todas as funções CRUD operam corretamente;
- atividades podem ser recuperadas por ano e fator;
- evidências se vinculam corretamente;
- regras personalizadas podem ser ativadas/desativadas;
- sugestões do ChatGPT podem ser persistidas.

---

## Fase 3 — Motor de cálculo de pontuação

### 8.1 Objetivo
Implementar a lógica de cálculo prevista no spec.

### 8.2 Entregas
- serviço de cálculo de pontuação;
- interpretação de fórmulas;
- preservação de pontuação original;
- suporte a valor manual;
- respeito ao teto da regra.

### 8.3 Regras de cálculo
Implementar:
- `fixo`
- `por_unidade`
- `por_hora`
- `intervalo`
- `manual`

### 8.4 Regras complementares
- `pontuacao_estimada` é calculada automaticamente;
- `pontuacao_confirmada` pode ser diferente;
- `pontuacao_original` preserva o primeiro cálculo;
- regras manuais exigem `valor_manual`.

### 8.5 Critérios de aceite
- atividades com regra fixa calculam corretamente;
- atividades por unidade e por hora calculam corretamente;
- regras manuais exigem preenchimento;
- pontuação não fica negativa;
- teto de regra é respeitado.

---

## Fase 4 — Motor de risco, pendências e alertas

### 9.1 Objetivo
Transformar o banco de dados em visão gerencial útil.

### 9.2 Entregas
- cálculo de risco por fator;
- detecção automática de pendências;
- geração automática de alertas;
- atualização de alertas quando dados mudarem.

### 9.3 Lógica mínima de risco
Para cada fator:
- baixo risco: >= 80% da meta;
- médio risco: 50% a 79%;
- alto risco: < 50%.

### 9.4 Pendências mínimas
- atividade sem evidência;
- atividade sem regra;
- atividade sem fator;
- valor manual faltante;
- atividade com potencial não explorado.

### 9.5 Tipos de alertas
- `atividade_sem_evidencia`
- `atividade_sem_regra`
- `atividade_sem_fator`
- `valor_manual_faltante`
- `risco_alto`
- `revisao_atrasada`
- `pontuacao_baixa`
- `potencial_nao_explorado`

### 9.6 Critérios de aceite
- risco por fator é calculado corretamente;
- alertas aparecem automaticamente;
- ao corrigir pendência, alerta pode ser resolvido;
- dashboard consegue consumir esses dados.

---

## Fase 5 — Tema visual e componentes base

### 10.1 Objetivo
Criar a base visual moderna antes de espalhar componentes soltos pelas telas.

### 10.2 Entregas
- paleta de cores;
- estilos globais;
- componentes visuais reutilizáveis;
- padrão de cards;
- padrão de tabelas;
- padrão de formulários;
- padrão de alertas e badges.

### 10.3 Itens a implementar
- arquivo `theme.py` ou equivalente com tokens visuais;
- helpers para:
  - card de resumo;
  - badge de risco;
  - tabela estilizada;
  - cabeçalho de página;
  - caixas de alerta;
- convenção visual para:
  - verde, amarelo, vermelho;
  - pendência;
  - atividade contabilizada;
  - sugestão do ChatGPT.

### 10.4 Critérios de aceite
- a UI deixa de ter aparência de protótipo cru;
- cards, tabelas e formulários seguem o mesmo padrão;
- o dashboard e as telas principais já herdam uma aparência moderna consistente.

---

## Fase 6 — Tela Dashboard

### 11.1 Objetivo
Entregar a tela principal do sistema.

### 11.2 Entregas
- seletor de ano;
- cards de resumo geral;
- cards por fator;
- bloco de pendências prioritárias;
- bloco de sugestões do ChatGPT;
- bloco de atividades recentes.

### 11.3 Componentes obrigatórios
- botão “Nova atividade”;
- botão “Gerar relatório”;
- botão “Analisar com ChatGPT”;
- botão “Registrar check-in”.

### 11.4 Critérios de aceite
- dashboard abre com ano atual;
- cards mostram metas, acumulado, faltante e risco;
- pendências e alertas resumidos aparecem;
- atividades recentes aparecem em ordem cronológica inversa;
- visual segue a diretriz moderna definida na Fase 5.

---

## Fase 7 — Telas de atividades

### 12.1 Objetivo
Permitir cadastro, edição, consulta e detalhe das atividades.

### 12.2 Entregas
- listagem de atividades;
- formulário “Nova atividade”;
- tela de detalhe;
- edição de atividade;
- ações rápidas por linha.

### 12.3 Requisitos obrigatórios
- filtros por ano, fator, status e pendência;
- cálculo automático ao escolher regra;
- suporte a item negociado;
- suporte a pontuação confirmada manual;
- detalhe com fórmulas, evidências, alertas e sugestões.

### 12.4 Critérios de aceite
- usuário consegue criar atividade completa;
- atividade aparece na listagem e no dashboard;
- detalhe mostra cálculo e relacionamentos;
- edição recalcula alerta e pontuação quando necessário;
- formulário e tabela mantêm aparência refinada.

---

## Fase 8 — Telas de evidências

### 13.1 Objetivo
Permitir anexar comprovação e atualizar o estado das atividades.

### 13.2 Entregas
- formulário de evidência;
- listagem de evidências no detalhe da atividade;
- vínculo múltiplo por atividade;
- atualização automática de pendência.

### 13.3 Critérios de aceite
- usuário consegue cadastrar várias evidências para a mesma atividade;
- evidência aparece vinculada corretamente;
- atividade sem pendência de evidência atualiza seu status quando aplicável;
- listagem de evidências é clara e visualmente consistente.

---

## Fase 9 — Telas de regras de pontuação

### 14.1 Objetivo
Permitir consultar regras padrão e criar regras personalizadas.

### 14.2 Entregas
- tela de regras padrão;
- tela de regras personalizadas;
- formulário de nova regra personalizada;
- ações de editar, duplicar, desativar.

### 14.3 Regras obrigatórias
- regra personalizada exige justificativa;
- prévia textual da fórmula;
- regra salva pode ser usada imediatamente.

### 14.4 Critérios de aceite
- regras padrão ficam somente para consulta;
- regras personalizadas podem ser criadas e reutilizadas;
- regra desativada deixa de aparecer no formulário de atividade.

---

## Fase 10 — Tela de alertas e pendências

### 15.1 Objetivo
Concentrar o trabalho de saneamento do ano.

### 15.2 Entregas
- tabela de alertas;
- filtros por ano, fator, tipo e severidade;
- ação de abrir atividade;
- ação de marcar alerta como resolvido.

### 15.3 Critérios de aceite
- todos os alertas do ano aparecem nesta tela;
- filtros funcionam corretamente;
- resolução fica persistida;
- severidade e risco são fáceis de interpretar visualmente.

---

## Fase 11 — Tela de check-ins

### 16.1 Objetivo
Registrar revisões periódicas e apoiar o acompanhamento histórico.

### 16.2 Entregas
- tela de listagem de check-ins;
- formulário de novo check-in;
- exibição simples de evolução.

### 16.3 Critérios de aceite
- usuário consegue registrar revisão geral ou por fator;
- lista mostra histórico em ordem decrescente;
- último check-in pode atualizar `ultima_revisao` do ano.

---

## Fase 12 — Relatório anual

### 17.1 Objetivo
Gerar consolidação exportável do ano.

### 17.2 Entregas
- tela de relatório anual;
- prévia do relatório;
- exportação em Markdown;
- exportação em CSV;
- PDF simples opcional na v1, se o fluxo estiver estável.

### 17.3 Conteúdo mínimo
- resumo por fator;
- atividades do ano;
- pontuação estimada e confirmada;
- pendências abertas;
- regras personalizadas usadas;
- observações finais.

### 17.4 Critérios de aceite
- usuário consegue gerar relatório por ano;
- conteúdo corresponde aos dados persistidos;
- exportações são geradas sem erro;
- layout da prévia mantém boa legibilidade.

---

## Fase 13 — Módulo ChatGPT (MVP)

### 18.1 Objetivo
Oferecer apoio consultivo sem alterar os registros automaticamente.

### 18.2 Entregas
- tela ChatGPT (MVP);
- modos de análise:
  - análise do ano;
  - análise por fator;
  - análise por atividade;
  - redação assistida;
- persistência das sugestões em `sugestoes_chatgpt`;
- controle “usar meu perfil de escrita do ChatGPT”;
- explicação de privacidade.

### 18.3 Regras obrigatórias
- somente dados explicitamente selecionados pelo usuário podem ser enviados;
- o uso do perfil deve depender de consentimento explícito;
- nenhuma sugestão altera o banco automaticamente;
- sugestões devem poder virar ação manual do usuário.

### 18.4 Casos de uso mínimos
- resumir o ano;
- destacar fatores de risco;
- sugerir indicadores e oportunidades;
- sugerir evidências necessárias;
- redigir observações e justificativas.

### 18.5 Critérios de aceite
- análise pode ser gerada por ano, fator ou atividade;
- sugestões podem ser visualizadas e salvas;
- usuário consegue reaproveitar o texto no relatório ou na revisão;
- sistema sinaliza claramente que se trata de sugestão, não automação.

---

## Fase 14 — Polimento visual e consistência final

### 19.1 Objetivo
Refinar a experiência para que a interface fique efetivamente moderna e consistente no uso real.

### 19.2 Entregas
- revisão visual de todas as telas;
- alinhamento de espaçamentos;
- ajuste de tipografia;
- refinamento de botões, badges, cards e tabelas;
- melhoria de estados vazios;
- revisão de microtextos.

### 19.3 Checklist de refinamento
- cabeçalhos consistentes;
- margens e paddings equilibrados;
- botões primários e secundários claros;
- cards com leitura rápida;
- formulários visualmente leves;
- tabelas sem poluição visual;
- blocos do ChatGPT separados do dado estruturado;
- alertas e riscos com forte contraste visual.

### 19.4 Critérios de aceite
- a interface parece produto e não só ferramenta interna;
- navegação está fluida;
- o uso frequente é agradável;
- as telas mantêm coerência visual.

---

## 7. Ordem sugerida de execução no Codex

### Sprint 1
- Fase 1
- Fase 2
- Fase 3
- Fase 4

### Sprint 2
- Fase 5
- Fase 6
- Fase 7
- Fase 8

### Sprint 3
- Fase 9
- Fase 10
- Fase 11
- Fase 12

### Sprint 4
- Fase 13
- Fase 14
- ajustes finais
- estabilização

---

## 8. Critérios globais de pronto

A implementação estará pronta para uso inicial quando:
1. o banco inicial for criado corretamente;
2. as regras padrão estiverem carregadas;
3. o usuário conseguir cadastrar atividades e evidências;
4. o sistema calcular pontuação e risco;
5. o dashboard mostrar faltantes, alertas e pendências;
6. o usuário conseguir revisar o ano e gerar relatório;
7. o módulo ChatGPT gerar sugestões sem alterar automaticamente os dados;
8. a interface apresentar padrão visual moderno, consistente e agradável.

---

## 9. Prompt-base sugerido para usar no Codex

```text
Implemente a v1 do sistema de controle da avaliação de desempenho docente usando Python + SQLite + Streamlit.

Use como fonte obrigatória:
- Spec_v3.md
- database_schema.md
- ui_flow.md
- implementation_plan.md

Siga a ordem das fases definida no implementation_plan.md.

Requisitos críticos:
- não implementar nada fora do escopo;
- não automatizar mudança de pontuação com IA;
- usar SQLite como banco local;
- criar o dashboard, cadastro de atividades, evidências, regras personalizadas, alertas, check-ins, relatório anual e módulo MVP de ChatGPT;
- persistir sugestões do ChatGPT no banco;
- exigir consentimento explícito para uso do perfil de escrita do usuário;
- garantir interface moderna, limpa e profissional.
```

---

## 10. Próxima etapa natural

Depois deste plano, o ideal é pedir ao Codex a implementação por etapas, começando por:

1. Fase 1 — Base de dados e bootstrap
2. Fase 2 — Camada de acesso aos dados
3. Fase 3 — Motor de cálculo de pontuação
