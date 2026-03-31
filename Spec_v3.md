# Spec.md — Especificação Funcional e Técnica do Sistema de Controle para Avaliação de Desempenho Docente

## 1. Objetivo da especificação

Esta especificação transforma o PRD em um documento executável de produto, descrevendo com maior precisão:

- o que o sistema deve fazer;
- quais dados precisa armazenar;
- como o usuário irá interagir com o sistema;
- quais regras precisam ser suportadas;
- quais limites de escopo devem ser respeitados na primeira implementação.

O sistema é voltado ao controle contínuo da avaliação de desempenho docente da UTFPR, com foco nos fatores:

- Formação / Atualização Continuada
- Funcional – Pedagógico
- Produção Institucional

---

## 2. Visão do sistema

O sistema será um ambiente de registro contínuo de atividades e evidências, com acompanhamento de pontuação por fator e geração de consolidação anual.

Ele deverá funcionar como seis módulos integrados:

1. **Registro de atividades**
2. **Gestão de evidências**
3. **Motor de classificação e pontuação**
4. **Painel anual e acompanhamento de risco**
5. **Alertas, recomendações e sugestões de ação**
6. **Relatório anual e apoio consultivo com ChatGPT (MVP)**

A lógica principal é:

- registrar a atividade quando ela acontece;
- vincular a evidência correspondente;
- associar a atividade a uma regra de pontuação;
- acompanhar o acumulado anual por fator;
- identificar pendências e lacunas;
- preparar o material para o fechamento do ciclo.

---

## 3. Escopo da primeira versão

### 3.1 Incluído
- cadastro manual de atividades;
- cadastro e vínculo de evidências;
- classificação por fator;
- uso de regras de pontuação pré-cadastradas;
- cadastro de regras personalizadas;
- cálculo de pontuação estimada;
- cálculo de risco por fator;
- alertas automáticos de itens faltantes;
- recomendações de revisão periódica;
- sugestões de ações para redução de lacunas;
- acompanhamento por ano;
- dashboard com acumulado, faltante e risco;
- listagem de pendências;
- geração de relatório anual em Markdown ou PDF simples;
- conexão MVP com ChatGPT para apoio interpretativo e consultivo sobre os dados já registrados.

### 3.2 Não incluído nesta fase
- integração direta com SIAVI;
- autenticação multiusuário complexa;
- workflow formal de aprovação por chefia;
- importação automática de e-mails;
- OCR de certificados;
- sincronização automática com Google Drive;
- app mobile nativo;
- homologação automática da pontuação;
- envio automático de dados institucionais para sistemas externos sem revisão do usuário.

---

## 4. Perfis de uso

### 4.1 Usuário principal
**Docente avaliado**

Responsável por:
- registrar atividades;
- anexar evidências;
- acompanhar pontuação;
- cadastrar regras personalizadas;
- gerar o relatório anual.

### 4.2 Usuário secundário futuro
**Chefia ou avaliador**
- fora do escopo operacional da v1;
- eventualmente poderá consumir relatórios exportados.

---

## 5. Estrutura funcional do produto

## 5.1 Módulo 1 — Registro de atividades

Permite o lançamento de qualquer atividade potencialmente pontuável.

### Campos obrigatórios
- título da atividade;
- data da atividade;
- ano de referência;
- fator principal;
- subtipo;
- regra de pontuação associada;
- descrição breve;
- status da atividade.

### Campos opcionais
- carga horária;
- quantidade;
- período letivo;
- observações;
- item negociado? (sim/não);
- pontuação confirmada manualmente;
- tags livres.

### Status possíveis
- rascunho;
- registrada;
- com evidência pendente;
- com evidência anexada;
- revisada;
- contabilizada;
- arquivada.

---

## 5.2 Módulo 2 — Gestão de evidências

Cada atividade poderá ter zero, uma ou várias evidências associadas.

### Tipos de evidência aceitos
- certificado;
- portaria;
- ata;
- e-mail;
- declaração;
- PDF;
- imagem;
- link externo;
- arquivo de material didático;
- print;
- outro.

### Campos da evidência
- atividade vinculada;
- tipo de evidência;
- nome do arquivo;
- caminho ou link;
- descrição;
- data de anexação;
- validade da evidência;
- observações.

