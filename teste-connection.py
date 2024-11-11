'''import mysql.connector

def test_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin',
            database='projetog2'
        )
        
        if connection.is_connected():
            print("Conexão bem-sucedida ao banco de dados!")
        
            # Realizar uma consulta simples para testar o banco
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")  # Verifica o banco de dados atual
            db_name = cursor.fetchone()
            print(f"Você está conectado ao banco de dados: {db_name[0]}")
            
            cursor.close()
            connection.close()
        else:
            print("Falha na conexão com o banco de dados!")
    
    except mysql.connector.Error as err:
        print(f"Erro ao conectar com o banco de dados: {err}")

# Testar a conexão
test_connection()
'''