from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class BuildingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    address: str
    latitude: Decimal
    longitude: Decimal
