from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Função para conectar ao banco de dados MySQL
def conectar_banco():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # usuário padrão do XAMPP
        password="",  # geralmente a senha é vazia no XAMPP, a menos que você tenha configurado
        database="conexao"  # nome do banco de dados que você criou
    )
    return conn

# Rota para exibir o formulário
@app.route('/')
def formulario():
    return render_template('formulario.html')

# Rota para processar os dados do formulário
@app.route('/submit', methods=['POST'])
def submit():
    nome = request.form['nome']
    email = request.form['email']
    
    # Inserção dos dados no banco de dados MySQL
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (nome, email) VALUES (%s, %s)', (nome, email))
    conn.commit()
    conn.close()
    
    return redirect(url_for('formulario'))

# Rota para exibir os dados cadastrados
@app.route('/usuarios')
def listar_usuarios():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    
    return render_template('usuarios.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)
