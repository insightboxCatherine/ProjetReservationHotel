from pydantic import BaseModel, EmailStr, constr

class ClientDTO(BaseModel):
    CLI_nom: str
    CLI_prenom: str
    CLI_adresse: str
    CLI_mobile: constr(pattern=r'^\+?\d{10,15}$')  # type: ignore # Numéro de téléphone valide avec un minimum de 10 chiffres
    CLI_motDePasse: str
    CLI_courriel: EmailStr