from typing import Union
from fastapi import FastAPI
from sqlalchemy import create_engine,text

#GRINDLUPC\SQLEXPRESS
engine = create_engine("mssql+pyodbc://GRINDLUPC\\SQLEXPRESS/hotel?driver=SQL+Server+Native+Client+11.0&trusted_connection=yes")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Sick World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    connection = engine.connect()
    query = "SELECT CHA_roomNumber FROM Chambre ORDER BY 1 ASC"
    result = connection.execute(text(query))
    numeros = [row[0] for row in result]
    for row in numeros:
        print(row)

    connection.close()
    
    return {"engine.connect()": "Réussi!!"}



