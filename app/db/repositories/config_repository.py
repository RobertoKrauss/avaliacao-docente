import sqlite3
from datetime import datetime
from typing import Optional


def get(conn: sqlite3.Connection, chave: str) -> Optional[str]:
    row = conn.execute("SELECT valor FROM configuracoes_usuario WHERE chave = ?", (chave,)).fetchone()
    return row["valor"] if row else None


def set(conn: sqlite3.Connection, chave: str, valor: str) -> None:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    exists = conn.execute("SELECT 1 FROM configuracoes_usuario WHERE chave = ?", (chave,)).fetchone()
    if exists:
        with conn:
            conn.execute(
                "UPDATE configuracoes_usuario SET valor = ?, updated_at = ? WHERE chave = ?",
                (valor, now, chave),
            )
    else:
        with conn:
            conn.execute(
                "INSERT INTO configuracoes_usuario (chave, valor, created_at, updated_at) VALUES (?,?,?,?)",
                (chave, valor, now, now),
            )
