from flask import Blueprint, render_template, request, redirect, flash, url_for
from connection import get_db_connection
import mysql.connector

restaurante_bp = Blueprint('restaurante', __name__)

@restaurante_bp.route('/cadastrar-restaurante', methods=['GET', 'POST'])
def cadastrar_restaurante():
    if request.method == 'POST':
        nome = request.form['nome']
        cnpj = request.form['cnpj']
        telefone = request.form['telefone']
        email = request.form['email']

        # Validações simples
        if not nome or not cnpj or not telefone or not email:
            flash('Todos os campos são obrigatórios!', 'danger')
            return render_template('cadastrar-restaurante.html')

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute('''INSERT INTO restaurantes (nome, cnpj, telefone, email) 
                              VALUES (%s, %s, %s, %s)''',
                           (nome, cnpj, telefone, email))
            connection.commit()
            flash('Restaurante cadastrado com sucesso!', 'success')
            return redirect(url_for('restaurante.listar_restaurante'))  # Redireciona para a lista de restaurantes após o cadastro
        except Exception as e:
            connection.rollback()
            flash(f'Erro ao cadastrar Restaurante: {str(e)}', 'danger')
        finally:
            cursor.close()
            connection.close()

    return render_template('cadastrar-restaurante.html')

@restaurante_bp.route("/listar-restaurante")
def listar_restaurante():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM restaurantes")
        restaurantes = cursor.fetchall()
    return render_template("listar-restaurante.html", restaurantes=restaurantes)

@restaurante_bp.route("/atualizar-restaurante", methods=["POST"])
def atualizar_restaurante():
    id = request.form["id"]
    nome = request.form["nome"]
    cnpj = request.form["cnpj"]
    telefone = request.form["telefone"]
    email = request.form["email"]

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "UPDATE restaurantes SET nome=%s, cnpj=%s, telefone=%s, email=%s WHERE id=%s"
                cursor.execute(query, (nome, cnpj, telefone, email, id))
                conn.commit()
        flash('Restaurante atualizado com sucesso!', 'success')
    except mysql.connector.Error as err:
        flash(f"Erro ao atualizar Restaurante: {err}", 'error')
    except Exception as err:
        flash(f"Erro inesperado: {err}", 'error')

    return redirect(url_for('restaurante.listar_restaurante'))  # Redirecionar para a lista após atualizar

@restaurante_bp.route("/excluir-restaurante/<int:id>")
def excluir_restaurante(id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Iniciar transação
                conn.start_transaction()

                # Excluir produtos associados ao restaurante
                cursor.execute("DELETE FROM produtos WHERE restaurante_id = %s", (id,))
                
                # Excluir o restaurante
                cursor.execute("DELETE FROM restaurantes WHERE id = %s", (id,))
                
                # Confirmar transação
                conn.commit()
        flash('Restaurante e seus produtos excluídos com sucesso!', 'success')
    except mysql.connector.Error as err:
        conn.rollback()
        flash(f"Erro ao excluir restaurante: {err}", 'error')
    except Exception as err:
        flash(f"Erro inesperado: {err}", 'error')

    return redirect(url_for('restaurante.listar_restaurante'))  # Redirecionar para a lista após excluir

@restaurante_bp.route('/menu/<int:restaurante_id>')
def menu(restaurante_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        # Buscar informações do restaurante
        cursor.execute("SELECT * FROM restaurantes WHERE id = %s", (restaurante_id,))
        restaurante = cursor.fetchone()

        # Buscar produtos associados ao restaurante
        cursor.execute("SELECT * FROM produtos WHERE restaurante_id = %s", (restaurante_id,))
        produtos = cursor.fetchall()
    
    return render_template("menu.html", restaurante=restaurante, produtos=produtos)
