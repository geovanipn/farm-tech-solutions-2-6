from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from src.models.field import Field
from src.models.harvester import Harvester
from src.models.harvest_record import HarvestRecord
from src.services.field_service import create_field, list_fields, get_field_by_id
from src.services.harvester_service import create_harvester, list_harvesters
from src.services.harvest_service import create_record, list_records, group_by_harvester, group_by_field


def test_create_field_calls_execute(mock_conn):
    cur = mock_conn.cursor.return_value.__enter__.return_value
    id_var_mock = MagicMock()
    id_var_mock.getvalue.return_value = [10]
    cur.var.return_value = id_var_mock

    field = create_field(mock_conn, "Talhão X", 100.0, "RB867515", date(2023, 1, 1))

    cur.execute.assert_called_once()
    call_args = cur.execute.call_args
    sql = call_args[0][0]
    params = call_args[0][1]
    assert "INSERT INTO field" in sql
    assert params["name"] == "Talhão X"
    assert params["area_ha"] == 100.0
    assert field.id == 10
    assert field.name == "Talhão X"


def test_list_fields_returns_objects(mock_conn):
    cur = mock_conn.cursor.return_value.__enter__.return_value
    cur.fetchall.return_value = [
        (1, "Talhão A", 50.0, "RB867515", date(2023, 4, 1)),
        (2, "Talhão B", 30.0, "CTC4", None),
    ]

    fields = list_fields(mock_conn)

    assert len(fields) == 2
    assert isinstance(fields[0], Field)
    assert fields[0].id == 1
    assert fields[0].name == "Talhão A"
    assert fields[1].id == 2
    assert fields[1].variety == "CTC4"


def test_get_field_by_id_found(mock_conn):
    cur = mock_conn.cursor.return_value.__enter__.return_value
    cur.fetchone.return_value = (5, "Talhão C", 75.0, "SP80-3280", date(2022, 5, 10))

    field = get_field_by_id(mock_conn, 5)

    assert field is not None
    assert field.id == 5
    assert field.name == "Talhão C"
    assert field.area_ha == 75.0


def test_get_field_by_id_not_found(mock_conn):
    cur = mock_conn.cursor.return_value.__enter__.return_value
    cur.fetchone.return_value = None

    field = get_field_by_id(mock_conn, 999)

    assert field is None


def test_create_harvester(mock_conn):
    cur = mock_conn.cursor.return_value.__enter__.return_value
    id_var_mock = MagicMock()
    id_var_mock.getvalue.return_value = [7]
    cur.var.return_value = id_var_mock

    harvester = create_harvester(mock_conn, "COL-05", "John Deere X9")

    cur.execute.assert_called_once()
    call_args = cur.execute.call_args
    sql = call_args[0][0]
    params = call_args[0][1]
    assert "INSERT INTO harvester" in sql
    assert params["code"] == "COL-05"
    assert params["model"] == "John Deere X9"
    assert harvester.id == 7
    assert harvester.code == "COL-05"


def test_list_harvesters(mock_conn):
    cur = mock_conn.cursor.return_value.__enter__.return_value
    cur.fetchall.return_value = [
        (1, "COL-01", "Case IH A8800"),
        (2, "COL-02", "John Deere X9"),
    ]

    harvesters = list_harvesters(mock_conn)

    assert len(harvesters) == 2
    assert isinstance(harvesters[0], Harvester)
    assert harvesters[0].code == "COL-01"
    assert harvesters[1].model == "John Deere X9"


def test_create_record_persists_losses(mock_conn):
    cur = mock_conn.cursor.return_value.__enter__.return_value
    id_var_mock = MagicMock()
    id_var_mock.getvalue.return_value = [15]
    cur.var.return_value = id_var_mock

    record = HarvestRecord(
        field_id=1, harvester_id=1,
        field_name="Talhão A", harvester_code="COL-01",
        operator_name="João Silva",
        harvest_date=date(2024, 8, 15),
        estimated_yield_ton=200.0,
        loss_pct=12.0,
        ton_price_brl=120.0,
    )

    result = create_record(mock_conn, record)

    cur.execute.assert_called_once()
    call_args = cur.execute.call_args
    params = call_args[0][1]
    assert params["loss_ton"] == 24.0
    assert params["loss_brl"] == 2880.0
    assert result.id == 15


def test_list_records_returns_objects(mock_conn):
    cur = mock_conn.cursor.return_value.__enter__.return_value
    cur.fetchall.return_value = [
        (1, 1, 1, "Talhão A", "COL-01", "João Silva",
         date(2024, 8, 15), 200.0, 12.0, 120.0, 24.0, 2880.0),
    ]

    records = list_records(mock_conn)

    assert len(records) == 1
    assert isinstance(records[0], HarvestRecord)
    assert records[0].field_name == "Talhão A"
    assert records[0].harvester_code == "COL-01"
    assert records[0].loss_ton == 24.0


def test_group_by_harvester():
    def _rec(harvester_code, field_name="F"):
        r = HarvestRecord(
            field_id=1, harvester_id=1,
            field_name=field_name, harvester_code=harvester_code,
            operator_name="Op", harvest_date=date(2024, 1, 1),
            estimated_yield_ton=100.0, loss_pct=5.0, ton_price_brl=100.0,
        )
        r.calculate_losses()
        return r

    records = [_rec("COL-01"), _rec("COL-02"), _rec("COL-01")]
    groups = group_by_harvester(records)

    assert len(groups) == 2
    assert len(groups["COL-01"]) == 2
    assert len(groups["COL-02"]) == 1


def test_group_by_field():
    def _rec(field_name, harvester_code="COL-01"):
        r = HarvestRecord(
            field_id=1, harvester_id=1,
            field_name=field_name, harvester_code=harvester_code,
            operator_name="Op", harvest_date=date(2024, 1, 1),
            estimated_yield_ton=100.0, loss_pct=5.0, ton_price_brl=100.0,
        )
        r.calculate_losses()
        return r

    records = [_rec("Talhão A"), _rec("Talhão B"), _rec("Talhão A")]
    groups = group_by_field(records)

    assert len(groups) == 2
    assert len(groups["Talhão A"]) == 2
    assert len(groups["Talhão B"]) == 1
