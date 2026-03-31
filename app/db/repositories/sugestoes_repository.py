from datetime import datetime
import sqlite3
from typing import List


def list_by_ano(conn: sqlite3.Connection, ano_id: int) -> List[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM sugestoes_chatgpt WHERE ano_id = ? ORDER BY created_at DESC", (ano_id,)
    ).fetchall()


def create(conn: sqlite3.Connection, data: dict) -> int:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "created_at": now,
        **data,
    }
    cols = ", ".join(payload.keys())
    placeholders = ", ".join(["?"] * len(payload))
    with conn:
        cur = conn.execute(
            f"INSERT INTO sugestoes_chatgpt ({cols}) VALUES ({placeholders})",
            tuple(payload.values()),
        )
    return cur.lastrowid
