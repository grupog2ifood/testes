from flask import Blueprint, render_template, request, redirect, flash, url_for
from connection import get_db_connection
import mysql.connector

usuario_bp = Blueprint('usuario', __name__)

# Rota para login
@usuario_bp.route("/")
def login():
    return render_template('login.html')

# Rota para cadastrar usuário
@usuario_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        email = request.form['email']
        celular = request.form['celular']
        telefone = request.form['telefone']

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Inserir os dados na tabela usuarios
            cursor.execute('''
                INSERT INTO usuarios (nome, cpf, email, celular, telefone)
                VALUES (%s, %s, %s, %s, %s)
            ''', (nome, cpf, email, celular, telefone))

            connection.commit()
            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('usuario.cadastrar_usuario'))  # Redireciona corretamente para a rota de cadastro

        except mysql.connector.IntegrityError as e:
            # Tratamento específico para erro de duplicidade de CPF ou email
            if "Duplicate entry" in str(e):
                flash("Erro: CPF ou Email já cadastrado!", 'danger')
            else:
                flash(f"Erro de integridade: {str(e)}", 'danger')
            connection.rollback()  # Reverte a transação em caso de erro

        except Exception as e:
            connection.rollback()  # Reverte a transação em caso de erro
            flash(f'Erro ao cadastrar usuário: {str(e)}', 'danger')

        finally:
            cursor.close()
            connection.close()

    return render_template('cadastrar-usuario.html')

# Rota para listar usuários
@usuario_bp.route("/listar-usuario")
def listar_usuarios():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
    return render_template("listar-usuario.html", usuarios=usuarios)

# Rota para atualizar usuário
@usuario_bp.route("/atualizar", methods=["POST"])
def atualizar_usuario():
    id = request.form["id"]
    nome = request.form["nome"]
    cpf = request.form["cpf"]
    email = request.form["email"]
    celular = request.form["celular"]
    telefone = request.form["telefone"]

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = '''
                    UPDATE usuarios SET nome=%s, cpf=%s, email=%s, celular=%s, telefone=%s WHERE id=%s
                '''
                cursor.execute(query, (nome, cpf, email, celular, telefone, id))
                conn.commit()
        flash('Usuário atualizado com sucesso!', 'success')

    except mysql.connector.Error as err:
        flash(f"Erro ao atualizar usuário: {err}", 'error')

    except Exception as err:
        flash(f"Erro inesperado: {err}", 'error')

    return redirect(url_for('usuario.listar_usuarios'))  # Redirecionar para a lista após atualizar

# Rota para excluir usuário
@usuario_bp.route("/excluir/<int:id>")
def excluir_usuario(id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM usuarios WHERE id=%s"
                cursor.execute(query, (id,))
                conn.commit()
        flash('Usuário excluído com sucesso!', 'success')

    except mysql.connector.Error as err:
        flash(f"Erro ao excluir usuário: {err}", 'error')

    except Exception as err:
        flash(f"Erro inesperado: {err}", 'error')

    return redirect(url_for('usuario.listar_usuarios'))  # Redirecionar para a lista após excluir
