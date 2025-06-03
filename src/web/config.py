"""
Configurações para o servidor web.
"""
import os
from pathlib import Path
from flask import Flask

class Config:
    """Configurações da aplicação web."""
    
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-padrao'
    
    # Diretório base do projeto
    BASE_DIR = Path(__file__).parent.parent.parent
    
    # Diretório para salvar relatórios
    REPORTS_DIR = BASE_DIR / 'reports'
    
    # Configurações do Flask
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    DEBUG = FLASK_ENV == 'development'
    
    # Configurações de upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    
    # Configurações do servidor
    HOST = os.getenv('GIT_METRICS_HOST', '0.0.0.0')
    PORT = int(os.getenv('GIT_METRICS_PORT', '5000'))
    DEBUG_SERVER = os.getenv('GIT_METRICS_DEBUG', 'False').lower() == 'true'
    
    @staticmethod
    def init_app(app: Flask):
        """
        Inicializa as configurações da aplicação Flask.
        
        Args:
            app: Instância da aplicação Flask
        """
        # Cria o diretório de relatórios se não existir
        os.makedirs(str(Config.REPORTS_DIR), exist_ok=True)
        
        # Configurações básicas
        app.config['SECRET_KEY'] = os.getenv('GIT_METRICS_SECRET_KEY', 'dev')
        
        # Configurações de template
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        
        # Configurações de upload
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
        
        # Configurações de sessão
        app.config['SESSION_TYPE'] = 'filesystem'
        
        # Configurações de cache
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 