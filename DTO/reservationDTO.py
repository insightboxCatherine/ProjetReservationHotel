from pydantic import BaseModel
from datetime import datetime
from DTO.chambreDTO import ChambreDTO
from modele.chambre import Reservation
from uuid import UUID
from typing import Optional, Tuple

class CriteresRechercheDTO(BaseModel):
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    priceRange: Optional[tuple[float, float]] = None
    nom: Optional[str] = None
    prenom: Optional[str] = None
    roomNumber: Optional[int] = None 
    idClient: Optional[UUID] = None
    idReservation: Optional[UUID] = None

class ReservationDTO(BaseModel):
    RES_startDate: datetime
    RES_endDate: datetime
    RES_pricePerDay: float
    RES_infoReservation: str = None 
    idReservation: UUID
    roomNumber: int

class ReservationInput(BaseModel):
    CLI_nom: str
    CHA_roomNumber: int
    reservation: ReservationDTO  