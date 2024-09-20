from typing import Union
from fastapi import FastAPI, HTTPException
from DTO.chambreDTO import ChambreDTO, TypeChambreDTO
from DTO.clientDTO import ClientDTO
from metier.chambreMetier import creerChambre, creerTypeChambre, getChambreParNumero
from metier.clientMetier import CreerClient, ChercherClient
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
    
# Endpoint to create a new 'TypeChambre'
@app.post("/creerTypeChambre")
def read_item(type_dto: TypeChambreDTO):
    return creerTypeChambre(type_dto)
    

@app.get("/client/{CLI_nom}")
def read_item(CLI_nom: str,CLI_prenom: Union[str] = None):
    return ChercherClient(CLI_nom)

@app.post("/creerclient")
def create_client(client_dto: ClientDTO):
    return CreerClient(client_dto)