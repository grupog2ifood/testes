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

    @staticmethod
    def adicionar(nome, cpf, email, celular, telefone):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    query = "INSERT INTO usuarios (nome, cpf, email, celular, telefone) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(query, (nome, cpf, email, celular, telefone))
                    conn.commit()
            return True
        except mysql.connector.Error as err:
            return f"Erro ao adicionar usuário: {err}"
        except Exception as err:
            return f"Erro inesperado: {err}"

    @staticmethod
    def atualizar(id, nome, cpf, email, celular, telefone):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    query = "UPDATE usuarios SET nome=%s, cpf=%s, email=%s, celular=%s, telefone=%s WHERE id=%s"
                    cursor.execute(query, (nome, cpf, email, celular, telefone, id))
                    conn.commit()
            return True
        except mysql.connector.Error as err:
            return f"Erro ao atualizar usuário: {err}"
        except Exception as err:
            return f"Erro inesperado: {err}"

    @staticmethod
    def excluir(id):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    query = "DELETE FROM usuarios WHERE id=%s"
                    cursor.execute(query, (id,))
                    conn.commit()
            return True
        except mysql.connector.Error as err:
            return f"Erro ao excluir usuário: {err}"
        except Exception as err:
            return f"Erro inesperado: {err}"

    @staticmethod
    def listar():
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM usuarios")
                    return cursor.fetchall()
        except Exception as err:
            return f"Erro ao listar usuários: {err}"