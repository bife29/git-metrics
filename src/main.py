#!/usr/bin/env python3
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console

from infrastructure.repositories.git_repository import GitRepository
from application.queries.get_commit_statistics_query import CommitStatisticsQuery
from application.commands.generate_excel_report_command import GenerateExcelReportCommand
from domain.entities.author import Author

app = typer.Typer()
console = Console()

def validate_path(path: str) -> str:
    """Valida e normaliza o caminho do repositório."""
    try:
        repo_path = Path(path).resolve()
        if not repo_path.exists():
            raise typer.BadParameter(f"Caminho do repositório não existe: {path}")
        if not (repo_path / ".git").exists():
            raise typer.BadParameter(f"Não é um repositório git: {path}")
        return str(repo_path)
    except Exception as e:
        raise typer.BadParameter(str(e))

@app.command()
def analyze(
    repo_path: str = typer.Option(..., "--path", "-p", help="Caminho do repositório git para análise"),
    author_emails: Optional[List[str]] = typer.Option(None, "--author", "-a", help="Filtrar por email(s) do(s) autor(es). Pode ser especificado múltiplas vezes.")
):
    """Analisa um repositório git e gera relatórios de contribuição em Excel e Power BI."""
    try:
        # Valida o caminho do repositório
        repo_path = validate_path(repo_path)
        
        # Inicializa o repositório
        repository = GitRepository(repo_path)
        
        # Se nenhum autor foi especificado, usa o mais recente
        if not author_emails:
            recent_author = repository.get_recent_author()
            author_emails = [recent_author.email]
            console.print(f"[yellow]Nenhum autor especificado. Usando contribuidor mais recente: {recent_author.name} ({recent_author.email})[/yellow]\n")
        
        # Obtém os autores
        authors = []
        for email in author_emails:
            # Procura o autor nos commits
            found = False
            for commit in repository.repo.iter_commits():
                if commit.author.email == email:
                    authors.append(Author(
                        name=commit.author.name,
                        email=email
                    ))
                    found = True
                    break
            
            # Se não encontrou, cria com nome desconhecido
            if not found:
                authors.append(Author(
                    name="Desconhecido",
                    email=email
                ))
        
        # Cria a query para obter estatísticas
        statistics_query = CommitStatisticsQuery(
            repository=repository,
            authors=authors
        )
        
        # Cria o comando para gerar o relatório Excel
        excel_command = GenerateExcelReportCommand(
            statistics_query=statistics_query,
            output_dir=Path("relatorios"),
            authors=authors
        )
        
        # Executa o comando e obtém o caminho do arquivo gerado
        try:
            excel_file = excel_command.execute()
            console.print(f"\n[green]Relatório Excel foi salvo como '{excel_file}'[/green]")
            
            # Exibe resumo final
            console.print("\n[bold green]Geração de relatórios concluída:[/bold green]")
            console.print(f"1. Relatório Excel: {excel_file}")
            console.print("\n[bold blue]Próximos passos:[/bold blue]")
            console.print("1. Abra o relatório Excel para análise detalhada")
            console.print("2. Use os filtros disponíveis para análises específicas")
            console.print("3. Verifique as diferentes abas para informações detalhadas")
            
        except ValueError as e:
            console.print(f"[red]Nenhum commit encontrado para os autores especificados[/red]")
            return
            
    except Exception as e:
        console.print(f"[red]Erro: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 