from flask import Flask, render_template, request, redirect, flash, url_for
#from flask_sqlalchemy import SQLAlchemy
from connection import get_db_connection
from models.usuario import Usuario
import mysql.connector


app = Flask(__name__)
#app.config.from_pyfile('config.py')
#db = SQLAlchemy(app)
app.secret_key = 'sua_chave_secreta'  # Adicione uma chave secreta para usar flash messages


# Rota para Login
@app.route("/")
def login():
    return render_template('login.html')


# Rota para cadastrar usuário
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        email = request.form['email']
        celular = request.form['celular']
        telefone = request.form['telefone']

        # Validações e inserção no banco de dados\
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute('''INSERT INTO usuarios (nome, cpf, email, celular, telefone)
                              VALUES (%s, %s, %s, %s, %s)''',
                           (nome, cpf, email, celular, telefone))
            connection.commit()
            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_usuarios'))  # Redireciona para a lista de usuários após o cadastro
        except Exception as e:
            connection.rollback()
            flash(f'Erro ao cadastrar usuário: {str(e)}', 'danger')
        finally:
            cursor.close()
            connection.close()

    return render_template('cadastrar-usuario.html')


# Rota para listar usuários
@app.route("/listar-usuario")
def listar_usuarios():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
    return render_template("listar-usuario.html", usuarios=usuarios)


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


'''                                  Restaurantes                                 '''

# Rota para cadastrar restaurante
@app.route('/cadastrar-restaurante', methods=['GET', 'POST'])
def cadastrar_restaurante():
    if request.method == 'POST':
        nome = request.form['nome']
        cnpj = request.form['cnpj']
        telefone = request.form['telefone']
        email = request.form['email']

        # Validações e inserção no banco de dados
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute('''INSERT INTO restaurantes (nome, cnpj, telefone, email) 
                              VALUES (%s, %s, %s, %s)''',
                           (nome, cnpj, telefone, email))
            connection.commit()
            flash('Restaurante cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_restaurante'))  # Redireciona para a lista de restaurantes após o cadastro
        except Exception as e:
            connection.rollback()
            flash(f'Erro ao cadastrar Restaurante: {str(e)}', 'danger')
        finally:
            cursor.close()
            connection.close()

    return render_template('cadastrar-restaurante.html')


# Rota para listar restaurantes
@app.route("/listar-restaurante")
def listar_restaurante():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM restaurantes")
        restaurantes = cursor.fetchall()
    return render_template("listar-restaurante.html", restaurantes=restaurantes)


# Rota para atualizar restaurante
@app.route("/atualizar-restaurante", methods=["POST"])
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

    return redirect(url_for('listar_restaurante'))  # Redirecionar para a lista após atualizar


# Rota para excluir restaurante
@app.route("/excluir-restaurante/<int:id>")
def excluir_restaurante(id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM restaurantes WHERE id=%s"
                cursor.execute(query, (id,))
                conn.commit()
        flash('Restaurante excluído com sucesso!', 'success')
    except mysql.connector.Error as err:
        flash(f"Erro ao excluir restaurante: {err}", 'error')
    except Exception as err:
        flash(f"Erro inesperado: {err}", 'error')

    return redirect(url_for('listar_restaurante'))  # Redirecionar para a lista após excluir


'''                                         Produtos                                 '''


#Rota para cadastrar produtos
@app.route('/cadastrar-produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        restaurante = request.form['restaurante']
        produto = request.form['produto']
        preco = request.form['preco']

        # Validações e inserção no banco de dados
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute('''INSERT INTO produtos (restaurante, produto, preco) 
                              VALUES (%s, %s, %s)''',
                           (restaurante, produto, preco))
            connection.commit()
            flash('Produto cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_produtos'))  # Redireciona para a lista de restaurantes após o cadastro
        except Exception as e:
            connection.rollback()
            flash(f'Erro ao cadastrar Produto: {str(e)}', 'danger')
        finally:
            cursor.close()
            connection.close()

    return render_template('cadastrar-produto.html')

# Rota para listar produtos
@app.route("/listar-produto")
def listar_produto():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()
    return render_template("listar-produto.html", produtos=produtos)

# Rota para atualizar restaurante
@app.route("/atualizar-produto", methods=["POST"])
def atualizar_produto():
    id = request.form["id"]
    restaurante = request.form["restaurante"]
    produto = request.form["produto"]
    preco = request.form["preco"]

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "UPDATE produtos SET restaurante=%s, produto=%s, preco=%s WHERE id=%s"
                cursor.execute(query, (restaurante, produto, preco, id))
                conn.commit()
        flash('Produto atualizado com sucesso!', 'success')
    except mysql.connector.Error as err:
        flash(f"Erro ao atualizar Restaurante: {err}", 'error')
    except Exception as err:
        flash(f"Erro inesperado: {err}", 'error')

    return redirect(url_for('listar_produto'))  # Redirecionar para a lista após atualizar

@app.route("/excluir-produto/<int:id>")
def excluir_produto(id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM produtos WHERE id=%s"
                cursor.execute(query, (id,))
                conn.commit()
        flash('Produto excluído com sucesso!', 'success')
    except mysql.connector.Error as err:
        flash(f"Erro ao excluir produto: {err}", 'error')
    except Exception as err:
        flash(f"Erro inesperado: {err}", 'error')

    return redirect(url_for('listar_produto'))  # Redirecionar para a lista após excluir

if __name__ == "__main__":
    app.run(debug=True)