### Regras
- uma atividade pode existir sem evidência;
- atividades sem evidência devem aparecer como pendência;
- o sistema não deve bloquear o cadastro da atividade por falta de evidência;
- o sistema deve permitir múltiplas evidências para a mesma atividade.

---

## 5.3 Módulo 3 — Regras de pontuação

O sistema deve suportar dois grupos de regras:

1. **regras padrão**
2. **regras personalizadas**

### 5.3.1 Regras padrão
São as regras conhecidas a partir do manual e da tabela adicional informada pelo usuário.

### 5.3.2 Regras personalizadas
Servem para registrar descrições de pontuação não previstas formalmente nas listas conhecidas.

O sistema deve permitir ao usuário criar uma nova regra com os campos:

- categoria principal;
- nome da atividade;
- descrição da regra;
- fórmula de pontuação;
- pontuação base;
- unidade de cálculo;
- pontuação máxima;
- evidência exigida;
- origem da regra;
- observações.

### 5.3.3 Tipos de fórmula de pontuação
O sistema deve suportar ao menos:

- valor fixo;
- valor por unidade;
- valor por hora;
- intervalo;
- valor manual.

### Exemplos
- 5 pontos por evento;
- 5 pontos a cada 10 horas;
- 20 pontos por trabalho;
- 0 a 10 pontos definidos manualmente;
- 10 pontos por participação.

---

## 5.4 Módulo 4 — Dashboard anual

O painel principal deve mostrar a situação do ano selecionado.

### Indicadores por fator
Para cada fator, exibir:
- teto do fator;
- pontuação estimada acumulada;
- pontuação confirmada;
- quantidade de atividades registradas;
- quantidade de atividades sem evidência;
- quanto falta para atingir o teto;
- status visual.

### Status visual sugerido
- verde: fator já atingido ou ultrapassado;
- amarelo: fator em andamento;
- vermelho: fator muito abaixo do alvo.

### Blocos do dashboard
- resumo geral do ano;
- cards por fator;
- tabela de pendências;
- atividades recentes;
- regras personalizadas criadas;
- alertas de inconsistência.

---

## 5.5 Módulo 5 — Alertas, recomendações e sugestões de ação

Este módulo complementa o dashboard sem alterar a lógica central já definida. Ele reutiliza os dados de atividades, evidências e pontuação para orientar o usuário ao longo do ciclo.

### 5.5.1 Alertas automáticos de itens faltantes
O sistema deve gerar alertas automáticos para situações como:
- atividade sem evidência;
- atividade sem regra associada;
- atividade sem fator definido;
- atividade com valor manual não preenchido;
- fator com baixa pontuação acumulada em relação ao teto;
- ausência de revisão recente no ano corrente.

### 5.5.2 Painel de acompanhamento de risco
Além do total por fator, o sistema deve exibir um indicador de risco para cada fator.

#### Faixas sugeridas
- **baixo risco**: fator com 80% ou mais do teto desejado;
- **médio risco**: fator entre 50% e 79% do teto desejado;
- **alto risco**: fator abaixo de 50% do teto desejado.

O risco deverá ser calculado com base na pontuação estimada acumulada, podendo futuramente considerar também pendências de evidência.

### 5.5.3 Recomendação de revisão
O sistema deverá exibir recomendações de revisão, por exemplo:
- “há mais de 30 dias sem revisão do ano corrente”;
- “existem atividades com evidência pendente”;
- “há fatores com risco alto que merecem revisão prioritária”;
- “há atividades registradas sem regra de pontuação”.

### 5.5.4 Sugestão de ações
O sistema deverá apresentar sugestões de ação baseadas nas lacunas detectadas, sem alterar automaticamente qualquer dado.

Exemplos:
- se Formação estiver baixa, sugerir registrar cursos, eventos, bancas ou capacitações recentes;
- se Funcional–Pedagógico estiver baixo, sugerir revisar materiais didáticos, orientações, metodologias aplicadas e reuniões registráveis;
- se Produção Institucional estiver baixa, sugerir revisar comissões, bancas, colegiados, eventos institucionais e encargos formais.

Essas sugestões devem ser tratadas como apoio de planejamento, e não como decisão automática de pontuação.

---

## 5.6 Módulo 6 — Relatório anual e apoio consultivo com ChatGPT (MVP)

Deve consolidar os dados do ano selecionado.

### Conteúdo mínimo
- identificação do ano;
- resumo por fator;
- lista de atividades por fator;
- pontuação estimada total;
- pontuação confirmada total;
- atividades sem evidência;
- atividades com regra personalizada;
- observações finais.

