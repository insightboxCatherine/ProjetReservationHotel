from sqlalchemy import create_engine, select,update,delete
from sqlalchemy.orm import Session
import os

from DTO.reservationDTO import ReservationDTO
from modele.chambre import Reservation, Chambre, Client, TypeChambre

engine = create_engine(f'mssql+pyodbc://{os.environ['COMPUTERNAME']}\\SQLEXPRESS/Hotel?driver=SQL Server', use_setinputsizes=False)


def ModifierReservation(PKRES_id: str, reservation : ReservationDTO):
    with Session(engine) as session:
        stmtReservation = select(Reservation).where(Reservation.PKRES_id == PKRES_id)
        resultReservation = session.execute(stmtReservation).scalars().first()

        stmtChambre = select(Chambre).where(resultReservation.FK_PKCHA_roomID == Chambre.PKCHA_roomID)
        resultChambre = session.execute(stmtChambre).scalars().first()

        stmtTypeChambre = select(TypeChambre).where(resultChambre.FK_PKTYP_id == TypeChambre.PKTYP_id)
        resultTypeChambre = session.execute(stmtTypeChambre).scalars().first()
        print(type(resultTypeChambre))
        if not resultReservation:
            return{"Réservation inexistante"}
        
        validationErreur = ValiderReservation(reservation, resultChambre, resultTypeChambre,session)
        if validationErreur:
            return validationErreur
        
        stmtModifyReservation = update(Reservation).where(Reservation.PKRES_id == PKRES_id).values({
            "RES_startDate": reservation.RES_startDate,
            "RES_endDate": reservation.RES_endDate,
            "RES_pricePerDay": reservation.RES_pricePerDay,
            "RES_infoReservation": reservation.RES_infoReservation
            })
        
        resultModififyReservation = session.execute(stmtModifyReservation)

        resultReservation = session.execute(stmtReservation).scalars().first()
        session.commit()

        if resultModififyReservation:
            return{
                "ID de la réservations": resultReservation.PKRES_id,
                "Début de la réservation": resultReservation.RES_startDate,
                "Fin de la réservation": resultReservation.RES_endDate,
                "Prix par jour": resultReservation.RES_pricePerDay,
                "Informations": resultReservation.RES_infoReservation
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
        
def CreerReservation(CLI_nom: str, CHA_roomNumber: int, reservation: ReservationDTO):
    with Session(engine) as session:
        # Rechercher le client
        stmtClient = select(Client).where(Client.PKCLI_id == reservation.CLI_id)
        resultClient = session.execute(stmtClient).scalars().first()

        if not resultClient:
            return {"Erreur": "Client inexistant"}

        # Rechercher la chambre
        stmtChambre = select(Chambre).where(Chambre.CHA_roomNumber == CHA_roomNumber)
        resultChambre = session.execute(stmtChambre).scalars().first()

        if not resultChambre:
            return {"Erreur": "Chambre inexistante"}

        # Valider que le prix par jour est dans l'intervalle autorisé
        stmtTypeChambre = select(TypeChambre).where(TypeChambre.PKTYP_id == resultChambre.FK_PKTYP_id)
        resultTypeChambre = session.execute(stmtTypeChambre).scalars().first()

        validationErreur = ValiderReservation(reservation, resultChambre, resultTypeChambre,session)
        if validationErreur:
            return validationErreur

        # Créer la nouvelle réservation
        new_reservation = Reservation(
            FK_PKCLI_id=resultClient.PKCLI_id,
            FK_PKCHA_roomID=resultChambre.PKCHA_roomID,
            RES_startDate=reservation.RES_startDate,
            RES_endDate=reservation.RES_endDate,
            RES_pricePerDay=reservation.RES_pricePerDay,
            RES_infoReservation=reservation.RES_infoReservation
        )

        session.add(new_reservation)
        resultChambre.CHA_availability = False
        session.commit()

        return {
            "Message": "Réservation créée avec succès",
            "ID Réservation": new_reservation.PKRES_id,
            "Début de la réservation": new_reservation.RES_startDate,
            "Fin de la réservation": new_reservation.RES_endDate,
            "Prix par jour": new_reservation.RES_pricePerDay,
            "Informations": new_reservation.RES_infoReservation
        }
 
def ValiderReservation(reservation: ReservationDTO, resultChambre, resultTypeChambre,session: Session):
    with Session(engine) as session:

        # Vérifier que la chambre est libre pendant la période
        stmtReservationValidation = select(Reservation).where(
            Reservation.FK_PKCHA_roomID == resultChambre.PKCHA_roomID,
            Reservation.RES_startDate < reservation.RES_endDate,
            Reservation.RES_endDate > reservation.RES_startDate
        )
        conflicting_reservation = session.execute(stmtReservationValidation).scalars().first()

        if conflicting_reservation:
            return {"Erreur": "La chambre est déjà réservée pendant cette période"}
        
        if not (resultTypeChambre.TYP_minPrice <= reservation.RES_pricePerDay <= resultTypeChambre.TYP_maxPrice):
            return {"Erreur": f"Le prix par jour doit être entre {resultTypeChambre.TYP_minPrice} et {resultTypeChambre.TYP_maxPrice}"}
        
        return None