from web.app import app
from web.config import Config

if __name__ == '__main__':
    # Inicializa as configurações
    Config.init_app(app)
    
    # Executa a aplicação
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT) 