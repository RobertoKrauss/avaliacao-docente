
# PRD.md — Sistema de Controle para Avaliação de Desempenho Docente (UTFPR)

## 1. Objetivo desta etapa

Documentar, em um único artefato, o problema de negócio, os requisitos de alto nível, os padrões externos encontrados e a base tecnológica viável para um sistema de controle que reduza a perda de pontos na avaliação de desempenho docente, com foco em:

- Formação / Atualização Continuada
- Fator Funcional – Pedagógico
- Produção Institucional

Este PRD resume:
- o que a regra interna da UTFPR exige;
- quais padrões externos semelhantes já existem em universidades e sistemas de gestão de desempenho;
- quais tecnologias têm documentação oficial adequada para implementação;
- qual recorte mínimo de produto faz sentido para a próxima fase.

---

## 2. Contexto do problema

O manual da UTFPR estrutura a avaliação em desempenho coletivo e desempenho individual. Para docentes, o desempenho individual soma até **70 pontos**, distribuídos em três fatores:

- **Formação / Atualização Continuada**: até **15 pontos**
- **Funcional – Pedagógico**: até **35 pontos**
- **Produção Institucional**: até **20 pontos**

Além disso, o desempenho coletivo vale até **30 pontos**, e a progressão funcional por mérito exige:
- no mínimo **40% dos pontos em cada etapa** (desempenho coletivo e individual);
- pontuação final mínima de **60 pontos**.

O próprio manual também estabelece dois princípios diretamente relevantes para este projeto:

1. **Portfólio**: o servidor deve manter pasta individual atualizada para registrar, documentar, assegurar e subsidiar o processo avaliativo.
2. **Continuidade**: o acompanhamento deve ser sistemático e histórico.

Na prática, o problema é que muitas evidências ficam dispersas entre:
- certificados;
- portarias;
- atas;
- comprovantes;
- páginas Moodle;
- materiais didáticos;
- e-mails;
- planilhas;
- arquivos em nuvem;
- memória pessoal.

Isso gera o risco de:
- esquecer atividades realizadas;
- não anexar evidências;
- não transformar trabalho já feito em item pontuável;
- chegar ao fim do ciclo sem visão clara do déficit por fator.

---

## 3. Problema de produto

**Problema central:** o docente realiza atividades potencialmente pontuáveis ao longo do ano, mas não possui um sistema contínuo de registro, consolidação, evidência e acompanhamento da pontuação por fator.

**Consequência operacional:** perda recorrente de pontos não por ausência de atividade, mas por ausência de controle estruturado.

---

## 4. Objetivo do produto

Criar um sistema pessoal de controle anual que permita:

1. registrar cada atividade relevante no momento em que ela ocorre;
2. anexar ou vincular evidências;
3. classificar a atividade nos fatores da avaliação;
4. acompanhar a pontuação acumulada por fator;
5. identificar lacunas antes do fechamento do ciclo;
6. gerar um resumo consolidado para apoiar a negociação, o preenchimento e a comprovação da avaliação.

---

## 5. Escopo funcional de alto nível

O produto deve operar como um **registro contínuo de evidências e pontuação**, e não apenas como uma planilha final preenchida no encerramento do ano.

### 5.1 Capacidades principais

- Cadastro de atividades
- Armazenamento ou vínculo de evidências
- Classificação por fator e subtipo
- Controle de status da evidência
- Cálculo de pontuação acumulada
- Visualização do déficit por fator
- Check-ins periódicos
- Geração de relatório consolidado

---

## 6. Requisitos do negócio derivados do manual da UTFPR

### 6.1 Estrutura dos fatores para docente

#### Formação / Atualização Continuada (até 15 pontos)
Itens-base do formulário docente:
- participação em eventos com certificado;
- participação em cursos de atualização e/ou estágios e/ou exercício profissional externo relevante;
- participação em cursos de pós-graduação;
- participação em bancas de estágio, monografia, mestrado e doutorado;
- 1 item adicional negociado.

