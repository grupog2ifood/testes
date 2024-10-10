from flask import Flask, flash, redirect, request, render_template, url_for
import mysql.connector
from connection import get_db_connection
from routes.usuario_routes import usuario_bp
from routes.restaurante_routes import restaurante_bp
from routes.produto_routes import produto_bp

app = Flask(__name__)
#app.config.from_pyfile('config.py')
#db = SQLAlchemy(app)
app.secret_key = 'sua_chave_secreta'  # Adicione uma chave secreta para usar flash messages

@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    nome = request.form['nome']
    cpf = request.form['cpf']
    email = request.form['email']
    celular = request.form['celular']
    telefone = request.form['telefone']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, cpf, email, celular, telefone) VALUES (%s, %s, %s, %s, %s)",
            (nome, cpf, email, celular, telefone)
        )
        conn.commit()
        flash('Usuário cadastrado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao cadastrar o usuário: {str(e)}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return render_template('cadastrar-usuario.html')

                ##Produtos 

                #Rota para cadastrar produtos
@app.route('/cadastrar-produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        restaurante_id = request.form['restaurante_id']
        produto = request.form['produto']
        preco = request.form['preco']

        # Validações e inserção no banco de dados
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute('''INSERT INTO produtos (restaurante_id, produto, preco) 
                              VALUES (%s, %s, %s)''',
                           (restaurante_id, produto, preco))
            connection.commit()
            flash('Produto cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_produto'))  # Redireciona para a lista de restaurantes após o cadastro
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

@app.route('/menu_restaurantes')
def menu_restaurantes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM restaurantes")
    restaurantes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('menu_restaurantes.html', restaurantes=restaurantes)

@app.route('/produtos/<int:restaurante_id>')
def produtos(restaurante_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM produtos WHERE restaurante_id = %s", (restaurante_id,))
    produtos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('produtos.html', produtos=produtos)

app.register_blueprint(usuario_bp)
app.register_blueprint(restaurante_bp)
app.register_blueprint(produto_bp)





if __name__ == "__main__":
    app.run(debug=True)