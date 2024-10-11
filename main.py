from fastapi import FastAPI
from typing import Union
from sqlalchemy import create_engine
import os

from DTO.clientDTO import ClientDTO
from metier.clientMetier import CreerClient,ChercherClient, ModifierClient
from DTO.chambreDTO import ChambreDTO, TypeChambreDTO
from metier.chambreMetier import CreerChambre, GetChambreParNumero, CreerTypeChambre
from DTO.reservationDTO import ReservationDTO
from metier.reservationMetier import ModifierReservation, SupprimerReservation, CreerReservation

engine = create_engine(f'mssql+pyodbc://{os.environ['COMPUTERNAME']}\\SQLEXPRESS/Hotel?driver=SQL Server', use_setinputsizes=False)

app = FastAPI()

@app.get("/chambre/{No_chambre}")
def read_item(CHA_roomNumber: int):
    return GetChambreParNumero(CHA_roomNumber)

@app.post("/creerchambre")
def read_item(chambre: ChambreDTO):
    return CreerChambre(chambre)

@app.post("/creerTypeChambre")
def read_item(type_dto: TypeChambreDTO):
    return CreerTypeChambre(type_dto)

@app.get("/client/{CLI_nom}")
def read_item(CLI_nom: str,CLI_prenom: Union[str] = None):
    return ChercherClient(CLI_nom)

@app.post("/creerclient")
def create_client(client_dto: ClientDTO):
    return CreerClient(client_dto)

@app.post("/modifierreservation")
def modify_reservation(CLI_nom : str, reservation : ReservationDTO):
    return ModifierReservation(CLI_nom, reservation)

@app.post("/supprimerreservation")
def delete_reservation(CLI_nom : str):
    return SupprimerReservation(CLI_nom)

@app.post("/creerreservation")
def Creer_reservation(CLI_nom: str, CHA_roomNumber,reservation: ReservationDTO):
    return CreerReservation(CLI_nom, CHA_roomNumber, reservation)

@app.post("/modifierclient/{client_id}")
def modifier_client(client_id: str, client_dto: ClientDTO):
    return ModifierClient(client_id, client_dto)