#### Funcional – Pedagógico (até 35 pontos)
Itens-base do formulário docente:
- orientação de trabalhos/estágios;
- desenvolvimento de material didático e/ou aplicação de novas metodologias;
- participação em reunião de departamento e/ou grupo de disciplina;
- entrega de documentação acadêmica nos prazos;
- 1 item adicional negociado.

#### Produção Institucional (até 20 pontos)
Itens-base do formulário docente:
- participação em grupos de trabalho, comissões, bancas e colegiados;
- participação em eventos representando a instituição, apresentando trabalho ou como palestrante;
- desenvolvimento de projetos de interesse do departamento, coordenação e/ou instituição;
- publicações em geral desenvolvidas pelo docente;
- até 2 itens adicionais negociados.

### 6.2 Regras de negociação relevantes ao sistema

O manual informa que:
- a negociação ocorre no início do período avaliativo;
- pontuações e itens negociados devem ser registrados no SIAVI;
- para docentes há possibilidade de personalização em todos os três fatores;
- o processo deve refletir necessidades institucionais, setoriais e individuais.

### 6.3 Implicação para o produto

O sistema precisa separar:
- **item realizado**
- **evidência disponível**
- **item negociado**
- **pontuação estimada**
- **pontuação homologada/confirmada**

Ou seja: o produto não deve tratar “atividade realizada” e “atividade pontuada” como a mesma coisa.

---

## 7. Padrões externos encontrados

Esta seção resume padrões observados em sistemas acadêmicos e de gestão de desempenho que fazem trabalho parecido.

### 7.1 Padrão A — Centralização única de atividades acadêmicas

Sistemas como **Watermark Faculty Success** e **Interfolio Faculty Activity Reporting** operam com a mesma lógica central:

- manter um hub central de dados de atividades;
- reutilizar os mesmos registros para relatórios diferentes;
- reduzir retrabalho em ciclos anuais de avaliação;
- manter materiais de apoio e dados de atividade em formato pesquisável.

**Padrão identificado:** “registrar uma vez, reutilizar muitas vezes”.

**Aplicação ao seu caso:** uma atividade como “participação em banca”, “material didático produzido” ou “portaria de comissão” deve entrar uma única vez na base e depois aparecer:
- no painel anual;
- no relatório final;
- na listagem de evidências;
- no resumo por fator.

---

### 7.2 Padrão B — Faculty Activity Reporting / Annual Faculty Activity Report

A literatura de produto desses sistemas mostra um padrão recorrente:

- coleta contínua de teaching, research e service;
- produção de relatórios anuais;
- apoio a review, tenure, promotion, accreditation e CV.

**Aplicação ao seu caso:** apesar de a taxonomia da UTFPR ser diferente, a lógica estrutural é a mesma:
- capturar evidência de atividade docente;
- organizar por categoria institucional;
- gerar relatório anual.

---

### 7.3 Padrão C — Teaching Portfolio / Evidence Portfolio

Guias universitários sobre teaching portfolio mostram uma prática estável:

- coletar materiais ao longo do tempo;
- guardar evidências seletivas;
- registrar avaliação, reflexão e documentação do ensino;
- manter arquivo separado e cumulativo.

**Aplicação ao seu caso:** o fator Funcional – Pedagógico se beneficia diretamente desse padrão. Exemplos de evidência que entram bem nesse modelo:
- apostilas;
- slides;
- atividades Moodle;
- listas;
- rubricas;
- provas;
- softwares didáticos;
- registros de novas metodologias;
- relatórios de orientação;
- atas e comprovantes de reuniões.

---

### 7.4 Padrão D — Check-ins regulares de progresso

Documentação de gestão por OKRs e desempenho contínuo mostra um padrão muito consistente:

- o progresso não é acompanhado apenas no fim do ciclo;
- o sistema usa check-ins periódicos;
- cada check-in registra métrica, status e nota contextual;
- lembretes automáticos mantêm cadência.

**Aplicação ao seu caso:** o produto deve ter revisão periódica de pontuação e evidências, por exemplo:
- mensal;
- bimestral;
- ou trimestral.

