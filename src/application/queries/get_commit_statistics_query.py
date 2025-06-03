from typing import List, Tuple
import pandas as pd
from datetime import datetime
from domain.entities.author import Author
from infrastructure.repositories.git_repository import GitRepository

class CommitStatisticsQuery:
    def __init__(self, repository: GitRepository, authors: List[Author]):
        self.repository = repository
        self.authors = authors

    def execute(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Executa a query para obter estatísticas de commits.
        
        Returns:
            Tuple contendo:
            - DataFrame com estatísticas diárias
            - DataFrame com estatísticas mensais
            - DataFrame com estatísticas por branch
        """
        # Inicializa as listas para armazenar os dados
        daily_data = []
        monthly_data = []
        branch_data = []

        for author in self.authors:
            commits = self.repository.get_commits_by_author(author)
            
            # Processa cada commit
            for commit in commits:
                date = commit.committed_datetime
                
                # Estatísticas do commit
                stats = {
                    'autor': str(author),  # Usa str(author) para obter o formato nome <email>
                    'data': date.date(),
                    'mes': date.strftime('%Y-%m'),
                    'arquivos_alterados': len(commit.stats.files),
                    'linhas_adicionadas': sum(f['insertions'] for f in commit.stats.files.values()),
                    'linhas_removidas': sum(f['deletions'] for f in commit.stats.files.values()),
                    'total_linhas': sum(f['lines'] for f in commit.stats.files.values()),
                    'hash': commit.hexsha[:8],
                    'mensagem': commit.message.strip(),
                    'branch': 'main',  # Simplificado para apenas main
                    'ambiente': 'PRD'   # Simplificado para apenas PRD
                }
                
                daily_data.append({**stats, 'data': stats['data']})
                monthly_data.append({**stats, 'data': stats['mes']})
                branch_data.append(stats)

        # Cria os DataFrames
        daily_df = pd.DataFrame(daily_data) if daily_data else pd.DataFrame()
        monthly_df = pd.DataFrame(monthly_data) if monthly_data else pd.DataFrame()
        branch_df = pd.DataFrame(branch_data) if branch_data else pd.DataFrame()

        # Agrupa os dados diários
        if not daily_df.empty:
            daily_df = daily_df.groupby(['data', 'autor']).agg({
                'arquivos_alterados': 'sum',
                'linhas_adicionadas': 'sum',
                'linhas_removidas': 'sum',
                'total_linhas': 'sum',
                'hash': 'count'
            }).reset_index().rename(columns={'hash': 'total_commits'})

        # Agrupa os dados mensais
        if not monthly_df.empty:
            monthly_df = monthly_df.groupby(['mes', 'autor']).agg({
                'arquivos_alterados': 'sum',
                'linhas_adicionadas': 'sum',
                'linhas_removidas': 'sum',
                'total_linhas': 'sum',
                'hash': 'count'
            }).reset_index().rename(columns={'hash': 'total_commits'})

        # Agrupa os dados por branch
        if not branch_df.empty:
            branch_df = branch_df.groupby(['autor', 'branch', 'ambiente']).agg({
                'arquivos_alterados': 'sum',
                'linhas_adicionadas': 'sum',
                'linhas_removidas': 'sum',
                'total_linhas': 'sum',
                'hash': 'count'
            }).reset_index().rename(columns={'hash': 'total_commits'})

        return daily_df, monthly_df, branch_df 