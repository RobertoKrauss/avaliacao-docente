# database_schema.md

## 1. Objetivo

Este documento define o esquema inicial do banco de dados da v1 do sistema de controle da avaliação de desempenho docente.

Premissas:
- Banco local SQLite.
- Estrutura preparada para futura migração para PostgreSQL.
- Todas as tabelas utilizam chave primária inteira autoincremental.
- Datas devem ser armazenadas em ISO-8601 (`YYYY-MM-DD` ou `YYYY-MM-DD HH:MM:SS`).
- Exclusão lógica sempre que possível.

---

# 2. Convenções

## 2.1 Nomes de tabelas
- Sempre no plural.
- Snake case.

Exemplo:
- `atividades`
- `regras_pontuacao`
- `evidencias`

## 2.2 Campos padrão

As tabelas principais devem possuir, quando aplicável:

```text
created_at DATETIME NOT NULL
updated_at DATETIME NOT NULL
deleted_at DATETIME NULL
```

- `deleted_at = NULL` → registro ativo.
- `deleted_at != NULL` → registro excluído logicamente.

---

# 3. Tabela `anos_avaliacao`

Representa cada ciclo anual monitorado.

| Campo | Tipo | Obrigatório | Observação |
|-------|-------|-------------|------------|
| id | INTEGER PK | Sim | autoincrement |
| ano | INTEGER | Sim | único |
| descricao | TEXT | Não | ex.: Avaliação 2026 |
| meta_formacao | REAL | Sim | default 15 |
| meta_funcional | REAL | Sim | default 35 |
| meta_producao | REAL | Sim | default 20 |
| ultima_revisao | DATE | Não | última revisão manual |
| created_at | DATETIME | Sim | |
| updated_at | DATETIME | Sim | |
| deleted_at | DATETIME | Não | |

### Constraints

```text
UNIQUE(ano)
CHECK(meta_formacao >= 0)
CHECK(meta_funcional >= 0)
CHECK(meta_producao >= 0)
```

---

# 4. Tabela `regras_pontuacao`

Armazena regras padrão e personalizadas.

| Campo | Tipo | Obrigatório | Observação |
|-------|-------|-------------|------------|
| id | INTEGER PK | Sim | |
| nome | TEXT | Sim | |
| categoria_principal | TEXT | Sim | formação, funcional, produção |
| subtipo | TEXT | Não | |
| origem | TEXT | Sim | padrao, personalizada |
| descricao_regra | TEXT | Sim | |
| justificativa | TEXT | Não | obrigatório para personalizada |
| tipo_formula | TEXT | Sim | fixo, por_unidade, por_hora, intervalo, manual |
| valor_base | REAL | Não | |
| unidade | TEXT | Não | evento, hora, orientado, capítulo etc. |
| divisor_unidade | REAL | Não | ex.: 10 horas |
| pontuacao_maxima | REAL | Não | |
| exige_valor_manual | INTEGER | Sim | 0 ou 1 |
| evidencia_necessaria | TEXT | Não | |
| origem_documento | TEXT | Não | manual, imagem, regra criada pelo usuário |
| ativa | INTEGER | Sim | 0 ou 1 |
| observacoes | TEXT | Não | |
| created_at | DATETIME | Sim | |
| updated_at | DATETIME | Sim | |
| deleted_at | DATETIME | Não | |

### Constraints

```text
CHECK(categoria_principal IN ('formacao','funcional','producao'))
CHECK(origem IN ('padrao','personalizada'))
CHECK(tipo_formula IN ('fixo','por_unidade','por_hora','intervalo','manual'))
CHECK(exige_valor_manual IN (0,1))
CHECK(ativa IN (0,1))
```

---

# 5. Tabela `atividades`

Tabela central do sistema.

