from fastapi import FastAPI
from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

from modele.chambre import Chambre, Client, Reservation

engine = create_engine('mssql+pyodbc://GRINDLUPC\\SQLEXPRESS/Hotel?driver=SQL Server', use_setinputsizes=False)

app = FastAPI()

@app.get("/chambre/{PKCHA_roomID}")
def read_item(PKCHA_roomID: int):
    with Session(engine) as session:
        stmt = select(Chambre).where(Chambre.CHA_roomNumber == PKCHA_roomID)
        result = session.execute(stmt)
        for chambre in result.scalars():
             print(f"{chambre.CHA_roomNumber} {chambre.Type_Chambre.TYP_name} {len(chambre.Type_Chambre.chambres)}")
        
        return {"numéro de Chambre": chambre.CHA_roomNumber,
                 "Type de Chambre" : chambre.Type_Chambre.TYP_name,
                 "ID": chambre.PKCHA_roomID
                }

@app.get("/client/{CLI_nom}")
def read_item(CLI_nom: str,CLI_prenom: Union[str] = None):
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
        
        

        
  