from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

import pandas as pd

from ...domain.entities.author import Author
from ...application.interfaces.repository_interface import GitRepositoryInterface

@dataclass
class CommitStatisticsQuery:
    """
    Query para obter estatísticas de commits.
    Segue o padrão CQS (Command Query Separation).
    """
    repository: GitRepositoryInterface
    authors: Optional[List[Author]] = None
    since: Optional[datetime] = None
    until: Optional[datetime] = None

    def execute(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Executa a query e retorna as estatísticas dos commits.
        
        Returns:
            tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: 
                - Estatísticas diárias
                - Estatísticas mensais
                - Estatísticas por branch
        """
        commits = self.repository.get_commits(
            authors=self.authors,
            since=self.since,
            until=self.until
        )

        # Converte commits para DataFrame
        commits_data = [{
            'data': commit.date,
            'nome_autor': commit.author.name,
            'email_autor': commit.author.email,
            'branch': commit.branch,
            'ambiente': commit.environment,
            'arquivos_alterados': commit.files_changed,
            'linhas_adicionadas': commit.insertions,
            'linhas_removidas': commit.deletions,
            'total_linhas': commit.total_lines,
            'commit_hash': commit.hash
        } for commit in commits]

        if not commits_data:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        df = pd.DataFrame(commits_data)

        # Estatísticas diárias
        daily_stats = df.groupby([df['data'].dt.date, 'email_autor', 'branch', 'ambiente']).agg({
            'nome_autor': 'first',
            'arquivos_alterados': 'sum',
            'linhas_adicionadas': 'sum',
            'linhas_removidas': 'sum',
            'total_linhas': 'sum',
            'commit_hash': 'count'
        }).reset_index()
        daily_stats.rename(columns={'commit_hash': 'total_commits'}, inplace=True)

        # Estatísticas mensais
        df['mes'] = df['data'].dt.to_period('M')
        monthly_stats = df.groupby(['mes', 'email_autor', 'branch', 'ambiente']).agg({
            'nome_autor': 'first',
            'arquivos_alterados': 'sum',
            'linhas_adicionadas': 'sum',
            'linhas_removidas': 'sum',
            'total_linhas': 'sum',
            'commit_hash': 'count'
        }).reset_index()
        monthly_stats.rename(columns={'commit_hash': 'total_commits'}, inplace=True)
        monthly_stats['mes'] = monthly_stats['mes'].astype(str)

        # Estatísticas por branch
        branch_stats = df.groupby(['branch', 'ambiente', 'email_autor']).agg({
            'nome_autor': 'first',
            'arquivos_alterados': 'sum',
            'linhas_adicionadas': 'sum',
            'linhas_removidas': 'sum',
            'total_linhas': 'sum',
            'commit_hash': 'count'
        }).reset_index()
        branch_stats.rename(columns={'commit_hash': 'total_commits'}, inplace=True)

        return daily_stats, monthly_stats, branch_stats 