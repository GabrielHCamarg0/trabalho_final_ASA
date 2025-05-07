from pydantic import BaseModel

class AirportResponse(BaseModel):
    id: int
    code: str
    name: str
    city: str

    class Config:
        from_attributes = True
class AirportCreate(BaseModel):
    code: str
    name: str
    city: str

    class Config:
        from_attributes = True