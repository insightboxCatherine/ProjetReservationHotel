from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

from modele.chambre import Chambre, TypeChambre
from DTO.clientDTO import ClientDTO
from metier.clientMetier import CreerClient,ChercherClient
from DTO.chambreDTO import ChambreDTO
from metier.chambreMetier import creerChambre, getChambreParNumero, creerTypeChambre
from DTO.reservationDTO import Reservation

engine = create_engine('mssql+pyodbc://GRINDLUPC\\SQLEXPRESS/Hotel?driver=SQL Server', use_setinputsizes=False)

app = FastAPI()

@app.get("/chambre/{No_chambre}")
def read_item(CHA_roomNumber: int):
    return getChambreParNumero(CHA_roomNumber)

@app.post("/creerchambre")
def read_item(chambre: ChambreDTO):
    return creerChambre(chambre)

@app.post("/creerTypeChambre")
def read_item(type_dto: ChambreDTO):
    return creerTypeChambre(type_dto)

@app.get("/client/{CLI_nom}")
def read_item(CLI_nom: str,CLI_prenom: Union[str] = None):
    return ChercherClient(CLI_nom)

@app.post("/creerclient")
def create_client(client_dto: ClientDTO):
    return CreerClient(client_dto)

@app.post("/modifierreservation")
def modify_reservation():
    return {}