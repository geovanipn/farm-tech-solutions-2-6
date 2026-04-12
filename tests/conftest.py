from datetime import date
from unittest.mock import MagicMock

import pytest

from src.models.field import Field
from src.models.harvester import Harvester
from src.models.harvest_record import HarvestRecord


@pytest.fixture
def mock_conn():
    """MagicMock simulando conexão Oracle com cursor."""
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value.__enter__ = MagicMock(return_value=cursor)
    conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
    return conn


@pytest.fixture
def tmp_json(tmp_path):
    """Caminho para arquivo JSON temporário."""
    return str(tmp_path / "test_records.json")


@pytest.fixture
def sample_field():
    return Field(id=1, name="Talhão A", area_ha=50.0,
                 variety="RB867515", plant_date=date(2023, 4, 1))


@pytest.fixture
def sample_harvester():
    return Harvester(id=1, code="COL-01", model="Case IH A8800")


@pytest.fixture
def sample_record(sample_field, sample_harvester):
    r = HarvestRecord(
        field_id=1, harvester_id=1,
        field_name="Talhão A", harvester_code="COL-01",
        operator_name="João Silva",
        harvest_date=date(2024, 8, 15),
        estimated_yield_ton=200.0,
        loss_pct=12.0,
        ton_price_brl=120.0
    )
    r.calculate_losses()
    return r
