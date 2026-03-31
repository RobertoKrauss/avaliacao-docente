from datetime import datetime

from app.db.connection import get_connection
from app.db.seed import bootstrap_database
from app.db.repositories import (
    anos_repository,
    atividades_repository,
    evidencias_repository,
    regras_repository,
)


def main():
    bootstrap_database()
    conn = get_connection()
    ano = anos_repository.get_or_create_current_year(conn)["id"]

    with conn:
        conn.execute("DELETE FROM evidencias")
        conn.execute("DELETE FROM atividades")

    now = datetime.utcnow()

    def regra_por_fator(fator):
        return conn.execute(
            "SELECT id FROM regras_pontuacao WHERE categoria_principal = ? ORDER BY id LIMIT 1",
            (fator,),
        ).fetchone()["id"]

    atividades_repository.create(
        conn,
        {
            "ano_id": ano,
            "titulo": "Curso de atualização X",
            "data_atividade": now.strftime("%Y-%m-%d"),
            "fator": "formacao",
            "regra_id": regra_por_fator("formacao"),
            "quantidade": 2,
            "status": "registrada",
        },
    )

    atividades_repository.create(
        conn,
        {
            "ano_id": ano,
            "titulo": "Software didático Y",
            "data_atividade": now.strftime("%Y-%m-%d"),
            "fator": "funcional",
            "regra_id": regra_por_fator("funcional"),
            "quantidade": 1,
            "status": "registrada",
        },
    )

    prod_id = atividades_repository.create(
        conn,
        {
            "ano_id": ano,
            "titulo": "Organização de evento UTFPR",
            "data_atividade": now.strftime("%Y-%m-%d"),
            "fator": "producao",
            "regra_id": regra_por_fator("producao"),
            "quantidade": 1,
            "status": "registrada",
        },
    )

    evidencias_repository.create(
        conn,
        {
            "atividade_id": prod_id,
            "tipo": "certificado",
            "data_anexacao": now.strftime("%Y-%m-%d %H:%M:%S"),
            "descricao": "Certificado do evento",
        },
    )
    conn.close()
    print("Dados de exemplo carregados.")


if __name__ == "__main__":
    main()
