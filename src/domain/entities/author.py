from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Author:
    """
    Representa um autor de commits no repositório.
    
    Attributes:
        name (str): Nome do autor
        email (str): Email do autor
        total_commits (Optional[int]): Total de commits do autor
    """
    name: str
    email: str
    total_commits: Optional[int] = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return NotImplemented
        return self.email == other.email

    def __hash__(self) -> int:
        return hash(self.email) 