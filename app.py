from flask import Flask, render_template, request, redirect, flash, url_for
from connection import get_db_connection
from models.usuario import Usuario
import mysql.connector

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Adicione uma chave secreta para usar flash messages


#Rota para Login

@app.route("/")
def login():
    return ("olá")


# Rota inicial (Página de Cadastro)
@app.route("/cadastro")
def index():
    return render_template("cadastrar.html")

# Rota para listar usuários
@app.route("/listar-usuarios")
def listar_usuarios():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
    return render_template("listar.html", usuarios=usuarios)

# Rota para cadastrar
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        email = request.form['email']
        celular = request.form['celular']
        telefone = request.form['telefone']

        # Validações e inserção no banco de dados
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute('''INSERT INTO usuarios (nome, cpf, email, celular, telefone) 
                              VALUES (%s, %s, %s, %s, %s)''',
                           (nome, cpf, email, celular, telefone))
            connection.commit()
            flash('Usuário cadastrado com sucesso!', 'success')
        except Exception as e:
            connection.rollback()
            flash(f'Erro ao cadastrar usuário: {str(e)}', 'danger')
        finally:
            cursor.close()
            connection.close()

        #return redirect('/listar-usuarios')  # Redireciona para a lista de usuários após o cadastro

    return render_template('cadastrar.html')

# Rota para atualizar usuário
@app.route("/atualizar", methods=["POST"])
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
                query = "UPDATE usuarios SET nome=%s, cpf=%s, email=%s, celular=%s, telefone=%s WHERE id=%s"
                cursor.execute(query, (nome, cpf, email, celular, telefone, id))
                conn.commit()
        flash('Usuário atualizado com sucesso!', 'success')
    except mysql.connector.Error as err:
        flash(f"Erro ao atualizar usuário: {err}", 'error')
    except Exception as err:
        flash(f"Erro inesperado: {err}", 'error')

    return redirect(url_for('listar_usuarios'))  # Redirecionar para a lista após atualizar

# Rota para excluir usuário
@app.route("/excluir/<int:id>")
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

    return redirect(url_for('listar_usuarios'))  # Redirecionar para a lista após excluir



if __name__ == "__main__":
    app.run(debug=True)