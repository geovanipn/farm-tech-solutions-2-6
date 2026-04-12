import oracledb

from src.models.harvester import Harvester


def create_harvester(conn, code: str, model: str | None) -> Harvester:
    with conn.cursor() as cur:
        id_var = cur.var(int)
        try:
            cur.execute(
                """
                INSERT INTO harvester (code, model)
                VALUES (:code, :model)
                RETURNING id INTO :id
                """,
                {"code": code, "model": model, "id": id_var},
            )
            conn.commit()
        except oracledb.IntegrityError:
            raise ValueError(
                f"Já existe uma colhedora com o código '{code}'. Use um código único."
            )
        new_id = id_var.getvalue()[0]
    return Harvester(id=new_id, code=code, model=model)


def list_harvesters(conn) -> list[Harvester]:
    with conn.cursor() as cur:
        cur.execute("SELECT id, code, model FROM harvester ORDER BY code")
        rows = cur.fetchall()
    return [Harvester(id=row[0], code=row[1], model=row[2]) for row in rows]