| Campo | Tipo | Obrigatório | Observação |
|-------|-------|-------------|------------|
| id | INTEGER PK | Sim | |
| ano_id | INTEGER FK | Sim | referência a `anos_avaliacao.id` |
| titulo | TEXT | Sim | |
| descricao | TEXT | Não | |
| data_atividade | DATE | Sim | |
| periodo_letivo | TEXT | Não | ex.: 2026/1 |
| fator | TEXT | Sim | formação, funcional, produção |
| subtipo | TEXT | Não | |
| regra_id | INTEGER FK | Não | referência a `regras_pontuacao.id` |
| quantidade | REAL | Não | |
| carga_horaria | REAL | Não | |
| valor_manual | REAL | Não | usado em regra manual |
| pontuacao_estimada | REAL | Não | calculada automaticamente |
| pontuacao_confirmada | REAL | Não | preenchida pelo usuário |
| pontuacao_original | REAL | Não | preserva valor calculado original |
| item_negociado | INTEGER | Sim | 0 ou 1 |
| status | TEXT | Sim | |
| prioridade | TEXT | Não | baixa, média, alta |
| possui_potencial_nao_explorado | INTEGER | Sim | 0 ou 1 |
| observacoes | TEXT | Não | |
| tags | TEXT | Não | lista separada por vírgula |
| created_at | DATETIME | Sim | |
| updated_at | DATETIME | Sim | |
| deleted_at | DATETIME | Não | |

### Status permitidos

```text
rascunho
registrada
com_evidencia_pendente
com_evidencia_anexada
revisada
contabilizada
arquivada
nao_pontuada
```

### Constraints

```text
FOREIGN KEY (ano_id) REFERENCES anos_avaliacao(id)
FOREIGN KEY (regra_id) REFERENCES regras_pontuacao(id)
CHECK(fator IN ('formacao','funcional','producao'))
CHECK(item_negociado IN (0,1))
CHECK(possui_potencial_nao_explorado IN (0,1))
CHECK(pontuacao_estimada IS NULL OR pontuacao_estimada >= 0)
CHECK(pontuacao_confirmada IS NULL OR pontuacao_confirmada >= 0)
```

---

# 6. Tabela `evidencias`

Cada atividade pode possuir várias evidências.

| Campo | Tipo | Obrigatório | Observação |
|-------|-------|-------------|------------|
| id | INTEGER PK | Sim | |
| atividade_id | INTEGER FK | Sim | |
| tipo | TEXT | Sim | |
| nome_arquivo | TEXT | Não | |
| caminho_arquivo | TEXT | Não | caminho local ou URL |
| descricao | TEXT | Não | |
| data_anexacao | DATETIME | Sim | |
| validade_status | TEXT | Não | valida, pendente, revisar |
| data_validade | DATE | Não | |
| obrigatoria | INTEGER | Sim | 0 ou 1 |
| aprovada | INTEGER | Sim | 0 ou 1 |
| observacoes | TEXT | Não | |
| created_at | DATETIME | Sim | |
| updated_at | DATETIME | Sim | |
| deleted_at | DATETIME | Não | |

### Constraints

```text
FOREIGN KEY (atividade_id) REFERENCES atividades(id)
CHECK(tipo IN (
  'certificado',
  'portaria',
  'ata',
  'email',
  'declaracao',
  'pdf',
  'imagem',
  'link',
  'material_didatico',
  'print',
  'outro'
))
CHECK(obrigatoria IN (0,1))
CHECK(aprovada IN (0,1))
```

---

# 7. Tabela `checkins`

Registra revisões periódicas do usuário.

| Campo | Tipo | Obrigatório | Observação |
|-------|-------|-------------|------------|
| id | INTEGER PK | Sim | |
| ano_id | INTEGER FK | Sim | |
| fator | TEXT | Não | null = geral |
| data_checkin | DATE | Sim | |
| pontuacao_acumulada | REAL | Não | |
| status_risco | TEXT | Não | baixo, medio, alto |
| atividades_pendentes | INTEGER | Não | |
| nota | TEXT | Não | |
| created_at | DATETIME | Sim | |
| updated_at | DATETIME | Sim | |

### Constraints

```text
FOREIGN KEY (ano_id) REFERENCES anos_avaliacao(id)
CHECK(status_risco IN ('baixo','medio','alto'))
```

---

# 8. Tabela `alertas`

Alertas automáticos gerados pelo sistema.

| Campo | Tipo | Obrigatório | Observação |
|-------|-------|-------------|------------|
| id | INTEGER PK | Sim | |
| ano_id | INTEGER FK | Sim | |
| atividade_id | INTEGER FK | Não | opcional |
| fator | TEXT | Não | |
| tipo_alerta | TEXT | Sim | |
| severidade | TEXT | Sim | baixa, media, alta |
| mensagem | TEXT | Sim | |
| recomendacao | TEXT | Não | ação sugerida |
| resolvido | INTEGER | Sim | 0 ou 1 |
| resolvido_em | DATETIME | Não | |
| created_at | DATETIME | Sim | |
| updated_at | DATETIME | Sim | |

