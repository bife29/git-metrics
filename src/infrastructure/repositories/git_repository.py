from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

from git import Repo
from git.objects.commit import Commit as GitCommit

from ...domain.entities.commit import Commit
from ...domain.entities.author import Author
from ...domain.enums.environment_type import EnvironmentType
from ...application.interfaces.repository_interface import GitRepositoryInterface

class GitRepository(GitRepositoryInterface):
    """
    Implementação concreta do repositório Git.
    Segue o princípio de Responsabilidade Única (SOLID).
    """
    
    def __init__(self, repo_path: str):
        """
        Inicializa o repositório Git.
        
        Args:
            repo_path: Caminho para o repositório Git
        """
        self.repo_path = Path(repo_path).resolve()
        if not (self.repo_path / ".git").exists():
            raise ValueError(f"Não é um repositório git: {repo_path}")
        self.repo = Repo(str(self.repo_path))
        self._author_cache: Dict[str, Author] = {}

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
        commits = []
        author_emails = {author.email for author in authors} if authors else None
        
        for branch in self.get_branches():
            try:
                environment = EnvironmentType.from_branch(branch)
                for git_commit in self.repo.iter_commits(branch):
                    # Filtra por autor se especificado
                    if author_emails and git_commit.author.email not in author_emails:
                        continue
                        
                    # Filtra por data se especificado
                    commit_date = git_commit.committed_datetime
                    if since and commit_date < since:
                        continue
                    if until and commit_date > until:
                        continue
                    
                    # Cria ou obtém o autor do cache
                    author = self._get_or_create_author(git_commit)
                    
                    # Cria o objeto Commit
                    commit = self._create_commit(git_commit, author, branch, environment)
                    commits.append(commit)
                    
            except Exception as e:
                # Log error but continue processing other branches
                print(f"Erro ao processar branch {branch}: {str(e)}")
                continue
                
        return commits

    def get_branches(self) -> List[str]:
        """
        Retorna lista de branches do repositório.
        
        Returns:
            List[str]: Lista de nomes das branches
        """
        return [ref.name for ref in self.repo.references 
                if not ref.name.startswith('origin/')]

    def get_authors(self) -> List[Author]:
        """
        Retorna lista de autores que contribuíram com o repositório.
        
        Returns:
            List[Author]: Lista de autores
        """
        authors = {}
        for commit in self.repo.iter_commits():
            email = commit.author.email
            if email not in authors:
                authors[email] = self._get_or_create_author(commit)
        return list(authors.values())

    def get_recent_author(self) -> Author:
        """
        Retorna o autor do commit mais recente.
        
        Returns:
            Author: Autor mais recente
        """
        recent_commit = self.repo.head.commit
        return self._get_or_create_author(recent_commit)

    def _get_or_create_author(self, commit: GitCommit) -> Author:
        """
        Obtém um autor do cache ou cria um novo.
        
        Args:
            commit: Commit do Git
            
        Returns:
            Author: Objeto Author
        """
        email = commit.author.email
        if email not in self._author_cache:
            self._author_cache[email] = Author(
                name=commit.author.name,
                email=email
            )
        return self._author_cache[email]

    def _create_commit(self, git_commit: GitCommit, 
                      author: Author, branch: str,
                      environment: EnvironmentType) -> Commit:
        """
        Cria um objeto Commit a partir de um commit do Git.
        
        Args:
            git_commit: Commit do Git
            author: Autor do commit
            branch: Nome da branch
            environment: Tipo do ambiente
            
        Returns:
            Commit: Objeto Commit
        """
        stats = git_commit.stats.total
        return Commit(
            hash=git_commit.hexsha[:8],
            author=author,
            date=git_commit.committed_datetime,
            branch=branch,
            environment=str(environment),
            files_changed=stats['files'],
            insertions=stats['insertions'],
            deletions=stats['deletions'],
            message=git_commit.message.strip()
        ) 