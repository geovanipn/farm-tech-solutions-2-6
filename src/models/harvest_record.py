import datetime


VALID_VARIETIES: tuple = (
    "RB867515", "SP80-3280", "CTC4", "RB92579",
    "SP83-2847", "RB966928", "Outra"
)


class HarvestRecord:
    def __init__(
        self,
        field_id: int,
        harvester_id: int,
        field_name: str,
        harvester_code: str,
        operator_name: str,
        harvest_date: datetime.date,
        estimated_yield_ton: float,
        loss_pct: float,
        ton_price_brl: float,
        id: int | None = None,
        loss_ton: float | None = None,
        loss_brl: float | None = None,
    ):
        self.id = id
        self.field_id = field_id
        self.harvester_id = harvester_id
        self.field_name = field_name
        self.harvester_code = harvester_code
        self.operator_name = operator_name
        self.harvest_date = harvest_date
        self.estimated_yield_ton = estimated_yield_ton
        self.loss_pct = loss_pct
        self.ton_price_brl = ton_price_brl
        self.loss_ton = loss_ton
        self.loss_brl = loss_brl

    def calculate_losses(self) -> None:
        self.loss_ton = round(self.estimated_yield_ton * self.loss_pct / 100, 2)
        self.loss_brl = round(self.loss_ton * self.ton_price_brl, 2)

    def is_high_loss(self) -> bool:
        return self.loss_pct > 10

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "field_id": self.field_id,
            "harvester_id": self.harvester_id,
            "field_name": self.field_name,
            "harvester_code": self.harvester_code,
            "operator_name": self.operator_name,
            "harvest_date": self.harvest_date.isoformat(),
            "estimated_yield_ton": self.estimated_yield_ton,
            "loss_pct": self.loss_pct,
            "ton_price_brl": self.ton_price_brl,
            "loss_ton": self.loss_ton,
            "loss_brl": self.loss_brl,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "HarvestRecord":
        harvest_date = datetime.date.fromisoformat(data["harvest_date"])
        return cls(
            id=data.get("id"),
            field_id=data["field_id"],
            harvester_id=data["harvester_id"],
            field_name=data["field_name"],
            harvester_code=data["harvester_code"],
            operator_name=data["operator_name"],
            harvest_date=harvest_date,
            estimated_yield_ton=data["estimated_yield_ton"],
            loss_pct=data["loss_pct"],
            ton_price_brl=data["ton_price_brl"],
            loss_ton=data.get("loss_ton"),
            loss_brl=data.get("loss_brl"),
        )
