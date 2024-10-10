from flask import Blueprint, render_template, request, redirect, flash, url_for
from connection import get_db_connection
import mysql.connector

produto_bp = Blueprint('produto', __name__)

# Rotas para cadastrar produtos
@produto_bp.route('/cadastrar-produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        restaurante_id = request.form['restaurante_id']  # ID do restaurante
        nome = request.form['produto']  # Nome do produto
        preco = request.form['preco']  # Preço do produto

        # Validações simples
        if not nome or not preco or not restaurante_id:
            flash('Todos os campos são obrigatórios!', 'danger')
            return redirect(url_for('produto.cadastrar_produto'))

        # Validação do preço como número
        try:
            preco = float(preco)  # Converte para float
        except ValueError:
            flash('Preço deve ser um número válido!', 'danger')
            return redirect(url_for('produto.cadastrar_produto'))

        print(f"Inserindo produto: {nome}, Preço: {preco}, Restaurante ID: {restaurante_id}")  # Debugging

        # Inserção no banco de dados
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute('''INSERT INTO produtos (nome, preco, restaurante_id) 
                              VALUES (%s, %s, %s)''',
                           (nome, preco, restaurante_id))
            connection.commit()
            flash('Produto cadastrado com sucesso!', 'success')
            return redirect(url_for('produto.listar_produto'))  # Redireciona para a lista de produtos após o cadastro
        except mysql.connector.Error as e:
            connection.rollback()
            flash(f'Erro ao cadastrar Produto: {str(e)}', 'danger')
        finally:
            cursor.close()
            connection.close()

    return render_template('cadastrar-produto.html')

@produto_bp.route("/listar-usuario")
def listar_produtos():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()
    return render_template("listar-usuario.html", produtos=produtos)

@produto_bp.route('/atualizar-produto/<int:id>', methods=['GET', 'POST'])
def atualizar_produto(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Consulta para buscar o produto pelo ID
    cursor.execute('SELECT id, nome, preco, restaurante_id FROM produtos WHERE id = %s', (id,))
    produto = cursor.fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        restaurante_id = request.form['restaurante_id']

        # Atualizando o produto no banco de dados
        cursor.execute('''
            UPDATE produtos 
            SET nome = %s, preco = %s, restaurante_id = %s 
            WHERE id = %s
        ''', (nome, preco, restaurante_id, id))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('produto_bp.listar_produto'))

    cursor.close()
    conn.close()

    return render_template('atualizar-produto.html', produto=produto)


@produto_bp.route("/excluir-produto/<int:id>")
def excluir_produto(id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM produtos WHERE id=%s"
                cursor.execute(query, (id,))
                conn.commit()
        flash('Produto excluído com sucesso!', 'success')
    except mysql.connector.Error as err:
        flash(f"Erro ao excluir produto: {err}", 'danger')
    except Exception as err:
        flash(f"Erro inesperado: {err}", 'danger')

    return redirect(url_for('produto.listar_produto'))  # Redirecionar para a lista de produtos
