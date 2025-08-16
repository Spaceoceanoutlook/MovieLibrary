from pydantic import BaseModel, ConfigDict


class CountryBase(BaseModel):
    name: str


class CountryCreate(CountryBase):
    pass


class CountryRead(CountryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
