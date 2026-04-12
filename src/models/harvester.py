class Harvester:
    def __init__(
        self,
        code: str,
        model: str | None = None,
        id: int | None = None,
    ):
        self.id = id
        self.code = code
        self.model = model

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "code": self.code,
            "model": self.model,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Harvester":
        return cls(
            id=data.get("id"),
            code=data["code"],
            model=data.get("model"),
        )
