from pydantic import BaseModel
from datetime import datetime

class ReservationDTO(BaseModel):

    RES_startDate: datetime
    RES_endDate: datetime
    RES_pricePerDay: float
    RES_infoReservation: str
    