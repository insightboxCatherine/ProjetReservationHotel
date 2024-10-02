from typing import List
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped
from uuid import UUID, uuid4

class Base(DeclarativeBase):
    pass

class Chambre(Base):
    __tablename__ = "chambre"

    CHA_roomNumber: Mapped[int]
    CHA_availability: Mapped[bool]
    CHA_otherInfo: Mapped[str]
    PKCHA_roomID: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    fk_PKTYP_id: Mapped[str] = mapped_column(ForeignKey("type_chambre.PKTYP_id"))

    type_chambre: Mapped['TypeChambre'] = relationship()
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="chambre")

class TypeChambre(Base):
    __tablename__ = "type_chambre"

    TYP_name: Mapped[str]
    TYP_minPrice: Mapped[float]
    TYP_maxPrice: Mapped[float]
    TYP_description: Mapped[str]
    PKTYP_id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)

    chambre: Mapped[List["Chambre"]] = relationship(back_populates="type_chambre")

class Reservation(Base):
    __tablename__ = "reservation"

    RES_startDate: Mapped[datetime]
    RES_endDate: Mapped[datetime]
    RES_pricePerDay: Mapped[float]
    RES_infoReservation: Mapped[str]
    PKRES_id: Mapped[UUID]= mapped_column(default=uuid4, primary_key=True)
    fk_PKCLI_id: Mapped[str]= mapped_column(ForeignKey("client.PKCLI_id"))
    fk_PKCHA_roomID: Mapped[str]= mapped_column(ForeignKey("chambre.PKCHA_roomID"))

    client: Mapped['Client'] = relationship()
    chambre: Mapped['Chambre'] = relationship()

class Client(Base):
    __tablename__ = "client"

    CLI_nom: Mapped[str]
    CLI_prenom: Mapped[str]
    CLI_adresse: Mapped[str]
    CLI_mobile: Mapped[str]
    CLI_motDePasse: Mapped[str]
    CLI_courriel: Mapped[str]
    PKCLI_id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    
    reservation: Mapped[List['Reservation']] = relationship( back_populates="client")  



     

