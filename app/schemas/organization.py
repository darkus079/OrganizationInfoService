from pydantic import BaseModel, ConfigDict

from app.schemas.building import BuildingResponse


class OrganizationPhoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    phone_number: str


class OrganizationListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    building_id: int


class OrganizationDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    building: BuildingResponse
    phones: list[OrganizationPhoneResponse]
