PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS anos_avaliacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ano INTEGER NOT NULL UNIQUE,
    descricao TEXT,
    meta_formacao REAL NOT NULL DEFAULT 15,
    meta_funcional REAL NOT NULL DEFAULT 35,
    meta_producao REAL NOT NULL DEFAULT 20,
    ultima_revisao DATE,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    deleted_at DATETIME
);

CREATE TABLE IF NOT EXISTS regras_pontuacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria_principal TEXT NOT NULL,
    subtipo TEXT,
    origem TEXT NOT NULL,
    descricao_regra TEXT NOT NULL,
    justificativa TEXT,
    tipo_formula TEXT NOT NULL,
    valor_base REAL,
    unidade TEXT,
    divisor_unidade REAL,
    pontuacao_maxima REAL,
    exige_valor_manual INTEGER NOT NULL,
    evidencia_necessaria TEXT,
    origem_documento TEXT,
    ativa INTEGER NOT NULL,
    observacoes TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    deleted_at DATETIME,
    CHECK(categoria_principal IN ('formacao','funcional','producao')),
    CHECK(origem IN ('padrao','personalizada')),
    CHECK(tipo_formula IN ('fixo','por_unidade','por_hora','intervalo','manual')),
    CHECK(exige_valor_manual IN (0,1)),
    CHECK(ativa IN (0,1))
);

CREATE TABLE IF NOT EXISTS atividades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ano_id INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT,
    data_atividade DATE NOT NULL,
    periodo_letivo TEXT,
    fator TEXT NOT NULL,
    subtipo TEXT,
    regra_id INTEGER,
    quantidade REAL,
    carga_horaria REAL,
    valor_manual REAL,
    pontuacao_estimada REAL,
    pontuacao_confirmada REAL,
    pontuacao_original REAL,
    item_negociado INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL,
    prioridade TEXT,
    possui_potencial_nao_explorado INTEGER NOT NULL DEFAULT 0,
    observacoes TEXT,
    tags TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    deleted_at DATETIME,
    FOREIGN KEY (ano_id) REFERENCES anos_avaliacao(id),
    FOREIGN KEY (regra_id) REFERENCES regras_pontuacao(id),
    CHECK(fator IN ('formacao','funcional','producao')),
    CHECK(item_negociado IN (0,1)),
    CHECK(possui_potencial_nao_explorado IN (0,1)),
    CHECK(pontuacao_estimada IS NULL OR pontuacao_estimada >= 0),
    CHECK(pontuacao_confirmada IS NULL OR pontuacao_confirmada >= 0)
);

CREATE TABLE IF NOT EXISTS evidencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    atividade_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    nome_arquivo TEXT,
    caminho_arquivo TEXT,
    descricao TEXT,
    data_anexacao DATETIME NOT NULL,
    validade_status TEXT,
    data_validade DATE,
    obrigatoria INTEGER NOT NULL DEFAULT 0,
    aprovada INTEGER NOT NULL DEFAULT 0,
    observacoes TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    deleted_at DATETIME,
    FOREIGN KEY (atividade_id) REFERENCES atividades(id),
    CHECK(tipo IN ('certificado','portaria','ata','email','declaracao','pdf','imagem','link','material_didatico','print','outro')),
    CHECK(obrigatoria IN (0,1)),
    CHECK(aprovada IN (0,1))
);

CREATE TABLE IF NOT EXISTS checkins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ano_id INTEGER NOT NULL,
    fator TEXT,
    data_checkin DATE NOT NULL,
    pontuacao_acumulada REAL,
    status_risco TEXT,
    atividades_pendentes INTEGER,
    nota TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (ano_id) REFERENCES anos_avaliacao(id),
    CHECK(status_risco IN ('baixo','medio','alto'))
);

CREATE TABLE IF NOT EXISTS alertas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ano_id INTEGER NOT NULL,
    atividade_id INTEGER,
    fator TEXT,
    tipo_alerta TEXT NOT NULL,
    severidade TEXT NOT NULL,
    mensagem TEXT NOT NULL,
    recomendacao TEXT,
    resolvido INTEGER NOT NULL DEFAULT 0,
    resolvido_em DATETIME,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (ano_id) REFERENCES anos_avaliacao(id),
    FOREIGN KEY (atividade_id) REFERENCES atividades(id),
    CHECK(severidade IN ('baixa','media','alta')),
    CHECK(resolvido IN (0,1))
);

CREATE TABLE IF NOT EXISTS sugestoes_chatgpt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ano_id INTEGER NOT NULL,
    atividade_id INTEGER,
    fator TEXT,
    tipo_sugestao TEXT NOT NULL,
    titulo TEXT NOT NULL,
    texto TEXT NOT NULL,
    indicador_sugerido TEXT,
    evidencias_sugeridas TEXT,
    acao_recomendada TEXT,
    origem_contexto TEXT,
    aplicada_pelo_usuario INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (ano_id) REFERENCES anos_avaliacao(id),
    FOREIGN KEY (atividade_id) REFERENCES atividades(id),
    CHECK(aplicada_pelo_usuario IN (0,1))
);

CREATE TABLE IF NOT EXISTS configuracoes_usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chave TEXT NOT NULL UNIQUE,
    valor TEXT,
    descricao TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_atividades_ano ON atividades(ano_id);
CREATE INDEX IF NOT EXISTS idx_atividades_fator ON atividades(fator);
CREATE INDEX IF NOT EXISTS idx_atividades_status ON atividades(status);
CREATE INDEX IF NOT EXISTS idx_atividades_regra ON atividades(regra_id);
CREATE INDEX IF NOT EXISTS idx_evidencias_atividade ON evidencias(atividade_id);
CREATE INDEX IF NOT EXISTS idx_alertas_ano ON alertas(ano_id);
CREATE INDEX IF NOT EXISTS idx_alertas_resolvido ON alertas(resolvido);
CREATE INDEX IF NOT EXISTS idx_alertas_tipo ON alertas(tipo_alerta);
CREATE INDEX IF NOT EXISTS idx_chatgpt_ano ON sugestoes_chatgpt(ano_id);
CREATE INDEX IF NOT EXISTS idx_chatgpt_tipo ON sugestoes_chatgpt(tipo_sugestao);
