# models/usuario.py
import mysql.connector
from connection import get_db_connection

class Restaurante:
    def __init__(self, nome, cnpj, telefone, email):
        self.nome = nome
        self.cpf = cnpj
        self.telefone = telefone
        self.email = email



