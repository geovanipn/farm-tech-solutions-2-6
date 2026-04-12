import os
from datetime import date
from unittest.mock import patch

import pytest

from src.models.harvest_record import HarvestRecord
from src.reports.report import (
    report_by_harvester,
    report_by_field,
    report_by_operator,
    summary_report,
)


def _make_record(field_name, harvester_code, operator_name, loss_pct,
                 yield_ton=200.0, price=120.0, field_id=1, harvester_id=1):
    r = HarvestRecord(
        field_id=field_id, harvester_id=harvester_id,
        field_name=field_name, harvester_code=harvester_code,
        operator_name=operator_name,
        harvest_date=date(2024, 8, 15),
        estimated_yield_ton=yield_ton,
        loss_pct=loss_pct,
        ton_price_brl=price,
    )
    r.calculate_losses()
    return r


@pytest.fixture
def records():
    return [
        _make_record("Talhão A", "COL-01", "João Silva", 12.0),
        _make_record("Talhão A", "COL-01", "João Silva", 8.0),
        _make_record("Talhão B", "COL-02", "Maria Souza", 5.0),
    ]


def test_report_by_harvester_contains_header(records, tmp_path):
    result = report_by_harvester(records, export_dir=str(tmp_path))
    assert "Colhedora" in result


def test_report_by_harvester_aggregates_loss(records, tmp_path):
    result = report_by_harvester(records, export_dir=str(tmp_path))
    # COL-01: 2 records with loss_ton=24.0 and 16.0 → total 40.0
    # tabulate may display "40" or "40.00" depending on version
    assert "40" in result and "COL-01" in result


def test_report_by_field_area(records, tmp_path):
    result = report_by_field(records, export_dir=str(tmp_path))
    assert "Talhão A" in result
    assert "Talhão B" in result


def test_report_by_operator_count(records, tmp_path):
    result = report_by_operator(records, export_dir=str(tmp_path))
    assert "João Silva" in result
    assert "Maria Souza" in result


def test_summary_report_totals(records, tmp_path):
    result = summary_report(records, export_dir=str(tmp_path))
    # 3 records total
    assert "3" in result
    # total yield = 200*3 = 600
    assert "600.00" in result


def test_alert_triggered_above_10_pct(tmp_path):
    record = _make_record("Talhão A", "COL-01", "João", 12.0)
    with patch("src.reports.report.print_alert") as mock_alert:
        report_by_harvester([record], export_dir=str(tmp_path))
        mock_alert.assert_called_once()


def test_no_alert_below_threshold(tmp_path):
    record = _make_record("Talhão A", "COL-01", "João", 8.0)
    with patch("src.reports.report.print_alert") as mock_alert:
        report_by_harvester([record], export_dir=str(tmp_path))
        mock_alert.assert_not_called()


def test_report_exports_txt_file(records, tmp_path):
    report_by_harvester(records, export_dir=str(tmp_path))
    txt_path = tmp_path / "relatorio_colhedora.txt"
    assert txt_path.exists()