### Formatos desejáveis
- Markdown;
- PDF simples;
- CSV exportável.

### Apoio consultivo com ChatGPT (MVP)
Na primeira versão, a conexão com ChatGPT deverá ser tratada como um recurso auxiliar e opcional, sem interferir no registro principal dos dados.

Objetivos do MVP de conexão com ChatGPT:
- resumir o ano com base nas atividades já registradas;
- destacar fatores com maior risco;
- sugerir revisão de pendências;
- ajudar a redigir textos de consolidação, observações e preparação para negociação;
- sugerir como organizar as evidências já cadastradas;
- sugerir possíveis indicadores, evidências e atividades que poderiam ser formalizados para reduzir o risco e aumentar a pontuação em cada fator;
- identificar atividades realizadas pelo usuário, mas ainda não formalizadas para pontuação;
- opcionalmente adaptar a linguagem, o estilo de escrita e as sugestões ao perfil do usuário já observado em conversas anteriores no ChatGPT.

Exemplos de inferência desejada:
- se o histórico do usuário indicar produção frequente de apostilas, materiais didáticos, páginas Moodle, questionários, dashboards, relatórios, participação em CPA, orientação de alunos ou projetos, o sistema deverá sugerir:
  - quais indicadores da avaliação podem ser atendidos por essas atividades;
  - quais evidências precisam ser guardadas;
  - quais ações adicionais poderiam transformar essas atividades em pontuação formal;
- por exemplo, se o usuário escreveu uma apostila, o sistema pode sugerir:
  - cadastrar a apostila como material didático;
  - validar a atividade junto ao fator funcional-pedagógico ou produção institucional;
  - anexar PDF, capa, data, disciplina e comprovante de uso;
  - solicitar formalização institucional, registro, publicação ou declaração, caso isso aumente a pontuação;
- se o usuário desenvolveu um sistema, dashboard, laboratório ou software, o sistema pode sugerir enquadramento como produção técnica, inovação institucional ou material pedagógico, conforme as regras cadastradas.

### Modo opcional de personalização pelo perfil do usuário
O sistema deverá possuir uma opção explícita do tipo “usar meu perfil de escrita do ChatGPT”.

Quando habilitada pelo usuário:
- o contexto enviado ao ChatGPT poderá incluir preferências de escrita e padrões de comunicação observados em interações anteriores;
- as sugestões deverão respeitar o estilo do usuário, por exemplo:
  - linguagem mais técnica ou mais institucional;
  - tom mais formal, diplomático ou direto;
  - preferência por justificativas detalhadas, listas, tabelas ou texto corrido;
  - foco em aspectos que o usuário normalmente valoriza, como pontuação, evidências, riscos ou negociação;
- o sistema poderá gerar recomendações mais alinhadas ao modo como o usuário normalmente organiza relatórios e argumentações;
- o sistema poderá inferir, a partir do histórico do usuário, quais atividades já executadas têm potencial de gerar pontuação mas ainda não foram registradas;
- o sistema poderá sugerir indicadores alternativos ou complementares para atingir a pontuação necessária em cada fator.

Exemplos de uso:
- sugerir observações finais no estilo normalmente utilizado pelo usuário;
- redigir justificativas para regras personalizadas usando um tom compatível com o histórico do usuário;
- priorizar recomendações coerentes com o padrão de escrita e análise já utilizado pelo usuário no ChatGPT.

Essa personalização deve ser:
- opcional e desabilitada por padrão;
- claramente informada ao usuário antes do envio do contexto;
- usada apenas para gerar texto e sugestões;
- incapaz de alterar automaticamente pontuações, regras ou classificações.

Limites do MVP:
- não altera pontuação automaticamente;
- não cria atividades automaticamente sem confirmação do usuário;
- não substitui a revisão humana;
- não substitui a negociação formal no SIAVI.

A conexão com ChatGPT deve consumir apenas os dados estruturados do sistema exportados pelo usuário ou disponibilizados em contexto controlado.

---

## 6. Regras de negócio

## 6.1 Estrutura dos fatores

### Formação / Atualização Continuada
Máximo desejado de acompanhamento: **15 pontos**

### Funcional – Pedagógico
Máximo desejado de acompanhamento: **35 pontos**

