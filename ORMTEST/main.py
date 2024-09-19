from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

from modele.chambre import Chambre, Client, Reservation, TypeChambre

engine = create_engine('mssql+pyodbc://GRINDLUPC\\SQLEXPRESS/Hotel?driver=SQL Server', use_setinputsizes=False)

app = FastAPI()

# Data Transfer Object : pydantic BaseModel pour intégration facile avec FastAPI
class TypeChambreDTO(BaseModel): 
    TYP_name: str
    TYP_maxPrice: float
    TYP_minPrice: float
    TYP_description : str

class ChambreDTO(BaseModel): 
    CHA_roomNumber: int
    CHA_availability : bool
    CHA_otherInfo: str
    type_chambre: str

class ClientDTO(BaseModel):
    CLI_nom: str
    CLI_prenom: str
    CLI_adresse: str
    CLI_mobile: str
    CLI_motDePasse: str
    CLI_courriel: str

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

@app.post("/creerchambre")
def read_item(chambre: ChambreDTO):
    with Session(engine) as session:
        stmt = select(TypeChambre).where(TypeChambre.TYP_name == chambre.type_chambre)
        result = session.execute(stmt)
        print(stmt)      

        for type_chambre in result.scalars():
            print("test")

            nouvelleChambre = Chambre(
            CHA_roomNumber = chambre.CHA_roomNumber,
            CHA_availability = chambre.CHA_availability,
            CHA_otherInfo = chambre.CHA_otherInfo,
            type_chambre = type_chambre
            )

            session.add(nouvelleChambre)
            session.commit()
        
        return chambre

@app.post("/creerTypeChambre")
def read_item(type: TypeChambreDTO):
    with Session(engine) as session:
        nouveauTypeChambre = TypeChambre (
            TYP_name = type.TYP_name,
            TYP_maxPrice = type.TYP_maxPrice,
            TYP_minPrice = type.TYP_minPrice,
            TYP_description = type.TYP_description
        )

        session.add(nouveauTypeChambre)
        session.commit()
        
        return type


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

@app.post("/creerclient")
def create_client(client_dto: ClientDTO):
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


