from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class ReservationDTO(BaseModel):
    CLI_nom: str
    CLI_prenom: str
    CHA_roomNumber: int 
    RES_startDate: datetime
    RES_endDate: datetime
    RES_pricePerDay: float
    RES_infoReservation: str
    FK_PKCHA_roomID: int  # Ajout du champ manquant

class ClientDTO(BaseModel):
    CLI_nom: str
    CLI_prenom: str
    CLI_adresse: str
    CLI_mobile: str
    CLI_motDePasse: str
    CLI_courriel: str  
   