from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
import os

from DTO.clientDTO import ClientDTO
from modele.chambre import Client

engine = create_engine(f'mssql+pyodbc://{os.environ['COMPUTERNAME']}\\SQLEXPRESS/Hotel?driver=SQL Server', use_setinputsizes=False)

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

        stmtClient = select(Client).where(Client.CLI_nom == CLI_nom)
        result = session.execute(stmtClient).scalars().first()

        print(stmtClient)
        
        if result:
            reservations = []

            for reservation in result.Reservation:
                reservations.append({
                    "ID de la réservations": reservation.PKRES_id,
                    "Début de la réservation": reservation.RES_startDate,
                    "Fin de la réservation": reservation.RES_endDate,
                    "Prix par jour": reservation.RES_pricePerDay,
                    "Informations": reservation.RES_infoReservation
                })

            return {
                "ID du client": result.PKCLI_id,
                "Nom": result.CLI_nom,
                "Prenom": result.CLI_prenom,
                "Adresse": result.CLI_adresse,
                "Mobile": result.CLI_mobile,
                "Réservation": reservations,
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