### Produção Institucional
Máximo desejado de acompanhamento: **20 pontos**

---

## 6.2 Separação entre pontuação estimada e confirmada

O sistema deve manter duas medidas diferentes:

### Pontuação estimada
- calculada automaticamente com base na regra associada;
- usada para planejamento e acompanhamento.

### Pontuação confirmada
- ajustada manualmente pelo usuário quando necessário;
- usada para refletir o que de fato foi aceito ou negociado.

---

## 6.3 Atividade não é igual a item homologado

Uma atividade registrada:
- pode não virar item pontuado;
- pode ser ajustada na negociação;
- pode ter pontuação reduzida;
- pode ser usada apenas como memória/evidência.

Por isso, o sistema deve permitir:
- registrar tudo;
- classificar depois;
- revisar depois;
- manter histórico mesmo se não pontuado.

---

## 6.4 Regras personalizadas obrigatoriamente descritivas

Toda regra fora das listas padrão deve exigir uma justificativa textual.

Campos mínimos obrigatórios:
- nome;
- descrição;
- categoria;
- fórmula;
- justificativa;
- evidência esperada.

---

## 6.5 Pendências operacionais

Devem ser tratadas como pendência:
- atividade sem evidência;
- atividade sem regra de pontuação;
- atividade sem fator definido;
- atividade com valor manual ainda não preenchido;
- atividade arquivada como “não pontuada”.

## 6.6 Cálculo de pontuação

O sistema deve calcular a pontuação estimada a partir da fórmula da regra associada e dos dados informados na atividade.

Regras mínimas de cálculo:
- **fixo**: usa diretamente o valor base da regra;
- **por_unidade**: multiplica quantidade pelo valor base;
- **por_hora**: divide carga horária pelo divisor da regra e multiplica pelo valor base;
- **intervalo/manual**: exige preenchimento manual pelo usuário;
- **com teto**: respeita pontuação máxima definida na regra, quando existir.

A pontuação confirmada deve poder sobrescrever a estimada sem apagar o histórico da estimativa original.

## 6.7 Cálculo de risco e recomendação de revisão

O sistema deve calcular risco por fator e gerar recomendação de revisão com base em:
- percentual do teto já alcançado;
- quantidade de atividades pendentes;
- existência de atividades sem evidência;
- tempo desde a última revisão/check-in.

Esse cálculo deve ser interpretativo e não deve modificar registros automaticamente.

---

## 7. Modelo de dados

## 7.1 Entidade `atividades`

| Campo | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| id | inteiro | sim | identificador único |
| titulo | texto | sim | nome curto da atividade |
| descricao | texto | não | descrição livre |
| data_atividade | data | sim | data principal |
| ano_referencia | inteiro | sim | ano da avaliação |
| periodo_letivo | texto | não | semestre/período |
| fator | texto | sim | formação, funcional ou produção |
| subtipo | texto | não | subtipo da atividade |
| regra_id | inteiro | não | regra associada |
| quantidade | real | não | número de unidades |
| carga_horaria | real | não | horas, quando aplicável |
| pontuacao_estimada | real | não | valor calculado |
| pontuacao_confirmada | real | não | valor ajustado manualmente |
| item_negociado | booleano | não | indica se é item negociado |
| status | texto | sim | status da atividade |
| observacoes | texto | não | anotações livres |
| created_at | datetime | sim | criação |
| updated_at | datetime | sim | última alteração |

---

## 7.2 Entidade `evidencias`

| Campo | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| id | inteiro | sim | identificador |
| atividade_id | inteiro | sim | vínculo com atividade |
| tipo | texto | sim | certificado, portaria etc. |
| nome_arquivo | texto | não | nome amigável |
| caminho_arquivo | texto | não | path local ou URL |
| descricao | texto | não | explicação |
| data_anexacao | datetime | sim | data de inclusão |
| validade_status | texto | não | válida, pendente, revisar |
| observacoes | texto | não | anotações |

---

## 7.3 Entidade `regras_pontuacao`

| Campo | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| id | inteiro | sim | identificador |
| nome | texto | sim | nome da regra |
| categoria_principal | texto | sim | fator |
| subtipo | texto | não | subtipo interno |
| origem | texto | sim | padrão ou personalizada |
| descricao_regra | texto | sim | explicação textual |
| tipo_formula | texto | sim | fixo, por_unidade, por_hora, intervalo, manual |
| valor_base | real | não | valor base |
| unidade | texto | não | evento, hora, trabalho, orientado etc. |
| divisor_unidade | real | não | ex.: 10 horas |
| pontuacao_maxima | real | não | teto opcional |
| evidencia_necessaria | texto | não | tipo de documento esperado |
| ativa | booleano | sim | regra disponível para uso |
| observacoes | texto | não | campo livre |

