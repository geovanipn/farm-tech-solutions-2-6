from datetime import date

from src.models.harvest_record import HarvestRecord


def _make_record(yield_ton, loss_pct, price):
    r = HarvestRecord(
        field_id=1, harvester_id=1,
        field_name="Campo", harvester_code="COL-01",
        operator_name="Operador",
        harvest_date=date(2024, 1, 1),
        estimated_yield_ton=yield_ton,
        loss_pct=loss_pct,
        ton_price_brl=price,
    )
    return r


def test_calculate_losses_normal():
    r = _make_record(200.0, 12.0, 120.0)
    r.calculate_losses()
    assert r.loss_ton == 24.0
    assert r.loss_brl == 2880.0


def test_calculate_losses_zero_pct():
    r = _make_record(200.0, 0.0, 120.0)
    r.calculate_losses()
    assert r.loss_ton == 0.0
    assert r.loss_brl == 0.0


def test_calculate_losses_max_pct():
    r = _make_record(200.0, 15.0, 150.0)
    r.calculate_losses()
    assert r.loss_ton == 30.0
    assert r.loss_brl == 4500.0


def test_calculate_losses_precision():
    r = _make_record(100.0, 3.0, 111.11)
    r.calculate_losses()
    assert r.loss_ton == round(100.0 * 3.0 / 100, 2)
    assert r.loss_brl == round(r.loss_ton * 111.11, 2)


def test_is_high_loss_above_threshold():
    r = _make_record(100.0, 10.1, 100.0)
    assert r.is_high_loss() is True


def test_is_high_loss_at_threshold():
    r = _make_record(100.0, 10.0, 100.0)
    assert r.is_high_loss() is False


def test_is_high_loss_below_threshold():
    r = _make_record(100.0, 5.0, 100.0)
    assert r.is_high_loss() is False
