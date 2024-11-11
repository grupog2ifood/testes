'''
# models/pedido.py
from database import get_db_connection

class Pedido:
    def __init__(self, usuario_id, restaurante_id, total, data_pedido):
        self.usuario_id = usuario_id
        self.restaurante_id = restaurante_id
        self.total = total
        self.data_pedido = data_pedido
        self.status = status

    @staticmethod
    def criar_pedido(usuario_id, restaurante_id, status="pendente"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pedidos (usuario_id, restaurante_id, status) VALUES (%s, %s, %s)",
            (usuario_id, restaurante_id, status)
        )
        conn.commit()
        pedido_id = cursor.lastrowid
        conn.close()
        return pedido_id

        @staticmethod
    def atualizar_status(pedido_id, novo_status):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE pedidos SET status = %s WHERE id = %s",
            (novo_status, pedido_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def obter_pedido(pedido_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pedidos WHERE id = %s", (pedido_id,))
        pedido = cursor.fetchone()
        conn.close()
        return pedido
'''