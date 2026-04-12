import datetime

import oracledb

from src.models.harvest_record import HarvestRecord


def create_record(conn, record: HarvestRecord) -> HarvestRecord:
    record.calculate_losses()
    with conn.cursor() as cur:
        id_var = cur.var(int)
        cur.execute(
            """
            INSERT INTO harvest_record (
                field_id, harvester_id, operator_name, harvest_date,
                estimated_yield_ton, loss_pct, ton_price_brl, loss_ton, loss_brl
            ) VALUES (
                :field_id, :harvester_id, :operator_name, :harvest_date,
                :estimated_yield_ton, :loss_pct, :ton_price_brl, :loss_ton, :loss_brl
            )
            RETURNING id INTO :id
            """,
            {
                "field_id": record.field_id,
                "harvester_id": record.harvester_id,
                "operator_name": record.operator_name,
                "harvest_date": record.harvest_date,
                "estimated_yield_ton": record.estimated_yield_ton,
                "loss_pct": record.loss_pct,
                "ton_price_brl": record.ton_price_brl,
                "loss_ton": record.loss_ton,
                "loss_brl": record.loss_brl,
                "id": id_var,
            },
        )
        conn.commit()
        record.id = id_var.getvalue()[0]
    return record


def list_records(conn) -> list[HarvestRecord]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                hr.id,
                hr.field_id,
                hr.harvester_id,
                f.name        AS field_name,
                h.code        AS harvester_code,
                hr.operator_name,
                hr.harvest_date,
                hr.estimated_yield_ton,
                hr.loss_pct,
                hr.ton_price_brl,
                hr.loss_ton,
                hr.loss_brl
            FROM harvest_record hr
            JOIN field     f ON f.id = hr.field_id
            JOIN harvester h ON h.id = hr.harvester_id
            ORDER BY hr.harvest_date DESC
            """
        )
        rows = cur.fetchall()
    return [
        HarvestRecord(
            id=row[0],
            field_id=row[1],
            harvester_id=row[2],
            field_name=row[3],
            harvester_code=row[4],
            operator_name=row[5],
            harvest_date=row[6] if isinstance(row[6], datetime.date) else row[6].date(),
            estimated_yield_ton=row[7],
            loss_pct=row[8],
            ton_price_brl=row[9],
            loss_ton=row[10],
            loss_brl=row[11],
        )
        for row in rows
    ]


def group_by_harvester(records: list[HarvestRecord]) -> dict[str, list[HarvestRecord]]:
    result: dict[str, list[HarvestRecord]] = {}
    for record in records:
        result.setdefault(record.harvester_code, []).append(record)
    return result


def group_by_field(records: list[HarvestRecord]) -> dict[str, list[HarvestRecord]]:
    result: dict[str, list[HarvestRecord]] = {}
    for record in records:
        result.setdefault(record.field_name, []).append(record)
    return result
