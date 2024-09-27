from sqlalchemy import create_engine, select,update,delete
from sqlalchemy.orm import Session
from typing import Union

from DTO.reservationDTO import ReservationDTO
from modele.chambre import Reservation, Chambre, TypeChambre,Client

engine = create_engine('mssql+pyodbc://GRINDLUPC\\SQLEXPRESS/Hotel?driver=SQL Server', use_setinputsizes=False)

