from typing import List, Dict, Any
from datetime import datetime
import pandas as pd
from collections import defaultdict
from domain.entities.author import Author
from infrastructure.repositories.git_repository import GitRepository

class RepositoryMetricsQuery:
    def __init__(self, repository: GitRepository):
        self.repository = repository

    def get_most_recent_name_for_email(self, commits_data: List[Dict]) -> Dict[str, str]:
        """Obtém o nome mais recente usado para cada email."""
        email_to_name = {}
        email_to_date = {}
        
        for commit in commits_data:
            email = commit['email_autor']
            date = commit['data']
            name = commit['nome_autor']
            
            if email not in email_to_date or date > email_to_date[email]:
                email_to_name[email] = name
                email_to_date[email] = date
        
        return email_to_name

    def execute(self, authors: List[Author]) -> Dict[str, Any]:
        """
        Executa a query para obter métricas do repositório.
        
        Args:
            authors: Lista de autores para analisar
            
        Returns:
            Dicionário com as métricas organizadas como na aba Resumo Geral do Excel
        """
        commits_data = []
        branch_commits = defaultdict(list)
        
        # Analisa commits em cada branch
        for branch in self.repository.get_branches():
            try:
                ambiente = 'PRD' if branch.lower() in ['main', 'master'] else 'HML'
                for commit in self.repository.repo.iter_commits(branch):
                    # Verifica se o commit é de um dos autores selecionados
                    if not any(author.email == commit.author.email for author in authors):
                        continue
                    
                    stats = commit.stats.total
                    commit_date = pd.to_datetime(commit.committed_datetime).tz_convert('UTC').tz_localize(None)
                    
                    commit_info = {
                        'data': commit_date,
                        'nome_autor': commit.author.name,
                        'email_autor': commit.author.email,
                        'branch': branch,
                        'ambiente': ambiente,
                        'arquivos': stats['files'],
                        'linhas_adicionadas': stats['insertions'],
                        'linhas_removidas': stats['deletions'],
                        'total_linhas': stats['insertions'] + stats['deletions'],
                        'commits': 1  # Cada commit conta como 1
                    }
                    
                    commits_data.append(commit_info)
                    branch_commits[branch].append(commit_info)
            except Exception as e:
                print(f"Aviso: Não foi possível analisar a branch {branch}: {str(e)}")
                continue
        
        if not commits_data:
            return {
                'resumo_autor_ambiente': [],
                'resumo_ambiente': [],
                'totais_diarios': [],
                'totais_mensais': []
            }

        # Obtém o nome mais recente para cada email
        email_to_name = self.get_most_recent_name_for_email(commits_data)
        
        # Atualiza os nomes dos autores para usar o mais recente
        for commit in commits_data:
            commit['nome_autor'] = email_to_name[commit['email_autor']]
        
        # Converte para DataFrame
        df = pd.DataFrame(commits_data)
        
        # 1. RESUMO POR AUTOR E AMBIENTE
        resumo_autor = df.groupby(['nome_autor', 'email_autor', 'ambiente']).agg({
            'commits': 'sum',
            'arquivos': 'sum',
            'linhas_adicionadas': 'sum',
            'linhas_removidas': 'sum',
            'total_linhas': 'sum',
            'branch': 'nunique'  # Conta número único de branches
        }).reset_index()
        
        # Renomeia a coluna branch para total_branches
        resumo_autor = resumo_autor.rename(columns={'branch': 'total_branches'})
        
        # 2. RESUMO POR AMBIENTE
        resumo_ambiente = df.groupby(['ambiente']).agg({
            'commits': 'sum',
            'arquivos': 'sum',
            'linhas_adicionadas': 'sum',
            'linhas_removidas': 'sum',
            'total_linhas': 'sum',
            'branch': 'nunique'  # Conta número único de branches
        }).reset_index()
        
        # Renomeia a coluna branch para total_branches
        resumo_ambiente = resumo_ambiente.rename(columns={'branch': 'total_branches'})
        
        # 3. TOTAIS DIÁRIOS
        df['data'] = df['data'].dt.strftime('%Y-%m-%d')
        totais_diarios = df.groupby(['data', 'ambiente']).agg({
            'commits': 'sum',
            'arquivos': 'sum',
            'linhas_adicionadas': 'sum',
            'linhas_removidas': 'sum',
            'total_linhas': 'sum'
        }).reset_index()
        
        # Soma os ambientes para cada dia
        totais_diarios = totais_diarios.groupby('data').agg({
            'commits': 'sum',
            'arquivos': 'sum',
            'linhas_adicionadas': 'sum',
            'linhas_removidas': 'sum',
            'total_linhas': 'sum'
        }).reset_index()
        
        totais_diarios = totais_diarios.sort_values('data', ascending=False)
        
        # 4. TOTAIS MENSAIS
        df['mes'] = pd.to_datetime(df['data']).dt.strftime('%Y-%m')
        totais_mensais = df.groupby(['mes', 'ambiente']).agg({
            'commits': 'sum',
            'arquivos': 'sum',
            'linhas_adicionadas': 'sum',
            'linhas_removidas': 'sum',
            'total_linhas': 'sum'
        }).reset_index()
        
        # Soma os ambientes para cada mês
        totais_mensais = totais_mensais.groupby('mes').agg({
            'commits': 'sum',
            'arquivos': 'sum',
            'linhas_adicionadas': 'sum',
            'linhas_removidas': 'sum',
            'total_linhas': 'sum'
        }).reset_index()
        
        totais_mensais = totais_mensais.sort_values('mes', ascending=False)
        
        return {
            'resumo_autor_ambiente': resumo_autor.to_dict('records'),
            'resumo_ambiente': resumo_ambiente.to_dict('records'),
            'totais_diarios': totais_diarios.to_dict('records'),
            'totais_mensais': totais_mensais.to_dict('records')
        } 