from pydantic import BaseModel
from uuid import UUID

class ChambreDTO(BaseModel): 
    CHA_roomNumber: int
    CHA_otherInfo: str
    Type_chambre: UUID

class TypeChambreDTO(BaseModel): 
    TYP_name: str
    TYP_maxPrice: float
    TYP_minPrice: float
    TYP_description : str
    
class DateRange(BaseModel):
    startDate: str
    endDate: str    