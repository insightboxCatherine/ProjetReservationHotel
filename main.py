from typing import Union
from fastapi import FastAPI, HTTPException
from DTO.chambreDTO import ChambreDTO, TypeChambreDTO
from DTO.clientDTO import ClientDTO
from DTO.reservationDTO import ReservationDTO
from metier.chambreMetier import creerChambre, creerTypeChambre, getChambreParNumero
from metier.clientMetier import CreerClient, ChercherClient
from metier.reservationMetier import CreerReservation, Reservation
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, engine
from modele.chambre import Chambre, TypeChambre, Client, Reservation
from pydantic import BaseModel
 
app = FastAPI()
 
@app.get("/chambre/{CHA_roomNumber}")
def read_item(CHA_roomNumber: int):
    return getChambreParNumero(CHA_roomNumber)
    
@app.post("/creerChambre")
def read_item(chambre: ChambreDTO):
        return creerChambre(chambre)

@app.post("/creerTypeChambre")
def read_item(type_dto: TypeChambreDTO):
    return creerTypeChambre(type_dto)
    
@app.get("/client/{CLI_nom}")
def read_item(CLI_nom: str,CLI_prenom: Union[str] = None):
    return ChercherClient(CLI_nom)

@app.post("/creerclient")
def create_client(client_dto: ClientDTO):
    return CreerClient(client_dto)

@app.post("/creerreservation")
def create_reservation(reservation_dto: ReservationDTO):
     return CreerReservation(reservation_dto.CLI_nom, reservation_dto)

@app.get("/chercherclient")
def chercher_client(CLI_nom: str):
    return ChercherClient(CLI_nom)