---

## 7.4 Entidade `checkins`

| Campo | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| id | inteiro | sim | identificador |
| ano_referencia | inteiro | sim | ano monitorado |
| data_checkin | data | sim | data da revisão |
| fator | texto | não | fator específico ou geral |
| pontuacao_acumulada | real | não | valor naquele momento |
| status | texto | não | verde/amarelo/vermelho |
| nota | texto | não | comentário do check-in |

## 7.5 Entidade `alertas`

| Campo | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| id | inteiro | sim | identificador |
| ano_referencia | inteiro | sim | ano monitorado |
| fator | texto | não | fator relacionado ou geral |
| tipo_alerta | texto | sim | evidência pendente, risco alto, revisão atrasada etc. |
| severidade | texto | sim | baixa, média, alta |
| mensagem | texto | sim | texto do alerta |
| resolvido | booleano | sim | indica tratamento pelo usuário |
| created_at | datetime | sim | criação |
| updated_at | datetime | sim | atualização |

---

## 8. Catálogo inicial de regras padrão

## 8.1 Formação / Atualização Continuada

| Atividade | Fórmula |
|-----------|---------|
| Participação em palestras, seminários e eventos com certificado | 2 pontos por evento |
| Participação em congressos com certificado | 5 pontos por evento |
| Cursos de atualização e/ou estágios | 5 pontos a cada 10h |
| Exercício de atividade profissional externa correlata | 5 pontos a cada 10h |
| Curso de especialização | 15 pontos fixos |
| Mestrado ou doutorado | 15 pontos fixos |
| Banca de estágio supervisionado | 3 pontos fixos |
| Banca de monografia ou TCC | 5 pontos fixos |
| Banca de dissertação de mestrado | 10 pontos fixos |
| Banca de tese de doutorado | 15 pontos fixos |
| Atualização de legislações vigentes para chefias | 15 pontos fixos |

## 8.2 Funcional – Pedagógico

| Atividade | Fórmula |
|-----------|---------|
| Orientação de estágio supervisionado | 10 pontos por orientado |
| Orientação de TCC | 20 pontos por trabalho |
| Orientação de mestrado | 30 pontos fixos |
| Orientação de doutorado | 35 pontos fixos |
| Orientação de iniciação científica da UTFPR | 20 pontos fixos |
| Orientação de bolsista de desenvolvimento científico regional / recém-doutor / pós-doc | 20 pontos fixos |
| Orientação de bolsista mestre/doutor em projeto institucional | 20 pontos fixos |
| Coorientação de iniciação científica | 10 pontos fixos |
| Coorientação de mestrado | 10 pontos fixos |
| Coorientação de doutorado | 10 pontos fixos |
| Desenvolvimento de software didático | 35 pontos fixos |
| Autoria de livro técnico/científico | 35 pontos por livro |
| Autoria de capítulo de livro técnico/científico | 20 pontos por capítulo |
| Organização/edição de livro ou anais científicos | 35 pontos por livro |
| Tradução de livro técnico/científico | 30 pontos por livro |
| Editor-chefe de revista científica internacional | 10 pontos fixos |
| Editor associado de revista científica nacional | 5 pontos fixos |
| Conselho científico/editorial de revista internacional | 5 pontos fixos |
| Conselho científico/editorial de revista nacional | 3 pontos fixos |
| Participação em reunião de departamento | valor manual entre 0 e 10 |
| Entrega de documentação acadêmica no prazo | valor manual entre 0 e 10 |

## 8.3 Produção Institucional

