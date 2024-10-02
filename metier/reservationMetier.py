
from sqlalchemy import create_engine, select, insert
from sqlalchemy.orm import Session
from typing import Union
from metier.clientMetier import ChercherClient
from DTO.reservationDTO import ReservationDTO
from modele.chambre import Reservation, Chambre, TypeChambre, Client

engine = create_engine('mssql+pyodbc://CATHB\\SQLEXPRESS/hotel?driver=SQL+Server', use_setinputsizes=False)

def CreerReservation(CLI_nom: str, reservation: ReservationDTO):
    with Session(engine) as session:
        # Rechercher le client par nom
        stmtClient = select(Client).where(Client.CLI_nom == CLI_nom)
        resultClient = session.execute(stmtClient).scalars().first()

        if not resultClient:
            return {"Erreur": "Client inexistant"}

        # Vérifier si la chambre existe et est disponible pour la période donnée
        stmtChambre = select(Chambre).where(Chambre.PKCHA_roomID == reservation.FK_PKCHA_roomID)
        resultChambre = session.execute(stmtChambre).scalars().first()

        if not resultChambre:
            return {"Erreur": "Chambre inexistante"}
        if resultChambre.RES_disponibilite == False:
            return {"Erreur": "Chambre non disponible"}

        # Créer une nouvelle réservation
        new_reservation = Reservation(
            FK_PKCLI_id=resultClient.PKCLI_id,
            FK_PKCHA_roomID=reservation.FK_PKCHA_roomID,
            RES_startDate=reservation.RES_startDate,
            RES_endDate=reservation.RES_endDate,
            RES_pricePerDay=reservation.RES_pricePerDay,
            RES_infoReservation=reservation.RES_infoReservation
        )

        session.add(new_reservation)
        session.commit()

        # Vérifier que la réservation a bien été ajoutée
        if new_reservation.PKRES_id:
            return {
                "Message": "Réservation créée avec succès",
                "ID Réservation": new_reservation.PKRES_id,
                "Début de la réservation": new_reservation.RES_startDate,
                "Fin de la réservation": new_reservation.RES_endDate,
                "Prix par jour": new_reservation.RES_pricePerDay,
                "Informations": new_reservation.RES_infoReservation
            }
        else:
            return {"Erreur": "La réservation n'a pas pu être créée"}
