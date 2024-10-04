# models/usuario.py
import mysql.connector
from connection import get_db_connection

class Usuario:
    def __init__(self, nome, cpf, email, celular, telefone):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.celular = celular
        self.telefone = telefone