| Atividade | Fórmula |
|-----------|---------|
| Cargo nomeado por portaria | 10 pontos fixos |
| Chefia de grupo de disciplinas | 10 pontos fixos |
| Presidência de comissão por portaria | 5 pontos fixos |
| Membro de comissão por portaria | 5 pontos fixos |
| Membro de banca de concurso público | 5 pontos fixos |
| Membro de banca de teste seletivo | 5 pontos fixos |
| Participação em conselho departamental ou colegiado | 5 pontos fixos |
| Organização de evento da UTFPR | 10 pontos por atividade |
| Responsável por laboratório | 10 pontos fixos |
| Responsável por atividades complementares | 10 pontos fixos |
| Responsável pela orientação de estágio | 10 pontos fixos |
| Responsável pelo trabalho de diplomação | 10 pontos fixos |
| Assessor de coordenação | 10 pontos fixos |
| Participação em evento representando a instituição / apresentando trabalho / palestrando em evento nacional | 10 pontos por participação |

---

## 9. Fluxos de uso

## 9.1 Fluxo A — Cadastro de atividade

1. usuário acessa “Nova atividade”;
2. informa título, data e fator;
3. escolhe uma regra existente;
4. preenche quantidade ou carga horária, se necessário;
5. sistema calcula pontuação estimada;
6. usuário salva;
7. atividade entra no ano selecionado.

## 9.2 Fluxo B — Anexar evidência

1. usuário abre uma atividade;
2. seleciona “Adicionar evidência”;
3. informa tipo de evidência;
4. faz upload ou cola link/caminho;
5. salva;
6. sistema atualiza status da atividade.

## 9.3 Fluxo C — Criar regra personalizada

1. usuário acessa “Nova regra personalizada”;
2. escolhe categoria principal;
3. escreve nome e descrição;
4. define fórmula;
5. define evidência necessária;
6. salva;
7. regra passa a ficar disponível no cadastro de atividades.

## 9.4 Fluxo D — Revisão anual

1. usuário seleciona um ano;
2. dashboard exibe totais por fator;
3. lista atividades pendentes;
4. lista atividades sem evidência;
5. permite ajustes;
6. usuário gera relatório.

## 9.5 Fluxo E — Alertas e recomendações

1. usuário acessa o dashboard do ano;
2. sistema calcula pontuação, faltante e risco por fator;
3. sistema exibe alertas automáticos;
4. sistema mostra recomendações de revisão;
5. sistema apresenta sugestões de ações sem alterar os dados.

## 9.6 Fluxo F — Apoio com ChatGPT (MVP)

1. usuário solicita uma análise do ano corrente ou de um fator específico;
2. sistema reúne os dados já estruturados;
3. usuário envia ou aprova o contexto a ser analisado;
4. ChatGPT retorna resumo, destaques de risco, pendências e sugestões textuais;
5. usuário decide manualmente o que aproveitar no relatório ou na revisão.

---

## 10. Requisitos funcionais detalhados

### RF-01 — Seleção de ano
O sistema deve permitir navegar por ano de referência.

### RF-02 — Cadastro de atividade
O sistema deve permitir criação, edição e exclusão lógica de atividade.

### RF-03 — Associação a fator
Toda atividade deve pertencer a um dos três fatores principais.

### RF-04 — Associação a regra
A atividade poderá usar uma regra padrão ou personalizada.

### RF-05 — Cálculo automático
O sistema deve calcular pontuação estimada quando a fórmula for determinística.

### RF-06 — Valor manual
O sistema deve permitir valor manual quando a regra for do tipo manual ou intervalo.

### RF-07 — Cadastro de evidência
O sistema deve permitir registrar múltiplas evidências para uma atividade.

### RF-08 — Painel por fator
O sistema deve mostrar total acumulado e faltante por fator.

### RF-09 — Painel de risco
O sistema deve calcular e exibir risco por fator.

### RF-10 — Pendências
O sistema deve exibir lista filtrável de pendências.

### RF-11 — Alertas automáticos
O sistema deve gerar alertas automáticos para itens faltantes e situações de risco.

### RF-12 — Recomendações de revisão
O sistema deve exibir recomendações de revisão com base em pendências, risco e tempo desde o último check-in.

### RF-13 — Sugestão de ações
O sistema deve apresentar sugestões de ações relacionadas às lacunas detectadas.

### RF-14 — Regras personalizadas
O sistema deve permitir cadastrar regras livres reutilizáveis.

### RF-15 — Exportação
O sistema deve exportar relatório anual.

### RF-16 — Apoio com ChatGPT no MVP
O sistema deve permitir uso opcional de um fluxo MVP de conexão com ChatGPT para resumir dados, destacar riscos e apoiar a redação de consolidações, sem alterar automaticamente os registros.