A lógica não é “esperar dezembro”; é detectar lacuna cedo.

---

### 7.5 Padrão E — Dashboard de lacunas (gap dashboard)

Sistemas de acompanhamento de metas costumam mostrar para cada eixo:
- meta;
- realizado;
- faltante;
- status;
- tendência.

**Aplicação ao seu caso:** para cada fator da UTFPR, o painel deve mostrar:
- pontuação máxima;
- pontuação estimada registrada;
- pontuação com evidência válida;
- pontuação confirmada;
- déficit restante.

---

### 7.6 Padrão F — Separação entre dado, documento e relatório

Nos sistemas externos pesquisados, há uma separação clara entre:
- **registro estruturado** da atividade;
- **material comprobatório** anexado ou vinculado;
- **relatório final** gerado sob demanda.

**Aplicação ao seu caso:** isso evita usar PDF solto como se ele fosse a base do sistema. O PDF deve ser evidência; a base do sistema deve ser estruturada.

---

## 8. Tecnologias pesquisadas com documentação oficial

Aqui estão as tecnologias com documentação oficial adequada e aderência ao problema.

### 8.1 Google Apps Script

**O que é na prática:** plataforma JavaScript em nuvem para automatizar e integrar Google Workspace.

**Capacidades relevantes:**
- automação de Planilhas Google;
- integração com Forms, Drive, Gmail e Calendar;
- execução em servidores do Google;
- editor no navegador;
- gatilhos baseados em tempo e evento;
- possibilidade de web app leve.

**Adequação ao projeto:**
- muito forte para MVP;
- boa para automação de alertas;
- boa para integração com planilha e Drive;
- adequada para protótipo rápido sem infraestrutura própria.

---

### 8.2 Google Sheets API

**O que é na prática:** API REST para ler, escrever e alterar dados de planilhas.

**Capacidades relevantes:**
- leitura e escrita de células;
- criação de planilhas;
- atualização de dados e formatação;
- uso como banco tabular simples.

**Adequação ao projeto:**
- boa para MVP orientado a planilha;
- útil se houver integração externa com Python ou outro backend.

---

### 8.3 Google Forms API

**O que é na prática:** API para criar, modificar e coletar respostas de formulários.

**Capacidades relevantes:**
- criação de formulários;
- leitura de respostas;
- automação de coleta de dados;
- notificações/push notifications.

**Adequação ao projeto:**
- boa para criar interface de lançamento rápido de atividades;
- útil para captura via celular;
- útil para um formulário do tipo “registrar atividade + anexar evidência”.

---

### 8.4 Google Drive API

**O que é na prática:** API REST para armazenamento, busca, upload, download e organização de arquivos no Drive.

**Capacidades relevantes:**
- upload e download;
- busca por arquivos e metadados;
- organização de pastas;
- compartilhamento;
- monitoração de eventos.

**Adequação ao projeto:**
- essencial se as evidências ficarem no Drive;
- útil para vincular automaticamente certificados, portarias, atas, PDFs e materiais didáticos.

---

### 8.5 Python + sqlite3

**O que é na prática:** o módulo `sqlite3` da biblioteca padrão do Python fornece uma interface DB-API 2.0 para SQLite, um banco de dados leve baseado em arquivo, sem processo servidor separado.

**Capacidades relevantes:**
- banco local simples e robusto;
- fácil backup;
- ideal para app individual;
- baixo custo operacional;
- sem necessidade de servidor de banco dedicado.

**Adequação ao projeto:**
- excelente para versão pessoal/autônoma;
- muito aderente a um sistema de controle anual com poucos usuários;
- adequado para histórico multi-ano.

---

### 8.6 SQLite

**O que é na prática:** banco de dados embarcado, documentado e amplamente usado em aplicações locais.

**Capacidades relevantes:**
- zero administração de servidor;
- arquivo único;
- SQL completo o suficiente para o caso;
- documentação sólida.

**Adequação ao projeto:**
- muito adequado como camada de persistência para app desktop/web pessoal.