### Tipos sugeridos

```text
atividade_sem_evidencia
atividade_sem_regra
atividade_sem_fator
valor_manual_faltante
risco_alto
revisao_atrasada
pontuacao_baixa
potencial_nao_explorado
```

---

# 9. Tabela `sugestoes_chatgpt`

Armazena sugestões geradas pelo módulo opcional de apoio com ChatGPT.

| Campo | Tipo | Obrigatório | Observação |
|-------|-------|-------------|------------|
| id | INTEGER PK | Sim | |
| ano_id | INTEGER FK | Sim | |
| atividade_id | INTEGER FK | Não | |
| fator | TEXT | Não | |
| tipo_sugestao | TEXT | Sim | |
| titulo | TEXT | Sim | |
| texto | TEXT | Sim | |
| indicador_sugerido | TEXT | Não | |
| evidencias_sugeridas | TEXT | Não | |
| acao_recomendada | TEXT | Não | |
| origem_contexto | TEXT | Não | dados, perfil_chatgpt, ambos |
| aplicada_pelo_usuario | INTEGER | Sim | 0 ou 1 |
| created_at | DATETIME | Sim | |

### Tipos sugeridos

```text
resumo
recomendacao
indicador
oportunidade
revisao
texto_para_relatorio
```

Exemplo de uso:
- atividade: "Apostila de Fundamentos de Comunicações"
- indicador sugerido: "Material didático produzido"
- evidências sugeridas: "PDF, capa, data, disciplina, print do Moodle"
- ação recomendada: "Formalizar e cadastrar no fator funcional-pedagógico"

---

# 10. Tabela `configuracoes_usuario`

Configurações persistentes do usuário.

| Campo | Tipo | Obrigatório | Observação |
|-------|-------|-------------|------------|
| id | INTEGER PK | Sim | |
| chave | TEXT | Sim | única |
| valor | TEXT | Não | |
| descricao | TEXT | Não | |
| created_at | DATETIME | Sim | |
| updated_at | DATETIME | Sim | |

### Configurações previstas

```text
usar_perfil_chatgpt
ultima_analise_chatgpt
ano_padrao
mostrar_alertas_resolvidos
```

---

# 11. Índices sugeridos

```sql
CREATE INDEX idx_atividades_ano ON atividades(ano_id);
CREATE INDEX idx_atividades_fator ON atividades(fator);
CREATE INDEX idx_atividades_status ON atividades(status);
CREATE INDEX idx_atividades_regra ON atividades(regra_id);

CREATE INDEX idx_evidencias_atividade ON evidencias(atividade_id);

CREATE INDEX idx_alertas_ano ON alertas(ano_id);
CREATE INDEX idx_alertas_resolvido ON alertas(resolvido);
CREATE INDEX idx_alertas_tipo ON alertas(tipo_alerta);

CREATE INDEX idx_chatgpt_ano ON sugestoes_chatgpt(ano_id);
CREATE INDEX idx_chatgpt_tipo ON sugestoes_chatgpt(tipo_sugestao);
```

---

# 12. Relacionamentos

```text
anos_avaliacao 1 ---- N atividades
anos_avaliacao 1 ---- N checkins
anos_avaliacao 1 ---- N alertas
anos_avaliacao 1 ---- N sugestoes_chatgpt

regras_pontuacao 1 ---- N atividades

atividades 1 ---- N evidencias
atividades 1 ---- N alertas
atividades 1 ---- N sugestoes_chatgpt
```

---

# 13. Dados iniciais obrigatórios

Ao criar o banco pela primeira vez, o sistema deve:

1. Inserir automaticamente um registro em `anos_avaliacao` para o ano atual.
2. Inserir as metas padrão:
   - Formação = 15
   - Funcional = 35
   - Produção = 20
3. Popular `regras_pontuacao` com todas as regras padrão do `Spec_v3.md`.
4. Inserir a configuração:

```text
usar_perfil_chatgpt = false
```

---

# 14. Possível evolução futura

Campos e tabelas já foram desenhados para suportar no futuro:
- múltiplos usuários;
- login;
- workflow de aprovação;
- sincronização com Google Drive;
- OCR de documentos;
- integração com SIAVI;
- histórico de versões das atividades;
- rastreamento de alterações;
- recomendação automática baseada em aprendizado de uso.
