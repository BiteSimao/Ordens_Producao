#BACKEND FLASK: ROTAS DA API REST

from flask import Flask, jsonify, request 
from flask_cors import CORS
from database import init_bd, get_connection

#Cria uma instância da aplicação Flash
app = Flask(__name__, static_folder='static', static_url_path='')

#Habilitar os CORS
CORS(app)

#ROTA N1 - Página Inicial
@app.route('/')
def index():
    #Alimentar o arquivo index.html da pasta static
    return app.send_static_file('index.html')
#ROTA N2 - Status API
@app.route('/status')
def status():
    '''Rota de verificação da API(Saúde)
    Retornar um Json informando que o servidor está ativo'''
    return jsonify({
        "status": "online",
        "sistema": "Sistema de ordem de produção",
        "versao":"1.0.0",
        "mensagem":"Olá, Fábrica, API FUNCIONANDO!"
    })
#ROTA N3 - Listar todas as ordens (GET)
@app.route('/ordens', methods=['GET'])
def listar_ordens():
    """
    LISTAR TODAS AS ORDENS DE PRODUÇÃO CADASTRADAS.
    MÉTODOS HTTP: GET
    URL: http://localhost:5000/ordens
    Retorna: Lista e ordens em formato JSON
    """
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ordens ORDER BY id DESC')
    ordens = cursor.fetchall()
    conn.close()
    
    #Converte cada Row do SQLite em dicionário Python para serializar em Json
    return jsonify([dict(o) for o in ordens ])

    
#ROTA POR ID - BUSCAR UMA ORDEM ESPECIFICA PELO ID(GET)

@app.route('/ordens/<int:ordem_id>', methods=['GET'])

def buscar_ordem(ordem_id):
    '''
    Buscar uma única ordem de produção pelo ID.
    
    Parametros de URL:
    - ordem id(int): ID da ordem a ser buscada.
    
    Retornar:
        200 + JSON da ordem, se for encontrada.
        404 + mensagem de erro, se não existir.
    '''
    conn = get_connection()
    cursor = conn.cursor()
    
    #O '?' é substituido pelo valor de ordem_id de forma segura
    cursor.execute('SELECT * FROM ordens WHERE id = ?', (ordem_id, ))
    ordem = cursor.fetchone() #Retorna um único registro ou None
    conn.close() 

    if ordem is None:
        return jsonify({'erro': f'Ordem {ordem_id} nao encontrada.'}), 404
    return jsonify(dict(ordem)), 200

#Ponto de Partida

if __name__=='__main__':
    init_bd()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
    
