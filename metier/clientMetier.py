import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, update
from DTO.clientDTO import ClientDTO
from modele.chambre import Client

engine = create_engine(f'mssql+pyodbc://{os.environ['COMPUTERNAME']}\\SQLEXPRESS/Hotel?driver=SQL Server', use_setinputsizes=False)

def CreerClient(client_dto: ClientDTO):
    with Session(engine) as session:
        # Vérification de l'unicité du courriel
        validationErreur = ValidationClient(client_dto, session)
        if validationErreur:
            return validationErreur

        # Création du nouveau client
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

        return {"message": "Client créé avec succès", "client_id": nouveau_client.PKCLI_id}

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

def ModifierClient(client_id: str,client_dto: ClientDTO):
     with Session(engine) as session:
          
        stmtClient = select(Client).where(Client.PKCLI_id == client_id)
        resultClient = session.execute(stmtClient).scalars().first()

        if not resultClient:
            return{"Ce client n'existe pas"}
        
        validationErreur = ValidationClient(client_dto, session)
        if validationErreur:
            return validationErreur
        
        stmtModifierClient = update(Client).where(Client.PKCLI_id == client_id).values({
            "CLI_nom": client_dto.CLI_nom,
            "CLI_prenom": client_dto.CLI_prenom,
            "CLI_adresse": client_dto.CLI_adresse,
            "CLI_mobile": client_dto.CLI_mobile,
            "CLI_motDePasse": client_dto.CLI_motDePasse,
            "CLI_courriel": client_dto.CLI_courriel
            })
        resultModifierClient = session.execute(stmtModifierClient)
        resultClient = session.execute(stmtClient).scalars().first()
        session.commit()

        if resultModifierClient:
            return{
                "ID du client": resultClient.PKCLI_id,
                "Nom": resultClient.CLI_nom,
                "Prenom": resultClient.CLI_prenom,
                "Adresse": resultClient.CLI_adresse,
                "Mobile": resultClient.CLI_mobile,
                "Courriel": resultClient.CLI_courriel,
            }
        
        return{"Client modifié avec succès"}
     
def ValidationClient(client_dto: ClientDTO, session: Session):
    with Session(engine) as session:
        # Vérification de l'unicité du courriel
        client_existant_email = session.execute(select(Client).where(Client.CLI_courriel == client_dto.CLI_courriel)).scalars().first()
        if client_existant_email:
            return {"error": "Le courriel est déjà utilisé."}

        # Vérification de l'unicité du numéro de mobile
        client_existant_mobile = session.execute(select(Client).where(Client.CLI_mobile == client_dto.CLI_mobile)).scalars().first()
        if client_existant_mobile:
            return {"error": "Le numéro de mobile est déjà utilisé."}
        
        return None