from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import os
from modele.chambre import TypeChambre
from fastapi.responses import JSONResponse

engine = create_engine(f'mssql+pyodbc://{os.environ['COMPUTERNAME']}\\SQLEXPRESS/Hotel?driver=SQL Server', use_setinputsizes=False)

def ListeTypesChambres():
    with Session(engine) as session:
        # Aller chercher les types de chambre
        stmt = select(TypeChambre)
        result = session.execute(stmt).scalars()
        
        types_chambres = [
            {"TYP_name": res.TYP_name, "PKTYP_id": res.PKTYP_id, "TYP_descriptions": res.TYP_description} 
            for res in result
        ]
        return types_chambres