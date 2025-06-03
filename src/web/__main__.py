from web.app import app
from web.config import Config

def main():
    """
    Função principal para iniciar o servidor web.
    Configura e inicia o servidor Flask com as configurações apropriadas.
    """
    # Inicializa as configurações
    Config.init_app(app)
    
    # Executa a aplicação
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )

if __name__ == "__main__":
    main() 