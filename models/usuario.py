from dataclasses import dataclass

@dataclass
class Usuario:
    id: int
    username: str
    password: str
    rol: str