from datetime import datetime
import sqlite3
from typing import Optional, Dict, Any, List


def get_or_create_current_year(conn: sqlite3.Connection) -> sqlite3.Row:
    year = datetime.utcnow().year
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with conn:
        conn.execute(
            """
            INSERT INTO anos_avaliacao (ano, descricao, created_at, updated_at)
            SELECT ?, ?, ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM anos_avaliacao WHERE ano = ? AND deleted_at IS NULL)
            """,
            (year, f"Avaliação {year}", now, now, year),
        )
    return conn.execute("SELECT * FROM anos_avaliacao WHERE ano = ? AND deleted_at IS NULL", (year,)).fetchone()


def get_by_id(conn: sqlite3.Connection, ano_id: int) -> Optional[sqlite3.Row]:
    return conn.execute("SELECT * FROM anos_avaliacao WHERE id = ? AND deleted_at IS NULL", (ano_id,)).fetchone()


def list_all(conn: sqlite3.Connection) -> List[sqlite3.Row]:
    return conn.execute("SELECT * FROM anos_avaliacao WHERE deleted_at IS NULL ORDER BY ano DESC").fetchall()


def create(conn: sqlite3.Connection, ano: int, descricao: Optional[str] = None) -> int:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with conn:
        cur = conn.execute(
            """
            INSERT INTO anos_avaliacao (ano, descricao, created_at, updated_at)
            VALUES (?,?,?,?)
            """,
            (ano, descricao or f"Avaliação {ano}", now, now),
        )
    return cur.lastrowid


def update_metas(conn: sqlite3.Connection, ano_id: int, metas: Dict[str, float]) -> None:
    campos = {k: metas[k] for k in ("meta_formacao", "meta_funcional", "meta_producao") if k in metas}
    if not campos:
        return
    campos["updated_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    sets = ", ".join([f"{k} = ?" for k in campos.keys()])
    params = list(campos.values()) + [ano_id]
    with conn:
        conn.execute(f"UPDATE anos_avaliacao SET {sets} WHERE id = ?", params)


def marcar_ultima_revisao(conn: sqlite3.Connection, ano_id: int, data: str) -> None:
    with conn:
        conn.execute(
            "UPDATE anos_avaliacao SET ultima_revisao = ?, updated_at = ? WHERE id = ?",
            (data, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), ano_id),
        )
