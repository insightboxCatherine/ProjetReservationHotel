from sqlalchemy import create_engine, select,update,delete
from sqlalchemy.orm import Session
from typing import Union

from metier.clientMetier import ChercherClient
from DTO.reservationDTO import ReservationDTO
from modele.chambre import Reservation, Chambre, TypeChambre,Client

engine = create_engine('mssql+pyodbc://GRINDLUPC\\SQLEXPRESS/Hotel?driver=SQL Server', use_setinputsizes=False)


def ModifierReservation(CLI_nom : str, reservation : ReservationDTO):
    with Session(engine) as session:
        stmtClient = select(Client).join(Reservation, Client.PKCLI_id == Reservation.FK_PKCLI_id).where(Client.CLI_nom == CLI_nom)
        resultClient = session.execute(stmtClient).scalars().first()

        if not resultClient:
            return{"Client sans réservation ou inexistant"}

        idClient = resultClient.PKCLI_id
        idChambre = resultClient.Reservation.FK_PKCHA_roomID
        res_startDate = reservation.RES_startDate
        res_endDate = reservation.RES_endDate
        res_pricePerDay = reservation.RES_pricePerDay
        res_infoReservation = reservation.RES_infoReservation

        print(idClient,"\n",idChambre,"\n",)
        
        stmtModifyReservation = update(Reservation).where(Reservation.FK_PKCLI_id == idClient).values({
            "RES_startDate": res_startDate,
            "RES_endDate": res_endDate,
            "RES_pricePerDay": res_pricePerDay,
            "RES_infoReservation": res_infoReservation
            })
        resultModififyReservation = session.execute(stmtModifyReservation)

        resultClient = session.execute(stmtClient).scalars().first()
        session.commit()

        if resultModififyReservation:
            return{
                "ID de la réservations": resultClient.Reservation.PKRES_id,
                "Début de la réservation": resultClient.Reservation.RES_startDate,
                "Fin de la réservation": resultClient.Reservation.RES_endDate,
                "Prix par jour": resultClient.Reservation.RES_pricePerDay,
                "Informations": resultClient.Reservation.RES_infoReservation
            }
        else:
            return {"Une erreur est survenu"}

def SupprimerReservation(CLI_nom : str):
    with Session(engine) as session:
        stmtClient = select(Client).join(Reservation, Client.PKCLI_id == Reservation.FK_PKCLI_id).where(Client.CLI_nom == CLI_nom)
        resultClient = session.execute(stmtClient).scalars().first()

        if not resultClient:
                return{"Client sans réservation ou inexistant"}
        idClient = resultClient.PKCLI_id
        idReservation = resultClient.Reservation.PKRES_id

        stmtDeleteReservation = delete(Reservation).where(Reservation.FK_PKCLI_id == idClient)
        resultDeleteReservation = session.execute(stmtDeleteReservation)

        if resultDeleteReservation:
             session.commit()
             return{
                  "La Réservation de ",resultClient.CLI_nom," ",resultClient.CLI_prenom," à été annulée\n",
                    "ID de la réservation annulée : ", idReservation
             }    
        else:
             return{"Quelque chose n'a pas fonctionnée"}
        
def CreerReservation(CLI_nom: str, CHA_roomNumber: int,reservation: ReservationDTO):
    with Session(engine) as session:
        # Rechercher le client par nom
        stmtClient = select(Client).where(Client.CLI_nom == CLI_nom)
        resultClient = session.execute(stmtClient).scalars().first()

        if not resultClient:
            return {"Erreur": "Client inexistant"}

        # Vérifier si la chambre existe et est disponible pour la période donnée
        stmtChambre = select(Chambre).where(Chambre.PKCHA_roomID == Reservation.FK_PKCHA_roomID)
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