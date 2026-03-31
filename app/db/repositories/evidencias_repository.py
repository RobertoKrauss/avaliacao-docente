from datetime import datetime
import sqlite3
from typing import List, Dict, Any


def list_by_atividade(conn: sqlite3.Connection, atividade_id: int) -> List[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM evidencias WHERE atividade_id = ? AND deleted_at IS NULL ORDER BY data_anexacao DESC",
        (atividade_id,),
    ).fetchall()


def create(conn: sqlite3.Connection, data: Dict[str, Any]) -> int:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "created_at": now,
        "updated_at": now,
        "obrigatoria": data.get("obrigatoria", 0),
        "aprovada": data.get("aprovada", 0),
        **data,
    }
    cols = ", ".join(payload.keys())
    placeholders = ", ".join(["?"] * len(payload))
    with conn:
        cur = conn.execute(
            f"INSERT INTO evidencias ({cols}) VALUES ({placeholders})",
            tuple(payload.values()),
        )
    return cur.lastrowid


def soft_delete(conn: sqlite3.Connection, evidencia_id: int) -> None:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with conn:
        conn.execute(
            "UPDATE evidencias SET deleted_at = ?, updated_at = ? WHERE id = ?",
            (now, now, evidencia_id),
        )
