import csv
import io
import sqlite3
import zipfile
import streamlit as st
from typing import List

from app.ui.theme import apply_theme
from app.db.connection import get_connection


IGNORED_TABLES = {"sqlite_sequence"}


def list_tables(conn: sqlite3.Connection) -> List[str]:
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()
    return [r[0] for r in rows if r[0] not in IGNORED_TABLES]


def export_zip(conn: sqlite3.Connection) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for table in list_tables(conn):
            rows = conn.execute(f"SELECT * FROM {table}").fetchall()
            cols = [c[0] for c in conn.execute(f"PRAGMA table_info({table})").fetchall()]
            csv_buf = io.StringIO()
            writer = csv.DictWriter(csv_buf, fieldnames=cols)
            writer.writeheader()
            for r in rows:
                writer.writerow({k: r[k] for k in cols})
            zf.writestr(f"{table}.csv", csv_buf.getvalue())
    buf.seek(0)
    return buf.read()


def import_csv_zip(conn: sqlite3.Connection, zip_bytes: bytes, mode: str = "merge"):
    """
    mode = 'merge' -> INSERT OR REPLACE
    mode = 'overwrite' -> DELETE + INSERT
    """
    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zf:
        table_files = [n for n in zf.namelist() if n.endswith(".csv")]
        if mode == "overwrite":
            for table_file in table_files:
                table = table_file.replace(".csv", "")
                conn.execute(f"DELETE FROM {table}")
        for table_file in table_files:
            table = table_file.replace(".csv", "")
            cols_info = conn.execute(f"PRAGMA table_info({table})").fetchall()
            colnames = [c[1] for c in cols_info]
            with zf.open(table_file) as f:
                text = io.TextIOWrapper(f, encoding="utf-8")
                reader = csv.DictReader(text)
                for row in reader:
                    payload = {k: row.get(k) for k in colnames}
                    placeholders = ",".join(["?"] * len(payload))
                    cols_sql = ",".join(colnames)
                    if mode == "merge":
                        conn.execute(
                            f"INSERT OR REPLACE INTO {table} ({cols_sql}) VALUES ({placeholders})",
                            tuple(payload.values()),
                        )
                    else:
                        conn.execute(
                            f"INSERT INTO {table} ({cols_sql}) VALUES ({placeholders})",
                            tuple(payload.values()),
                        )
        conn.commit()


def import_export_page():
    apply_theme()
    st.title("Importar / Exportar CSV")
    conn = get_connection()

    st.subheader("Exportar base inteira (CSV)")
    if st.button("Gerar ZIP com CSVs"):
        data = export_zip(conn)
        st.download_button(
            "Baixar export.zip",
            data=data,
            file_name="export.zip",
            mime="application/zip",
        )

    st.markdown("---")
    st.subheader("Importar CSVs")
    modo = st.radio(
        "Modo de importação",
        ["merge", "overwrite"],
        format_func=lambda x: "Mesclar (merge)" if x == "merge" else "Sobrescrever tudo",
    )
    uploaded = st.file_uploader(
        "Envie um ZIP contendo um CSV por tabela (nome_do_arquivo = nome_da_tabela.csv)",
        type=["zip"],
    )
    if uploaded and st.button("Importar agora"):
        try:
            import_csv_zip(conn, uploaded.read(), mode=modo)
            st.success("Importação concluída.")
        except Exception as e:
            st.error(f"Erro na importação: {e}")

    st.caption("Formato esperado: um ZIP contendo arquivos .csv com cabeçalhos idênticos aos nomes de colunas das tabelas.")
    conn.close()


if __name__ == "__main__":
    import_export_page()
