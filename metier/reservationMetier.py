from datetime import datetime
from sqlalchemy import create_engine, select,update,delete
from sqlalchemy.orm import Session
import os

from DTO.reservationDTO import ReservationDTO, CriteresRechercheDTO
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
        idReservation = resultClient.Reservation[0].PKRES_id

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
        stmtClient = select(Client).where(Client.CLI_nom == CLI_nom)
        resultClient = session.execute(stmtClient).scalars().first()

        if not resultClient:
            return {"Erreur": "Client inexistant"}

        # Rechercher la chambre
        stmtChambre = select(Chambre).where(Chambre.CHA_roomNumber == CHA_roomNumber)
        resultChambre = session.execute(stmtChambre).scalars().first()

        if not resultChambre:
            return {"Erreur": "Chambre inexistante"}
        
        stmtTypeChambre = select(TypeChambre).where(resultChambre.FK_PKTYP_id == TypeChambre.PKTYP_id)
        resultTypeChambre = session.execute(stmtTypeChambre).scalars().first()

        # Vérifier que la chambre est libre pendant la période
        stmtReservation = select(Reservation).where(
            Reservation.FK_PKCHA_roomID == resultChambre.PKCHA_roomID,
            Reservation.RES_startDate < reservation.RES_endDate,
            Reservation.RES_endDate > reservation.RES_startDate
        )
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

def rechercherReservation(prenom:str, nom: str, roomNumber: int, idClient:str, idReservation:str, startDate:datetime, endDate:datetime):
    with Session(engine) as session:

        # Validation des critères
        if prenom and len(prenom) > 60:
            raise ValueError('Le prénom est trop long')
            
        if nom and len(nom) > 60:
            raise ValueError('Le nom est trop long')
        
        if not nom and prenom:
            raise ValueError("La recherche par prénom seulement n'est pas supportée. Veuillez indiquer un nom et prénom.")
        
        if roomNumber is not None and not isinstance(roomNumber, int):
            raise ValueError("Le numéro de chambre doit être un entier valide")
        
        if idClient and len(idClient) != 36:
            raise ValueError("idClient doit contenir 36 caractères")
        
        if idReservation and len(idReservation) != 36:
            raise ValueError("idReservation doit contenir 36 caractères")

        # Construction de la requête
        stmt = select(Reservation)

        if idReservation:
            stmt = stmt.where(Reservation.PKRES_id == idReservation)
        
        if roomNumber:
            stmt = stmt.join(Chambre).where(Chambre.CHA_roomNumber == roomNumber)

        if idClient:
            stmt = stmt.where(Reservation.FK_PKCLI_id == idClient)

        if nom:
            stmt = stmt.join(Client).where(Client.CLI_nom == nom)
            if prenom:
                stmt = stmt.where(Client.CLI_prenom == prenom)

        if startDate: 
            stmt = stmt.where(
                Reservation.RES_endDate >= startDate)
        if endDate:
            stmt = stmt.where(
                Reservation.RES_startDate <= endDate)        

        reservations = []
        for reservation in session.execute(stmt).scalars():
            reservations.append(ReservationDTO(
                RES_startDate=reservation.RES_startDate,
                RES_endDate=reservation.RES_endDate,
                RES_pricePerDay=reservation.RES_pricePerDay,
                RES_infoReservation=reservation.RES_infoReservation,
                idReservation=reservation.PKRES_id
            ))

        if reservations == []:
           return {"Il n'y a pas de réservation selon ce critère!"} 
        return reservations

