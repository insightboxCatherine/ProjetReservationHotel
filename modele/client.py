from typing import List

from sqlalchemy import Column, ForeignKey, DateTime, Float, String
from sqlalchemy.orm import relationship
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from modele.chambre import Base

class Reservation(Base):
    __tablename__ = "reservation"

    PKRES_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    FK_PKCLI_id = Column(UUID(as_uuid=True), ForeignKey("client.PKCLI_id"))  
    FK_PKCHA_roomID = Column(UUID(as_uuid=True), ForeignKey("chambre.PKCHA_roomID"))  
    RES_startDate = Column(DateTime)
    RES_endDate = Column(DateTime)
    RES_pricePerDay = Column(Float)
    RES_infoReservation = Column(String)

    client = relationship("Client", back_populates="reservations")
    chambre = relationship("Chambre", back_populates="reservations")