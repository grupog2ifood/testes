import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='yourhost',
            user='youruser',
            password='yourpassword',
            database='yourdatabase'
        )
        if connection.is_connected():
            print("Conexão bem-sucedida ao banco de dados!")
        else:

            print("Falha na conexão com o banco de dados!")
        return connection
    
    except mysql.connector.Error as err:
        print(f"Erro ao conectar com o banco de dados: {err}")
        return None
