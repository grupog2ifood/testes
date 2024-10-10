'''
from flask import Flask, render_template, request, redirect, flash, url_for, session
import requests
#from flask_sqlalchemy import SQLAlchemy
from connection import get_db_connection
from models.usuario import Usuario
import mysql.connector



app = Flask(__name__)
#app.config.from_pyfile('config.py')
#db = SQLAlchemy(app)
app.secret_key = 'sua_chave_secreta'  # Adicione uma chave secreta para usar flash messages



# API Key do Google Maps 
api_key = 'AIzaSyBau5j0lo8SVyBfrBJMZzhFBIQEbB2kd2I'

# Configuração do Google OAuth

@app.route('/rota')
def index():
    return render_template('index.html')  # Página inicial com o formulário

@app.route('/rotas', methods=['POST'])  # Método POST para capturar dados do formulário
def obter_rotas():
    # Capturar os dados do formulário HTML
    origem = request.form['origem']
    destino = request.form['destino']
    
    # Endpoint da API de Direções do Google
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'origin': origem,
        'destination': destino,
        'key': 'AIzaSyBau5j0lo8SVyBfrBJMZzhFBIQEbB2kd2I',
        'mode': 'driving'
    }

    # Fazer a requisição à API do Google Maps
    response = requests.get(url, params=params)
    data = response.json()

    # Verificar se a API retornou resultados válidos
    if data['status'] == 'OK':
        rota = data['routes'][0]
        legs = rota['legs'][0]
        distancia = legs['distance']['text']
        duracao = legs['duration']['text']
        endereco_origem = legs['start_address']
        endereco_destino = legs['end_address']

        # Passar os dados para a página HTML
        return render_template('resultado.html', origem=endereco_origem, destino=endereco_destino, 
                               distancia=distancia, duracao=duracao)
    else:
        # Caso a rota não seja encontrada
        return "Não foi possível calcular a rota. Verifique os dados fornecidos."
'''