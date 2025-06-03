from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.entities.author import Author

@dataclass(frozen=True)
class Commit:
    """
    Representa um commit no repositório.
    
    Attributes:
        hash (str): Hash do commit
        author (Author): Autor do commit
        date (datetime): Data do commit
        branch (str): Branch onde o commit foi feito
        environment (str): Ambiente (PRD/HML)
        files_changed (int): Número de arquivos alterados
        insertions (int): Número de linhas adicionadas
        deletions (int): Número de linhas removidas
        message (Optional[str]): Mensagem do commit
    """
    hash: str
    author: Author
    date: datetime
    branch: str
    environment: str
    files_changed: int
    insertions: int
    deletions: int
    message: Optional[str] = None

    @property
    def total_lines(self) -> int:
        """Retorna o total de linhas alteradas (adições + remoções)."""
        return self.insertions + self.deletions

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Commit):
            return NotImplemented
        return self.hash == other.hash

    def __hash__(self) -> int:
        return hash(self.hash) 