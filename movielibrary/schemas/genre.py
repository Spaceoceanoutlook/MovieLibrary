from pydantic import BaseModel, ConfigDict


class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class GenreRead(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)
