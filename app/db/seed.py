from datetime import datetime
from pathlib import Path
import sqlite3

from app.db.connection import get_connection, DB_PATH

SCHEMA_FILE = Path(__file__).resolve().parent / "schema.sql"


def bootstrap_database(db_path: Path = DB_PATH) -> None:
    conn = get_connection(db_path)
    with conn:
        conn.executescript(SCHEMA_FILE.read_text(encoding="utf-8"))
    seed_basics(conn)
    conn.close()


def seed_basics(conn: sqlite3.Connection) -> None:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    year = datetime.utcnow().year
    with conn:
        conn.execute(
            """
            INSERT INTO anos_avaliacao (ano, descricao, created_at, updated_at)
            SELECT ?, ?, ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM anos_avaliacao WHERE ano = ?)
            """,
            (year, f"Avaliação {year}", now, now, year),
        )
        conn.execute(
            """
            INSERT INTO configuracoes_usuario (chave, valor, descricao, created_at, updated_at)
            SELECT 'usar_perfil_chatgpt', 'false', 'Controle de uso do perfil de escrita', ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM configuracoes_usuario WHERE chave = 'usar_perfil_chatgpt')
            """,
            (now, now),
        )
        seed_regras_padrao(conn, now)


def seed_regras_padrao(conn: sqlite3.Connection, now: str) -> None:
    regras = [
        # Formação / Atualização Continuada
        ("Participação em palestras, seminários e eventos com certificado", "formacao", "evento", "padrao", "2 pontos por evento", "por_unidade", 2, "evento", None, None, 0),
        ("Participação em congressos com certificado", "formacao", "evento", "padrao", "5 pontos por evento", "por_unidade", 5, "evento", None, None, 0),
        ("Cursos de atualização e/ou estágios", "formacao", "curso", "padrao", "5 pontos a cada 10h", "por_hora", 5, "hora", 10, None, 0),
        ("Exercício de atividade profissional externa correlata", "formacao", "atividade_profissional", "padrao", "5 pontos a cada 10h", "por_hora", 5, "hora", 10, None, 0),
        ("Curso de especialização", "formacao", "especializacao", "padrao", "15 pontos fixos", "fixo", 15, None, None, 15, 0),
        ("Mestrado ou doutorado", "formacao", "pos", "padrao", "15 pontos fixos", "fixo", 15, None, None, 15, 0),
        ("Banca de estágio supervisionado", "formacao", "banca", "padrao", "3 pontos fixos", "fixo", 3, None, None, None, 0),
        ("Banca de monografia ou TCC", "formacao", "banca", "padrao", "5 pontos fixos", "fixo", 5, None, None, None, 0),
        ("Banca de dissertação de mestrado", "formacao", "banca", "padrao", "10 pontos fixos", "fixo", 10, None, None, None, 0),
        ("Banca de tese de doutorado", "formacao", "banca", "padrao", "15 pontos fixos", "fixo", 15, None, None, None, 0),
        ("Atualização de legislações vigentes para chefias", "formacao", "legislacao", "padrao", "15 pontos fixos", "fixo", 15, None, None, None, 0),
        # Funcional – Pedagógico
        ("Orientação de estágio supervisionado", "funcional", "orientacao", "padrao", "10 pontos por orientado", "por_unidade", 10, "orientado", None, None, 0),
        ("Orientação de TCC", "funcional", "orientacao", "padrao", "20 pontos por trabalho", "por_unidade", 20, "trabalho", None, None, 0),
        ("Orientação de mestrado", "funcional", "orientacao", "padrao", "30 pontos fixos", "fixo", 30, None, None, None, 0),
        ("Orientação de doutorado", "funcional", "orientacao", "padrao", "35 pontos fixos", "fixo", 35, None, None, None, 0),
        ("Orientação de iniciação científica da UTFPR", "funcional", "orientacao", "padrao", "20 pontos fixos", "fixo", 20, None, None, None, 0),
        ("Orientação de bolsista de desenvolvimento científico regional / recém-doutor / pós-doc", "funcional", "orientacao", "padrao", "20 pontos fixos", "fixo", 20, None, None, None, 0),
        ("Orientação de bolsista mestre/doutor em projeto institucional", "funcional", "orientacao", "padrao", "20 pontos fixos", "fixo", 20, None, None, None, 0),
        ("Coorientação de iniciação científica", "funcional", "coorientacao", "padrao", "10 pontos fixos", "fixo", 10, None, None, None, 0),
        ("Coorientação de mestrado", "funcional", "coorientacao", "padrao", "10 pontos fixos", "fixo", 10, None, None, None, 0),
        ("Coorientação de doutorado", "funcional", "coorientacao", "padrao", "10 pontos fixos", "fixo", 10, None, None, None, 0),
        ("Desenvolvimento de software didático", "funcional", "software", "padrao", "35 pontos fixos", "fixo", 35, None, None, None, 0),
        ("Autoria de livro técnico/científico", "funcional", "livro", "padrao", "35 pontos por livro", "por_unidade", 35, "livro", None, None, 0),
        ("Autoria de capítulo de livro técnico/científico", "funcional", "capitulo", "padrao", "20 pontos por capítulo", "por_unidade", 20, "capitulo", None, None, 0),
        ("Organização/edição de livro ou anais científicos", "funcional", "organizacao", "padrao", "35 pontos por livro", "por_unidade", 35, "livro", None, None, 0),
        ("Tradução de livro técnico/científico", "funcional", "traducao", "padrao", "30 pontos por livro", "por_unidade", 30, "livro", None, None, 0),
        ("Editor-chefe de revista científica internacional", "funcional", "revista", "padrao", "10 pontos fixos", "fixo", 10, None, None, None, 0),
        ("Editor associado de revista científica nacional", "funcional", "revista", "padrao", "5 pontos fixos", "fixo", 5, None, None, None, 0),
        ("Conselho científico/editorial de revista internacional", "funcional", "revista", "padrao", "5 pontos fixos", "fixo", 5, None, None, None, 0),
        ("Conselho científico/editorial de revista nacional", "funcional", "revista", "padrao", "3 pontos fixos", "fixo", 3, None, None, None, 0),
        ("Participação em reunião de departamento", "funcional", "reuniao", "padrao", "valor manual entre 0 e 10", "manual", None, None, None, 10, 1),
        ("Entrega de documentação acadêmica no prazo", "funcional", "documentacao", "padrao", "valor manual entre 0 e 10", "manual", None, None, None, 10, 1),
        # Produção Institucional
        ("Cargo nomeado por portaria", "producao", "cargo", "padrao", "10 pontos fixos", "fixo", 10, None, None, None, 0),
        ("Chefia de grupo de disciplinas", "producao", "chefia", "padrao", "10 pontos fixos", "fixo", 10, None, None, None, 0),
        ("Presidência de comissão por portaria", "producao", "comissao", "padrao", "5 pontos fixos", "fixo", 5, None, None, None, 0),
        ("Membro de comissão por portaria", "producao", "comissao", "padrao", "5 pontos fixos", "fixo", 5, None, None, None, 0),
        ("Membro de banca de concurso público", "producao", "banca", "padrao", "5 pontos fixos", "fixo", 5, None, None, None, 0),
        ("Membro de banca de teste seletivo", "producao", "banca", "padrao", "5 pontos fixos", "fixo", 5, None, None, None, 0),
        ("Participação em conselho departamental ou colegiado", "producao", "colegiado", "padrao", "5 pontos fixos", "fixo", 5, None, None, None, 0),
        ("Organização de evento da UTFPR", "producao", "evento", "padrao", "10 pontos por atividade", "por_unidade", 10, "atividade", None, None, 0),
        ("Responsável por laboratório", "producao", "laboratorio", "padrao", "10 pontos fixos", "fixo", 10, None, None, None, 0),
        ("Responsável por atividades complementares", "producao", "atividades_complementares", "padrao", "10 pontos fixos", "fixo", 10, None, None, None, 0),
        ("Responsável pela orientação de estágio", "producao", "estagio", "padrao", "10 pontos fixos", "fixo", 10, None, None, None, 0),
        ("Responsável pelo trabalho de diplomação", "producao", "trabalho_diplomacao", "padrao", "10 pontos fixos", "fixo", 10, None, None, None, 0),
        ("Assessor de coordenação", "producao", "assessor", "padrao", "10 pontos fixos", "fixo", 10, None, None, None, 0),
        ("Participação em evento representando a instituição / apresentando trabalho / palestrando em evento nacional", "producao", "evento", "padrao", "10 pontos por participação", "por_unidade", 10, "participacao", None, None, 0),
    ]

    for nome, categoria, subtipo, origem, descricao, tipo, valor, unidade, divisor, teto, exige_manual in regras:
        conn.execute(
            """
            INSERT INTO regras_pontuacao (
                nome, categoria_principal, subtipo, origem, descricao_regra, tipo_formula,
                valor_base, unidade, divisor_unidade, pontuacao_maxima,
                exige_valor_manual, evidencia_necessaria, origem_documento, ativa, observacoes,
                created_at, updated_at
            )
            SELECT ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            WHERE NOT EXISTS (
                SELECT 1 FROM regras_pontuacao
                WHERE nome = ? AND categoria_principal = ? AND subtipo IS ?
            )
            """,
            (
                nome,
                categoria,
                subtipo,
                origem,
                descricao,
                tipo,
                valor,
                unidade,
                divisor,
                teto,
                exige_manual,
                None,
                origem,
                1,
                None,
                now,
                now,
                nome,
                categoria,
                subtipo,
            ),
        )


if __name__ == "__main__":
    bootstrap_database()
    print(f"Banco inicial criado em {DB_PATH}")
