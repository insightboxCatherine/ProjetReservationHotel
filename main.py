from typing import Annotated
from passlib.context import CryptContext
import jwt
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Union
from sqlalchemy import create_engine 
import os
from DTO.clientDTO import ClientDTO
from metier.clientMetier import CreerClient,ChercherClient
from DTO.chambreDTO import ChambreDTO, TypeChambreDTO
from metier.chambreMetier import CreerChambre, GetChambreParNumero, CreerTypeChambre, RechercherChambreLibre
from DTO.reservationDTO import ReservationDTO
from metier.reservationMetier import ModifierReservation, SupprimerReservation, CreerReservation, rechercherReservation

engine = create_engine(f'mssql+pyodbc://{os.environ['COMPUTERNAME']}\\SQLEXPRESS/Hotel?driver=SQL+Server', use_setinputsizes=False)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Créez un contexte pour hacher les mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Clé secrète pour signer le JWT (gardez-la en sécurité !)
SECRET_KEY = "votre_clé_secrète"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": hash_password("secret")
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": hash_password("secret2")
    },
}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

def fake_hash_password(password: str):
    return "fakehashed" + password

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return get_user(fake_users_db, username)  # Utilise get_user pour obtenir l'utilisateur
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None

class UserInDB(User):
    hashed_password: str

@app.get("/chambre/{No_chambre}")
def read_item(CHA_roomNumber: int, current_user: Annotated[User, Depends(get_current_user)]):
    return GetChambreParNumero(CHA_roomNumber)

@app.post("/creerTypeChambre")
def read_item(type_dto: TypeChambreDTO, current_user: Annotated[User, Depends(get_current_user)]):
    return CreerTypeChambre(type_dto)    

@app.post("/creerchambre")
def read_item(chambre: ChambreDTO, current_user: Annotated[User, Depends(get_current_user)]):
    return CreerChambre(chambre)

@app.get("/client/{CLI_nom}")
def read_item(CLI_nom: str, CLI_prenom: Union[str, None] = None, current_user: User = Depends(get_current_user)):
    return ChercherClient(CLI_nom)

@app.post("/creerclient")
def create_client(client_dto: ClientDTO, current_user: Annotated[User, Depends(get_current_user)]):
    return CreerClient(client_dto)

@app.post("/modifierreservation")
def modify_reservation(CLI_nom : str, reservation : ReservationDTO, current_user: Annotated[User, Depends(get_current_user)]):
    return ModifierReservation(CLI_nom, reservation)

@app.post("/supprimerreservation")
def delete_reservation(CLI_nom : str, current_user: Annotated[User, Depends(get_current_user)]):
    return SupprimerReservation(CLI_nom)

@app.post("/creerreservation")
def Creer_reservation(CLI_nom: str, CHA_roomNumber,reservation: ReservationDTO, current_user: Annotated[User, Depends(get_current_user)]):
    return CreerReservation(CLI_nom, CHA_roomNumber, reservation)

@app.post("/rechercherReservation")
def rechercher_reservations(
    prenom: Union[str, None] = None,
    nom: Union[str, None] = None,
    roomNumber: Union[int, None] = None,
    idClient: Union[str, None] = None,
    idReservation: Union[str, None] = None,
    startDate: Union[datetime, None] = None,
    endDate: Union[datetime, None] = None,
    current_user: User = Depends(get_current_user)  
):
    try:
        return rechercherReservation(prenom, nom, roomNumber, idClient, idReservation, startDate, endDate)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/rechercherchambrelibre")
def rechercher_chambre_libre(current_user: User = Depends(get_current_user)):
    return RechercherChambreLibre()
 

 
  

