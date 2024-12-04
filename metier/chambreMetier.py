from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy import and_, not_
from fastapi import HTTPException
import os

from DTO.chambreDTO import ChambreDTO, TypeChambreDTO

from modele.chambre import Chambre, Reservation, TypeChambre


engine = create_engine(f'mssql+pyodbc://{os.environ['COMPUTERNAME']}\\SQLEXPRESS/Hotel?driver=SQL+Server', use_setinputsizes=False)

def CreerChambre(chambre: ChambreDTO):
     with Session(engine) as session:
        stmt = select(TypeChambre).where(TypeChambre.TYP_name == chambre.Type_chambre)
        result = session.execute(stmt)
        
        for typeChambre in result.scalars():
            
            nouvelleChambre = Chambre(
            CHA_roomNumber = chambre.CHA_roomNumber,
            CHA_availability = chambre.CHA_availability,
            CHA_otherInfo = chambre.CHA_otherInfo,
            Type_Chambre = typeChambre
            )

            session.add(nouvelleChambre)
            session.commit()
        
        return chambre
     
def GetChambreParNumero(CHA_roomNumber: int):
    with Session(engine) as session:
        stmt = select(Chambre).where(Chambre.CHA_roomNumber == CHA_roomNumber)
        result = session.execute(stmt)
        for chambre in result.scalars():
             print(f"{chambre.CHA_roomNumber} {chambre.Type_Chambre.TYP_name} {len(chambre.Type_Chambre.chambres)}")
        
        return {"numero_chambre": chambre.CHA_roomNumber,
                 "type_chambre" : chambre.Type_Chambre.TYP_name}     
    
def CreerTypeChambre(type_dto: TypeChambreDTO):    
    with Session(engine) as session:
        try:
            nouveau_type = TypeChambre(
                TYP_name=type_dto.TYP_name,
                TYP_maxPrice=type_dto.TYP_maxPrice,
                TYP_minPrice=type_dto.TYP_minPrice,
                TYP_description=type_dto.TYP_description
            )
            session.add(nouveau_type)
            session.commit()
            return type_dto
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        
def RechercherChambreLibre(startDate, endDate):
    with Session(engine) as session:
        #Subquery to get rooms in reservation
        subquery = (
            select(Reservation)
            .where(
                and_(
                    Reservation.FK_PKCHA_roomID == Chambre.PKCHA_roomID,
                    Reservation.RES_startDate < endDate,
                    Reservation.RES_endDate > startDate
                )
            )
        )

        # Requete pour enlever de la liste les chambres occupées
        stmtChambre = (
            select(Chambre)
            .where(not_(subquery.exists()))
        ).order_by(Chambre.CHA_roomNumber)

        '''# Requête pour trouver les chambres qui ne sont pas réservées pendant la plage horaire donnée
        stmtChambre = select(Chambre).where(
            Chambre.CHA_availability == True,
            ~Chambre.reservations.any(
                and_(
                    Reservation.RES_startDate <= endDate,
                    Reservation.RES_endDate >= startDate
                )
            )
        ).order_by(Chambre.CHA_roomNumber)'''
        
        resultChambre = session.execute(stmtChambre).scalars().all()
        
        if not resultChambre:
            return {"message": "Aucune chambre libre pour cette période."}

        chambresLibres = []
        for chambre in resultChambre:
            chambresLibres.append({
                "ID chambre": chambre.PKCHA_roomID,
                "Disponibilité": chambre.CHA_availability,
                "numéro de chambre": chambre.CHA_roomNumber,
                "type_chambre": chambre.Type_Chambre.TYP_name
            })

        return {"Chambres Libres": chambresLibres}