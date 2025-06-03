#!/usr/bin/env python3
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console

from infrastructure.repositories.git_repository import GitRepository
from application.queries.get_commit_statistics_query import CommitStatisticsQuery
from application.commands.generate_excel_report_command import GenerateExcelReportCommand
from domain.entities.author import Author
from application.commands.analyze_repository import AnalyzeRepositoryCommand

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
    path: str = typer.Option(None, "--path", "-p", help="Caminho do repositório Git"),
    repository_path: str = typer.Argument(None, help="Caminho do repositório Git"),
    author_emails: Optional[List[str]] = typer.Option(
        None,
        "--author",
        "-a",
        help="Email do autor para filtrar (pode ser usado múltiplas vezes)"
    )
):
    """
    Analisa um repositório git e gera relatórios de contribuição em Excel.
    
    Args:
        path: Caminho do repositório Git (via opção --path)
        repository_path: Caminho do repositório Git (via argumento posicional)
        author_emails: Lista de emails dos autores para filtrar
    """
    try:
        # Usa --path se fornecido, senão usa o argumento posicional
        repo_path = path if path else repository_path
        if not repo_path:
            console.print("[red]Erro: Caminho do repositório não fornecido. Use --path ou forneça o caminho como argumento.[/red]")
            raise typer.Exit(1)
            
        # Valida o caminho
        repo_path = validate_path(repo_path)
        
        # Inicializa o repositório
        repository = GitRepository(repo_path)
        
        # Se não foram especificados autores, usa todos do repositório
        if not author_emails:
            authors = repository.get_authors()
        else:
            # Filtra apenas os autores especificados
            all_authors = {author.email: author.name for author in repository.get_authors()}
            authors = []
            
            for email in author_emails:
                if email in all_authors:
                    authors.append(Author(name=all_authors[email], email=email))
                else:
                    # Procura por correspondência parcial
                    found = False
                    for repo_email, name in all_authors.items():
                        if email.lower() in repo_email.lower() or email.lower() in name.lower():
                            authors.append(Author(name=name, email=repo_email))
                            found = True
                            break
                    
                    if not found:
                        console.print(f"[yellow]Aviso: Autor '{email}' não encontrado no repositório[/yellow]")
        
        if not authors:
            console.print("[red]Erro: Nenhum autor válido encontrado[/red]")
            raise typer.Exit(1)
        
        # Executa a análise
        command = AnalyzeRepositoryCommand(repository)
        excel_path = command.execute(authors)
        
        # Exibe resultado
        console.print("\n[green]Análise concluída com sucesso![/green]")
        console.print(f"\nArquivos gerados:")
        console.print(f"1. Relatório Excel: {excel_path}")
        
    except Exception as e:
        console.print(f"[red]Erro: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 