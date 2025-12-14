from dataclasses import dataclass

@dataclass(frozen=True)
class Rifugio:
    id: int
    nome: str
    localita: str
    altitudine: int
    capienza: int
    aperto: int


    def __hash__(self):
        return hash(self.id)


    def __str__(self):
        return f"[{self.id}] {self.nome} ({self.localita})"