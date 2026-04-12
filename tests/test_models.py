from datetime import date

from src.models.field import Field
from src.models.harvester import Harvester
from src.models.harvest_record import HarvestRecord


def test_field_to_dict(sample_field):
    d = sample_field.to_dict()
    assert d["id"] == 1
    assert d["name"] == "Talhão A"
    assert d["area_ha"] == 50.0
    assert d["variety"] == "RB867515"
    assert d["plant_date"] == "2023-04-01"


def test_field_from_dict():
    data = {"id": 2, "name": "Talhão B", "area_ha": 30.0,
            "variety": "CTC4", "plant_date": "2022-06-15"}
    f = Field.from_dict(data)
    assert f.id == 2
    assert f.name == "Talhão B"
    assert f.area_ha == 30.0
    assert f.variety == "CTC4"
    assert f.plant_date == date(2022, 6, 15)


def test_harvester_to_dict(sample_harvester):
    d = sample_harvester.to_dict()
    assert d["id"] == 1
    assert d["code"] == "COL-01"
    assert d["model"] == "Case IH A8800"


def test_harvester_from_dict():
    data = {"id": 3, "code": "COL-02", "model": "John Deere X9"}
    h = Harvester.from_dict(data)
    assert h.id == 3
    assert h.code == "COL-02"
    assert h.model == "John Deere X9"


def test_harvest_record_to_dict(sample_record):
    d = sample_record.to_dict()
    assert d["field_id"] == 1
    assert d["harvester_id"] == 1
    assert d["field_name"] == "Talhão A"
    assert d["harvester_code"] == "COL-01"
    assert d["operator_name"] == "João Silva"
    assert d["harvest_date"] == "2024-08-15"
    assert d["estimated_yield_ton"] == 200.0
    assert d["loss_pct"] == 12.0
    assert d["ton_price_brl"] == 120.0
    assert d["loss_ton"] == 24.0
    assert d["loss_brl"] == 2880.0


def test_harvest_record_from_dict(sample_record):
    d = sample_record.to_dict()
    r2 = HarvestRecord.from_dict(d)
    assert r2.field_id == sample_record.field_id
    assert r2.harvester_id == sample_record.harvester_id
    assert r2.field_name == sample_record.field_name
    assert r2.harvester_code == sample_record.harvester_code
    assert r2.operator_name == sample_record.operator_name
    assert r2.harvest_date == sample_record.harvest_date
    assert r2.estimated_yield_ton == sample_record.estimated_yield_ton
    assert r2.loss_pct == sample_record.loss_pct
    assert r2.ton_price_brl == sample_record.ton_price_brl
    assert r2.loss_ton == sample_record.loss_ton
    assert r2.loss_brl == sample_record.loss_brl
