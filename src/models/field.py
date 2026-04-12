import datetime


class Field:
    def __init__(
        self,
        name: str,
        area_ha: float,
        variety: str | None = None,
        plant_date: datetime.date | None = None,
        id: int | None = None,
    ):
        self.id = id
        self.name = name
        self.area_ha = area_ha
        self.variety = variety
        self.plant_date = plant_date

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "area_ha": self.area_ha,
            "variety": self.variety,
            "plant_date": self.plant_date.isoformat() if self.plant_date else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Field":
        plant_date = None
        if data.get("plant_date"):
            plant_date = datetime.date.fromisoformat(data["plant_date"])
        return cls(
            id=data.get("id"),
            name=data["name"],
            area_ha=data["area_ha"],
            variety=data.get("variety"),
            plant_date=plant_date,
        )
