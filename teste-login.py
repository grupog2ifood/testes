from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mail import Mail, Message
import os
import random
import time
from dotenv import load_dotenv
import mysql.connector
from connection import get_db_connection  # Conexão com MySQL

app = Flask(__name__)
app.secret_key = 'yoursecretkey' #echave secreta para usar flash messages
mail = Mail(app)



# Configuração da conexão com o banco de dados
def get_db_connection():
    return mysql.connector.connect(
        host="yourhost",
        user="youruser",
        password="yourpassword",
        database="yourdatabase"
    )

# Configurações do servidor de e-mail (neste exemplo, para Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'seu_email@gmail.com'  # Substitua pelo seu e-mail
app.config['MAIL_PASSWORD'] = 'sua_senha'  # Substitua pela sua senha de e-mail
app.config['MAIL_DEFAULT_SENDER'] = ('Seu Nome', 'seu_email@gmail.com')  # Remetente padrão

mail = Mail(app)

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Dicionário global para armazenar códigos de verificação temporários (para fins de exemplo)
verification_codes = {}

# Função para gerar o código de verificação
def generate_code():
    return random.randint(100000, 999999)


@app.route('/pagina-inicial')
def pagina_inicial():
    return render_template('login.html') 


@app.route('/login', methods=['GET'])
def login():
    error_message = request.args.get('error')  # Pega a mensagem de erro da URL, se houver
    return render_template('login.html', error=error_message)  # Passa a mensagem de erro para o template de login


# Rota para enviar código de verificação
@app.route('/send-code', methods=['POST'])
def send_code():
    email = request.json.get('email')

    # Verificar se o email existe no banco de dados
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM usuarios WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Usuário não encontrado!"}), 404
    
    # Gerar o código de verificação
    code = generate_code()
    expiration_time = time.time() + 300  # Código válido por 5 minutos

    # Armazenar o código e a expiração temporariamente no banco ou em memória
    verification_codes[email] = {"code": code, "expiration_time": expiration_time}

    # Enviar o código por e-mail
    msg = Message('Seu Código de Verificação', sender='seu-email@gmail.com', recipients=[email])
    msg.body = f"Seu código de verificação é: {code}"

    try:
        mail.send(msg)
        return jsonify({"message": "Código de verificação enviado para o e-mail!"}), 200
    except Exception as e:
        return jsonify({"error": "Erro ao enviar o e-mail!"}), 500
    

@app.route('/verify-code', methods=['GET', 'POST'])
def verify_code():
    if request.method == 'POST':
        email = request.form.get('email')
        code = request.form.get('code')
        
        # Conectando ao banco de dados para verificar se o email está cadastrado
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        # Se o email não estiver cadastrado no banco, retorna erro
        if not user:
            return redirect(url_for('login', error="E-mail não cadastrado. Verifique e tente novamente."))

        # Verificar se o email está no dicionário de códigos de verificação
        if email in verification_codes:
            stored_code = verification_codes[email]["code"]
            expiration_time = verification_codes[email]["expiration_time"]
            
            # Verificar se o código está expirado
            if time.time() > expiration_time:
                return redirect(url_for('login', error="O código expirou! Solicite um novo código."))

            # Verificar se o código está correto
            if code == stored_code:
                # Limpar o código após a verificação bem-sucedida
                del verification_codes[email]
                return "Logado! Seja bem-vindo"
            else:
                return redirect(url_for('login', error="Código inválido. Tente novamente."))
        else:
            return redirect(url_for('login', error="Código não encontrado. Solicite um novo código."))

    return render_template('verify-code.html')  # Exibe o formulário de verificação para método GET


if __name__ == "__main__":
    app.run(debug=True)



