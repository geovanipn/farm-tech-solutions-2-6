from datetime import date

import oracledb

from src.models.field import Field


def create_field(
    conn,
    name: str,
    area_ha: float,
    variety: str | None,
    plant_date: date | None,
) -> Field:
    with conn.cursor() as cur:
        id_var = cur.var(int)
        cur.execute(
            """
            INSERT INTO field (name, area_ha, variety, plant_date)
            VALUES (:name, :area_ha, :variety, :plant_date)
            RETURNING id INTO :id
            """,
            {
                "name": name,
                "area_ha": area_ha,
                "variety": variety,
                "plant_date": plant_date,
                "id": id_var,
            },
        )
        conn.commit()
        new_id = id_var.getvalue()[0]
    return Field(id=new_id, name=name, area_ha=area_ha, variety=variety, plant_date=plant_date)


def list_fields(conn) -> list[Field]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, area_ha, variety, plant_date FROM field ORDER BY name"
        )
        rows = cur.fetchall()
    return [
        Field(id=row[0], name=row[1], area_ha=row[2], variety=row[3], plant_date=row[4])
        for row in rows
    ]


def get_field_by_id(conn, field_id: int) -> Field | None:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, area_ha, variety, plant_date FROM field WHERE id = :id",
            {"id": field_id},
        )
        row = cur.fetchone()
    if row is None:
        return None
    return Field(id=row[0], name=row[1], area_ha=row[2], variety=row[3], plant_date=row[4])
