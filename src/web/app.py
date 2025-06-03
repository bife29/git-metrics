from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import json
import shutil
from pathlib import Path
from git import Repo, InvalidGitRepositoryError

# Adiciona o diretório src ao PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent.parent))

from application.commands.analyze_repository import AnalyzeRepositoryCommand
from application.queries.repository_metrics import RepositoryMetricsQuery
from infrastructure.repositories.git_repository import GitRepository
from domain.entities.author import Author

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    repo_path = data.get('repository_path')
    author_emails = data.get('authors', [])
    
    if not repo_path or not author_emails:
        return jsonify({'error': 'Repository path and at least one author email are required'}), 400
    
    try:
        # Verifica se o diretório existe
        repo_path = Path(repo_path).resolve()
        if not repo_path.exists():
            return jsonify({'error': f'Directory not found: {repo_path}'}), 404
        if not (repo_path / '.git').exists():
            return jsonify({'error': f'Not a git repository: {repo_path}'}), 400
            
        # Inicializa o repositório
        repo = GitRepository(str(repo_path))
        
        # Cria a lista de autores com os emails fornecidos
        author_list = [Author(name=email.split('@')[0], email=email) for email in author_emails]
        
        # Executa a análise
        command = AnalyzeRepositoryCommand(repo)
        query = RepositoryMetricsQuery(repo)
        
        # Gera o relatório Excel
        excel_path = command.execute(author_list)
        
        # Obtém as métricas para o gráfico
        metrics = query.execute(author_list)
        
        return jsonify({
            'success': True,
            'excel_path': excel_path,
            'metrics': metrics
        })
        
    except Exception as e:
        import traceback
        print(f"Erro ao analisar repositório: {str(e)}")
        print("Traceback completo:")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/save-report', methods=['POST'])
def save_report():
    data = request.json
    download_path = data.get('download_path')
    excel_path = data.get('excel_path')
    
    if not download_path or not excel_path:
        return jsonify({'error': 'Download path and Excel path are required'}), 400
    
    try:
        # Converte os caminhos para objetos Path
        download_path = Path(download_path)
        excel_path = Path(excel_path)
        
        # Verifica se o diretório de download existe
        if not download_path.exists():
            download_path.mkdir(parents=True, exist_ok=True)
        
        # Verifica se o arquivo Excel existe
        if not excel_path.exists():
            return jsonify({'error': 'Excel file not found'}), 404
        
        # Gera o nome do arquivo no diretório de destino
        dest_file = download_path / excel_path.name
        
        # Copia o arquivo
        shutil.copy2(excel_path, dest_file)
        
        return jsonify({
            'success': True,
            'saved_path': str(dest_file)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/check-repository', methods=['POST'])
def check_repository():
    try:
        data = request.get_json()
        repository_path = data.get('repository_path')
        
        if not repository_path:
            return jsonify({'error': 'Caminho do repositório não informado'}), 400
            
        if not os.path.exists(repository_path):
            return jsonify({'error': 'Diretório não encontrado'}), 404
            
        try:
            # Tenta abrir o repositório
            repo = Repo(repository_path)
            # Verifica se é realmente um repositório Git
            if not repo.git_dir:
                raise InvalidGitRepositoryError
            
            return jsonify({'success': True})
            
        except InvalidGitRepositoryError:
            return jsonify({'error': 'O diretório não é um repositório Git válido'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list-authors', methods=['POST'])
def list_authors():
    try:
        data = request.get_json()
        repository_path = data.get('repository_path')
        
        if not repository_path:
            return jsonify({'error': 'Caminho do repositório não informado'}), 400
            
        if not os.path.exists(repository_path):
            return jsonify({'error': 'Diretório não encontrado'}), 404
            
        try:
            # Inicializa o repositório
            repo = GitRepository(repository_path)
            # Obtém a lista de autores
            authors = repo.get_authors()
            
            # Converte os autores para dicionário
            authors_list = [{'name': author.name, 'email': author.email} for author in authors]
            
            return jsonify({
                'success': True,
                'authors': authors_list
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 