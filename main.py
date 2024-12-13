from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Annotated
from pydantic import BaseModel
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy import create_engine, select
from datetime import date, datetime, timedelta, timezone
import jwt
import uvicorn
import os
from DTO.clientDTO import ClientDTO
from metier.clientMetier import CreerClient,ChercherClient, ModifierClient
from DTO.chambreDTO import ChambreDTO, DateRange, TypeChambreDTO
from metier.chambreMetier import CreerChambre, GetChambreParNumero, CreerTypeChambre, RechercherChambreLibre
from DTO.reservationDTO import ReservationDTO, CriteresRechercheDTO
from metier.reservationMetier import ModifierReservation, SupprimerReservation, CreerReservation, rechercherReservation
from metier.listetypeschambre import ListeTypesChambres

engine = create_engine(f'mssql+pyodbc://{os.environ['COMPUTERNAME']}\\SQLEXPRESS/Hotel?driver=SQL Server', use_setinputsizes=False)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.get("/chambre")
def read_item(current_user: Annotated[User, Depends(get_current_active_user)], CHA_roomNumber: int):
    return GetChambreParNumero(CHA_roomNumber)

@app.post("/creerchambre")
def read_item(current_user: Annotated[User, Depends(get_current_active_user)], chambre: ChambreDTO):
    return CreerChambre(chambre)

@app.post("/creerTypeChambre")
def read_item(current_user: Annotated[User, Depends(get_current_active_user)], type_dto: TypeChambreDTO):
    return CreerTypeChambre(type_dto)

@app.get("/client/{CLI_nom}")
def read_item(current_user: Annotated[User, Depends(get_current_active_user)], CLI_nom: str,CLI_prenom: Union[str] = None):
    return ChercherClient(CLI_nom)

@app.post("/creerclient")
def create_client(current_user: Annotated[User, Depends(get_current_active_user)], client_dto: ClientDTO):
    return CreerClient(client_dto)

@app.post("/modifierreservation")
def modify_reservation(current_user: Annotated[User, Depends(get_current_active_user)], PKRES_id: str, reservation : ReservationDTO):
    return ModifierReservation(PKRES_id, reservation)

@app.post("/supprimerreservation")
def delete_reservation(current_user: Annotated[User, Depends(get_current_active_user)], PKRES_id: str):
    return SupprimerReservation(PKRES_id)

@app.post("/creerreservation")
def Creer_reservation(
    current_user: Annotated[User, Depends(get_current_active_user)],
    CLI_nom: str,
    CHA_roomNumber: int,
    reservation: ReservationDTO,
): return CreerReservation(CLI_nom, CHA_roomNumber, reservation)
  
@app.post("/modifierclient/{client_id}")
def modifier_client(current_user: Annotated[User, Depends(get_current_active_user)], client_id: str, client_dto: ClientDTO):
    return ModifierClient(client_id, client_dto)

@app.post("/rechercherReservation")
def rechercher_reservations(current_user: Annotated[User,Depends(get_current_active_user)], criteres: CriteresRechercheDTO):
    prenom = criteres.prenom
    nom = criteres.nom
    roomNumber = criteres.roomNumber
    startDate = criteres.startDate
    endDate = criteres.endDate
    return rechercherReservation(prenom, nom, roomNumber, startDate, endDate)

@app.post("/rechercherchambrelibre")
def rechercher_chambre_libre(
    date_range: DateRange,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    startDate = date_range.startDate
    endDate = date_range.endDate

    # Validation des dates
    if not startDate or not endDate:
        raise HTTPException(status_code=400, detail="Les dates de début et de fin sont requises.")

    # Appel à la fonction RechercherChambreLibre avec les dates
    return RechercherChambreLibre(startDate, endDate)

@app.get("/listetypeschambres")
def list_types_chambres(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return ListeTypesChambres()