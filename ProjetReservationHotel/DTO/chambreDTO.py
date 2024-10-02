from pydantic import BaseModel

class ChambreDTO(BaseModel): 
    CHA_roomNumber: int
    CHA_availability : bool
    CHA_otherInfo: str
    Type_chambre: str

class TypeChambreDTO(BaseModel): 
    TYP_name: str
    TYP_maxPrice: float
    TYP_minPrice: float
    TYP_description : str