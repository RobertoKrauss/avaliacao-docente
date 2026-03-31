from datetime import datetime
import sqlite3
from typing import List, Optional


def list_by_ano(conn: sqlite3.Connection, ano_id: int) -> List[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM alertas WHERE ano_id = ? ORDER BY created_at DESC", (ano_id,)
    ).fetchall()


def list_filtered(
    conn: sqlite3.Connection,
    ano_id: int,
    fator: str = None,
    tipo: str = None,
    severidade: str = None,
    resolvido: int = None,
) -> List[sqlite3.Row]:
    query = "SELECT * FROM alertas WHERE ano_id = ?"
    params = [ano_id]
    if fator and fator != "todos":
        query += " AND fator = ?"
        params.append(fator)
    if tipo and tipo != "todos":
        query += " AND tipo_alerta = ?"
        params.append(tipo)
    if severidade and severidade != "todos":
        query += " AND severidade = ?"
        params.append(severidade)
    if resolvido is not None:
        query += " AND resolvido = ?"
        params.append(resolvido)
    query += " ORDER BY created_at DESC"
    return conn.execute(query, tuple(params)).fetchall()


def create_alert(
    conn: sqlite3.Connection,
    ano_id: int,
    tipo_alerta: str,
    severidade: str,
    mensagem: str,
    recomendacao: str = "",
    atividade_id: Optional[int] = None,
    fator: Optional[str] = None,
) -> int:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with conn:
        cur = conn.execute(
            """
            INSERT INTO alertas (ano_id, atividade_id, fator, tipo_alerta, severidade, mensagem, recomendacao, resolvido, created_at, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)
            """,
            (ano_id, atividade_id, fator, tipo_alerta, severidade, mensagem, recomendacao, 0, now, now),
        )
    return cur.lastrowid


def resolver(conn: sqlite3.Connection, alerta_id: int) -> None:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with conn:
        conn.execute(
            "UPDATE alertas SET resolvido = 1, resolvido_em = ?, updated_at = ? WHERE id = ?",
            (now, now, alerta_id),
        )