---

### 8.7 Streamlit

**O que é na prática:** framework Python para construir data apps com frontend web e backend Python.

**Capacidades relevantes:**
- criação rápida de interface web;
- execução local ou em servidor;
- integração fácil com Python;
- boa para dashboard, filtros, formulários e visualizações.

**Adequação ao projeto:**
- excelente para dashboard e painel de pontuação;
- muito bom para um sistema pessoal com interface amigável;
- bom para MVP v2 ou v3, acima do protótipo em planilha.

---

## 9. Padrão arquitetural consolidado para este projeto

A partir dos padrões externos e das tecnologias pesquisadas, o padrão mais consistente para este problema é:

### 9.1 Camadas

1. **Camada de registro**
   - formulário ou tela para lançar atividade.

2. **Camada de dados**
   - planilha estruturada ou banco SQLite.

3. **Camada de evidência**
   - arquivos no Drive ou em pasta organizada.

4. **Camada de classificação**
   - regra que associa a atividade ao fator e subtipo.

5. **Camada de acompanhamento**
   - dashboard com acumulado, faltante e status.

6. **Camada de saída**
   - relatório anual consolidado.

---

## 10. Entidades principais do sistema

### 10.1 Atividade
Campos esperados:
- id
- título
- descrição
- data da atividade
- período letivo/ano
- fator
- subtipo
- item negociado? (sim/não)
- pontuação estimada
- pontuação confirmada
- status
- observações

### 10.2 Evidência
Campos esperados:
- id
- atividade_id
- tipo de evidência
- nome do arquivo
- link/path
- data de anexação
- validade/pendência
- observações

### 10.3 Regra de pontuação
Campos esperados:
- fator
- subtipo
- limite máximo
- origem da regra (manual / negociação)
- observações

### 10.4 Check-in
Campos esperados:
- id
- data
- fator
- pontuação acumulada
- status
- nota contextual
- pendências identificadas

### 10.5 Relatório anual
Campos esperados:
- ano
- total por fator
- evidências faltantes
- itens negociados
- itens concluídos
- itens pendentes

---

## 11. Taxonomia inicial sugerida para classificação

### 11.1 Formação / Atualização Continuada
Subtipos iniciais:
- evento com certificado
- curso de atualização
- estágio/capacitação
- pós-graduação
- banca
- grupo de estudo/discussão
- leitura/documentação relevante
- mentoria/orientação/coaching

### 11.2 Funcional – Pedagógico
Subtipos iniciais:
- orientação de estágio
- orientação de TCC
- orientação de IC
- orientação de mestrado/doutorado
- material didático
- software didático
- nova metodologia
- reunião de departamento/grupo
- entrega de documentação
- outro item negociado

### 11.3 Produção Institucional
Subtipos iniciais:
- comissão
- colegiado
- banca
- portaria/função
- evento representando a instituição
- palestra/curso ministrado
- projeto institucional
- extensão
- publicação
- organização de evento
- assessoramento/coordenação
- material de apoio ao setor

---

## 12. Fluxo funcional resumido

### 12.1 Fluxo ideal do usuário

1. O docente realiza uma atividade.
2. Registra a atividade no sistema em até poucos minutos.
3. Anexa ou vincula a evidência.
4. O sistema classifica no fator correto.
5. A pontuação estimada é somada ao painel.
6. Em check-ins periódicos, o sistema mostra lacunas.
7. No fechamento do ciclo, o relatório anual é gerado.

---

## 13. Requisitos funcionais do MVP

### RF-01 — Cadastrar atividade
O usuário deve conseguir registrar uma atividade em formulário simples.

### RF-02 — Vincular evidência
O usuário deve conseguir anexar ou linkar a evidência.

### RF-03 — Classificar por fator
O sistema deve classificar a atividade em:
- Formação / Atualização Continuada
- Funcional – Pedagógico
- Produção Institucional

### RF-04 — Acompanhar pontuação
O sistema deve mostrar total acumulado por fator.

