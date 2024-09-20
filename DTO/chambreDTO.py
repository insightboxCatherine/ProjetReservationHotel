from pydantic import BaseModel

class ChambreDTO(BaseModel): 
    CHA_roomNumber: int
    CHA_availability : bool
    CHA_otherInfo: str
    type_chambre: str

class TypeChambreDTO(BaseModel): 
    TYP_name: str
    TYP_maxPrice: float
    TYP_minPrice: float
    TYP_description : str
