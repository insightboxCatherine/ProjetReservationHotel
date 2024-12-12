from pydantic import BaseModel, EmailStr
from datetime import date
from DTO.chambreDTO import ChambreDTO
from modele.chambre import Reservation
from uuid import UUID
from typing import Optional, Tuple

class CriteresRechercheDTO(BaseModel):
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    nom: Optional[str] = None
    prenom: Optional[str] = None
    roomNumber: Optional[int] = None 

class ReservationDTO(BaseModel):
    CLI_prenom: Optional[str] = None
    CLI_courriel: Optional[EmailStr] = None
    RES_startDate: date
    RES_endDate: date
    RES_pricePerDay: float
    RES_infoReservation: str = None 
    idReservation: UUID
    roomNumber: int

class ReservationInput(BaseModel):
    CLI_nom: str
    CHA_roomNumber: int
    reservation: ReservationDTO  