### RF-17 — Personalização pelo perfil de escrita
O sistema deve permitir, opcionalmente, que o ChatGPT utilize o perfil de escrita e de argumentação previamente observado nas conversas do usuário para produzir sugestões e textos mais alinhados ao seu estilo.

### RF-18 — Sugestão de indicadores e oportunidades
Com base nos dados registrados e, opcionalmente, no histórico de atividades observadas no perfil do usuário, o sistema deve sugerir:
- indicadores que poderiam ser apresentados para reduzir o risco em cada fator;
- atividades já realizadas pelo usuário que poderiam ser convertidas em pontuação;
- evidências e documentos necessários para formalizar cada sugestão;
- ações recomendadas para alcançar a pontuação mínima ou desejada.

### RF-19 — Controle explícito de privacidade
O uso do perfil de escrita deve exigir ativação explícita do usuário e indicar claramente quais tipos de contexto poderão ser utilizados.

### RF-20 — Histórico
O sistema deve manter dados de anos anteriores sem sobrescrever históricos.

---

## 11. Requisitos não funcionais detalhados

### RNF-01 — Baixo atrito
Cadastrar uma atividade comum deve levar pouco tempo.

### RNF-02 — Persistência simples
A primeira versão deve funcionar sem servidor de banco dedicado.

### RNF-03 — Portabilidade
Os dados devem poder ser copiados e armazenados por backup simples.

### RNF-04 — Usabilidade
A interface deve ser simples para uso recorrente durante o ano.

### RNF-05 — Transparência
O sistema deve deixar claro como a pontuação foi calculada.

### RNF-06 — Não interferência automática
Alertas, recomendações, sugestões e apoio com ChatGPT não devem alterar automaticamente pontuação, classificação ou evidências.

### RNF-07 — Privacidade e transparência
Quando o modo de personalização pelo perfil do usuário estiver habilitado, o sistema deve informar de forma transparente quais informações de estilo e escrita estão sendo utilizadas.

---

## 12. Regras de validação

- título não pode ser vazio;
- data da atividade é obrigatória;
- ano de referência é obrigatório;
- fator é obrigatório;
- regra personalizada exige descrição;
- regra do tipo por hora exige unidade e divisor coerentes;
- pontuação confirmada não pode ser negativa;
- evidência vinculada deve manter referência para a atividade;
- atividade sem regra deve ser marcada como pendente;
- alerta automático deve ser recalculado quando atividade, evidência ou regra for alterada;
- conexão com ChatGPT no MVP deve operar apenas sobre dados explicitamente selecionados ou exportados pelo usuário;
- uso do perfil de escrita do usuário deve exigir consentimento explícito antes de qualquer envio de contexto adicional.

---

## 13. Estratégia de implementação sugerida

## Fase 1 — Base de dados e catálogo de regras
- criar estrutura SQLite;
- criar tabelas principais;
- carregar regras padrão.

## Fase 2 — Cadastro e edição
- tela de cadastro de atividade;
- tela de regras personalizadas;
- tela de evidências.

## Fase 3 — Dashboard e risco
- cards por fator;
- totais;
- pendências;
- risco por fator;
- filtros por ano.

## Fase 4 — Alertas e recomendações
- alertas automáticos;
- recomendações de revisão;
- sugestões de ações.

## Fase 5 — Relatório anual e MVP ChatGPT
- consolidação;
- exportação;
- fluxo opcional de apoio com ChatGPT;
- revisão final.

---

## 14. Critérios de aceite da v1

A v1 será considerada pronta quando:

1. for possível cadastrar atividades nos três fatores;
2. for possível associar evidências às atividades;
3. for possível usar regras padrão e personalizadas;
4. o sistema calcular pontuação estimada corretamente para regras determinísticas;
5. o painel anual mostrar totais e risco por fator;
6. o sistema listar pendências relevantes e emitir alertas automáticos;
7. o sistema exibir recomendações de revisão e sugestões de ações sem alterar dados automaticamente;
8. o relatório anual puder ser exportado;
9. o fluxo MVP com ChatGPT puder apoiar a análise textual dos dados já registrados, sem modificar automaticamente os registros.

---

## 15. Estrutura sugerida do arquivo/exportação `Spec.md`

Esta especificação já pode ser usada como base de implementação e também como insumo para a próxima etapa, que pode ser:

- `database_schema.md`
- `ui_flow.md`
- `implementation_plan.md`

ou diretamente um prompt de implementação para Codex.

