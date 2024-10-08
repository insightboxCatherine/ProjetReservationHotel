from pydantic import BaseModel


class ClientDTO(BaseModel):
    CLI_nom: str
    CLI_prenom: str
    CLI_adresse: str
    CLI_mobile: str
    CLI_motDePasse: str
    CLI_courriel: str