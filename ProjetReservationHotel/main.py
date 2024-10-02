from fastapi import FastAPI
from typing import Union
from sqlalchemy import create_engine

from DTO.clientDTO import ClientDTO
from metier.clientMetier import CreerClient,ChercherClient
from DTO.chambreDTO import ChambreDTO
from metier.chambreMetier import creerChambre, getChambreParNumero, CreerTypeChambre
from DTO.reservationDTO import ReservationDTO
from metier.reservationMetier import ModifierReservation, SupprimerReservation, CreerReservation

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
def modify_reservation(CLI_nom : str, reservation : ReservationDTO):
    return ModifierReservation(CLI_nom, reservation)

@app.post("/supprimerreservation")
def delete_reservation(CLI_nom : str):
    return SupprimerReservation(CLI_nom)

@app.post("/creerreservation")
def Creer_reservation(CLI_nom: str, CHA_roomNumber,reservation: ReservationDTO):
    return CreerReservation(CLI_nom, CHA_roomNumber, reservation)