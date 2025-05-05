from pydantic import BaseModel

class Aeroporto(BaseModel):
    airport_code: str
    name: str
    city: str
    country: str
    latitude: float
    longitude: float
