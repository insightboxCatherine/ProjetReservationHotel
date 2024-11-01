from typing import List
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from uuid import UUID, uuid4

class Base(DeclarativeBase):
    pass

class Chambre(Base):
    __tablename__ = "Chambre"

    CHA_roomNumber: Mapped[int]
    CHA_availability: Mapped[bool]
    CHA_otherInfo: Mapped[str]
    PKCHA_roomID: Mapped[UUID] = mapped_column(default=uuid4,primary_key=True)
    FK_PKTYP_id: Mapped[str] = mapped_column(ForeignKey("Type_Chambre.PKTYP_id"))

    Type_Chambre: Mapped['TypeChambre'] = relationship()
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="chambre")

class TypeChambre(Base):
    __tablename__ = "Type_Chambre"

    TYP_name: Mapped[str]
    TYP_maxPrice: Mapped[float]
    TYP_minPrice: Mapped[float]
    TYP_description: Mapped[str]
    PKTYP_id: Mapped[UUID] = mapped_column(default=uuid4,primary_key=True)

    chambres: Mapped[List["Chambre"]] = relationship(back_populates="Type_Chambre")

class Client(Base):
    __tablename__ = "Client"

    CLI_nom: Mapped[str]
    CLI_prenom: Mapped[str]
    CLI_adresse: Mapped[str]
    CLI_mobile: Mapped[str]
    CLI_motDePasse: Mapped[str]
    CLI_courriel: Mapped[str]
    PKCLI_id: Mapped[UUID] = mapped_column(default=uuid4,primary_key=True)

    Reservation: Mapped[List['Reservation']] = relationship()

class Reservation(Base):
    __tablename__ = "Reservation"

    RES_startDate: Mapped[datetime]
    RES_endDate: Mapped[datetime]
    RES_pricePerDay: Mapped[float]
    RES_infoReservation: Mapped[str]
    PKRES_id: Mapped[UUID] = mapped_column(default=uuid4,primary_key=True)
    FK_PKCLI_id: Mapped[str] = mapped_column(ForeignKey("Client.PKCLI_id"))
    FK_PKCHA_roomID: Mapped[str] = mapped_column(ForeignKey("Chambre.PKCHA_roomID"))

    clients: Mapped[List["Client"]] = relationship(back_populates="Reservation")
    chambre: Mapped["Chambre"] = relationship()


     

