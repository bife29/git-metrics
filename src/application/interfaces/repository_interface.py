from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from domain.entities.commit import Commit
from domain.entities.author import Author

class GitRepositoryInterface(ABC):
    """
    Interface para acesso ao repositório Git.
    Segue o princípio de Inversão de Dependência (SOLID).
    """
    
    @abstractmethod
    def get_commits(self, 
                   authors: Optional[List[Author]] = None,
                   since: Optional[datetime] = None,
                   until: Optional[datetime] = None) -> List[Commit]:
        """
        Retorna lista de commits do repositório.
        
        Args:
            authors: Lista opcional de autores para filtrar
            since: Data inicial opcional
            until: Data final opcional
            
        Returns:
            List[Commit]: Lista de commits encontrados
        """
        pass

    @abstractmethod
    def get_branches(self) -> List[str]:
        """
        Retorna lista de branches do repositório.
        
        Returns:
            List[str]: Lista de nomes das branches
        """
        pass

    @abstractmethod
    def get_authors(self) -> List[Author]:
        """
        Retorna lista de autores que contribuíram com o repositório.
        
        Returns:
            List[Author]: Lista de autores
        """
        pass

    @abstractmethod
    def get_recent_author(self) -> Author:
        """
        Retorna o autor do commit mais recente.
        
        Returns:
            Author: Autor mais recente
        """
        pass 