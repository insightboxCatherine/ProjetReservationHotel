from pydantic import BaseModel
from datetime import datetime
from modele.chambre import Reservation

class ReservationDTO(BaseModel):
    RES_startDate: datetime
    RES_endDate: datetime
    RES_pricePerDay: float
    RES_infoReservation: str
    
   