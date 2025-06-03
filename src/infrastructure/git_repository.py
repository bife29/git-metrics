from datetime import datetime
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
from git.objects.commit import Commit
from domain.entities.author import Author

from git import Repo

class GitRepository:
    def __init__(self, path: str):
        """
        Inicializa o repositório Git.
        
        Args:
            path: Caminho para o repositório Git
        """
        self.path = Path(path).resolve()
        self.repo = Repo(str(self.path))
        self._authors_cache = None
    
    def get_all_authors(self) -> List[Tuple[str, str]]:
        """
        Retorna todos os autores do repositório com seus emails.
        
        Returns:
            Lista de tuplas (nome, email) de todos os autores
        """
        if self._authors_cache is None:
            authors = set()
            for commit in self.repo.iter_commits():
                authors.add((commit.author.name, commit.author.email))
            self._authors_cache = list(authors)
        return self._authors_cache

    def find_author_variations(self, author) -> List[Tuple[str, str]]:
        """
        Encontra todas as variações de um autor no repositório.
        
        Args:
            author: Objeto Author para buscar
            
        Returns:
            Lista de tuplas (nome, email) que correspondem ao autor
        """
        variations = []
        search_email = author.email.lower() if author.email else None
        search_name = author.name.lower() if author.name else None
        
        for name, email in self.get_all_authors():
            name_lower = name.lower()
            email_lower = email.lower()
            
            # Correspondência exata por email
            if search_email and search_email == email_lower:
                variations.append((name, email))
                continue
                
            # Correspondência por nome se não encontrou por email
            if search_name and search_name == name_lower:
                variations.append((name, email))
                continue
                
            # Correspondência parcial por email (se o email do autor estiver contido)
            if search_email and search_email in email_lower:
                variations.append((name, email))
                continue
                
            # Correspondência parcial por nome (se o nome do autor estiver contido)
            if search_name and search_name in name_lower:
                variations.append((name, email))
        
        return variations
        
    def get_commits_by_author(self, author: Author) -> List[Commit]:
        """
        Retorna todos os commits feitos por um autor específico.
        """
        commits = []
        for branch in self.get_all_branches():
            try:
                for commit in self.repo.iter_commits(branch):
                    if commit.author.email == author.email:
                        commits.append(commit)
            except:
                print(f"Aviso: Não foi possível analisar a branch {branch}")
        return commits

    def get_all_branches(self) -> List[str]:
        """
        Retorna lista de todas as branches do repositório.
        Exclui referências remotas (origin/).
        """
        return [ref.name for ref in self.repo.references if not ref.name.startswith('origin/')]

    def classify_branch(self, branch_name: str) -> str:
        """
        Classifica a branch como PRD ou HML.
        PRD: main ou master
        HML: todas as outras
        """
        if branch_name.lower() in ['main', 'master']:
            return 'PRD'
        return 'HML'

    def get_recent_developer(self) -> tuple[str, str]:
        """
        Obtém o desenvolvedor mais recente que fez commit no repositório.
        Retorna uma tupla (nome, email).
        """
        recent_commit = self.repo.head.commit
        return recent_commit.author.name, recent_commit.author.email
    
    def get_commit_count_by_author(self, author) -> int:
        """
        Retorna o número total de commits de um autor.
        
        Args:
            author: Objeto Author
            
        Returns:
            Número total de commits
        """
        return len(self.get_commits_by_author(author))
    
    def get_lines_changed_by_author(self, author) -> int:
        """
        Retorna o número total de linhas alteradas por um autor.
        
        Args:
            author: Objeto Author
            
        Returns:
            Número total de linhas alteradas
        """
        total_lines = 0
        for commit in self.get_commits_by_author(author):
            for file in commit.stats.files:
                total_lines += commit.stats.files[file]['lines']
        return total_lines
    
    def get_file_types_by_author(self, author) -> dict:
        """
        Retorna um dicionário com a contagem de tipos de arquivo modificados pelo autor.
        
        Args:
            author: Objeto Author
            
        Returns:
            Dicionário com contagem de tipos de arquivo
        """
        file_types = {}
        for commit in self.get_commits_by_author(author):
            for file in commit.stats.files:
                extension = file.split('.')[-1] if '.' in file else 'other'
                file_types[extension] = file_types.get(extension, 0) + 1
        return file_types 