### RF-05 — Mostrar lacuna
O sistema deve mostrar quanto falta para cada fator atingir o teto desejado.

### RF-06 — Identificar pendências
O sistema deve listar atividades:
- sem evidência;
- sem classificação;
- sem confirmação;
- sem pontuação atribuída.

### RF-07 — Gerar relatório anual
O sistema deve gerar uma consolidação anual com:
- atividades;
- evidências;
- pontuação por fator;
- pendências.

---

## 14. Requisitos não funcionais

- uso rápido;
- baixo atrito para lançamento;
- acesso por computador e celular;
- backup simples;
- organização histórica por ano;
- busca rápida por evidência;
- exportação em formato compartilhável;
- curva de aprendizado baixa.

---

## 15. Opções de implementação encontradas

### Opção A — Google Workspace-first
**Componentes:**
- Google Form
- Google Sheets
- Google Drive
- Google Apps Script

**Perfil:**
- MVP rápido;
- baixo custo;
- baixo esforço de infraestrutura;
- boa aderência a uso móvel e automação simples.

---

### Opção B — Python local/web pessoal
**Componentes:**
- Python
- SQLite
- Streamlit
- pasta local ou Drive para evidências

**Perfil:**
- mais robusto;
- melhor dashboard;
- melhor controle de dados;
- excelente para evolução futura.

---

### Opção C — Híbrido
**Componentes:**
- captura via Google Form
- armazenamento/integração com Drive
- processamento e dashboard em Python/Streamlit

**Perfil:**
- captura rápida + dashboard melhor;
- combina praticidade de coleta com painel mais forte.

---

## 16. MVP recomendado para a próxima etapa

Como esta etapa é apenas de PRD, o MVP aqui é definido apenas em termos de escopo documental.

### MVP mínimo
- registrar atividade;
- guardar evidência;
- classificar por fator;
- acompanhar pontuação acumulada;
- listar pendências;
- gerar relatório simples.

---

## 17. Critérios de sucesso do produto

O sistema será bem-sucedido se, ao longo do ciclo anual, permitir:

1. visibilidade contínua do total por fator;
2. redução do esquecimento de atividades já realizadas;
3. redução de evidências dispersas;
4. preparação mais simples para a negociação e avaliação;
5. menor risco de perder pontuação por falha de registro.

---

## 18. Riscos documentados nesta etapa

- diferença entre atividade realizada e item efetivamente pontuado após negociação;
- necessidade de manter aderência ao que foi negociado no SIAVI;
- dependência de evidência documental mínima;
- risco de excesso de fricção no cadastro se a interface for lenta.

---

## 19. Decisões documentais desta etapa

Com base no manual da UTFPR e nos padrões externos pesquisados, o produto deve ser tratado como um sistema de:

- **registro contínuo de atividades**;
- **portfólio/evidence repository**;
- **dashboard de lacunas por fator**;
- **gerador de relatório anual**.

Ele não deve ser modelado apenas como “planilha final de pontos”.

---

## 20. Fontes pesquisadas

### Manual interno UTFPR
- Manual de Avaliação de Desempenho dos Servidores da UTFPR (5ª versão, maio/2017)

### Documentação oficial de tecnologia
- Google Apps Script Overview
- Google Sheets API Overview
- Google Forms API Overview
- Google Drive API Overview
- Python `sqlite3` documentation
- SQLite documentation
- Streamlit documentation
- Streamlit: Connecting to data
- Streamlit: Client-server architecture

### Padrões externos / sistemas equivalentes
- Watermark Faculty Success
- Interfolio Faculty Activity Reporting
- Cornell Center for Teaching Innovation — Teaching Portfolio
- Microsoft Viva Goals documentation on check-ins and reminders

---

## 21. Próxima saída natural após este PRD

A próxima etapa técnica pode produzir um dos seguintes artefatos:

- modelo de dados;
- estrutura da planilha/base SQLite;
- dicionário de campos;
- wireframe do dashboard;
- fluxo de cadastro;
- tabela de regras de pontuação por subtipo;
- protótipo do MVP.

