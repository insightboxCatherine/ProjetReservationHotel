from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from DTO.clientDTO import ClientDTO
from modele.chambre import Client,Reservation

engine = create_engine('mssql+pyodbc://GRINDLUPC\\SQLEXPRESS/Hotel?driver=SQL Server', use_setinputsizes=False)

def CreerClient(client_dto: ClientDTO):
    with Session(engine) as session:
            nouveau_client = Client(
                CLI_nom=client_dto.CLI_nom,
                CLI_prenom=client_dto.CLI_prenom,
                CLI_adresse=client_dto.CLI_adresse,
                CLI_mobile=client_dto.CLI_mobile,
                CLI_motDePasse=client_dto.CLI_motDePasse,
                CLI_courriel=client_dto.CLI_courriel
            )
            
            session.add(nouveau_client)
            session.commit()

def ChercherClient(CLI_nom: str):
      with Session(engine) as session:

        stmtClient = select(Client).join(Reservation, Client.PKCLI_id == Reservation.FK_PKCLI_id).where(Client.CLI_nom == CLI_nom)
        result = session.execute(stmtClient).scalars().first()

        print(stmtClient)
        
        if result:
            reservation = {
                "ID de la réservations": result.Reservation.PKRES_id,
                "Début de la réservation": result.Reservation.RES_startDate,
                "Fin de la réservation": result.Reservation.RES_endDate,
                "Prix par jour": result.Reservation.RES_pricePerDay,
                "Informations": result.Reservation.RES_infoReservation
            }

            return {
                "ID du client": result.PKCLI_id,
                "Nom": result.CLI_nom,
                "Prenom": result.CLI_prenom,
                "Adresse": result.CLI_adresse,
                "Mobile": result.CLI_mobile,
                "Réservation": reservation,
            }
        
        
        elif not result:
            stmtClient = select(Client).where(Client.CLI_nom == CLI_nom)
            result = session.execute(stmtClient).scalars().first()

            if not result:
                return{"Doesn't exist"}

            return{"ID du client": result.PKCLI_id,
                "Nom": result.CLI_nom,
                "Prenom": result.CLI_prenom,
                "Adresse": result.CLI_adresse,
                "Mobile": result.CLI_mobile,
                "Réservation": "None",
            }