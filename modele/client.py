from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column

class Base(DeclarativeBase):
    pass

class Client(Base):
    __tablename__ = "client"

    CLI_nom: Mapped[str]
    CLI_prenom: Mapped[str]
    CLI_adresse: Mapped[str]
    CLI_mobile: Mapped[str]
    CLI_motDePasse: Mapped[str]
    PKCHA_roomID: Mapped[str] = mapped_column(primary_key=True)
    fk_PKTYP_id: Mapped[str] = mapped_column(ForeignKey("type_chambre.PKTYP_id"))

    type_chambre: Mapped['TypeChambre'] = relationship()