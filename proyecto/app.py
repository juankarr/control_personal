#app.py
from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash
 
app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
 
DB_HOST = "localhost"
DB_NAME = "controlp"
DB_USER = "postgres"
DB_PASS = "admin"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
 
@app.route('/')
def home():
   
    if 'loggedin' in session:

        return render_template('home.html', username=session['username'])

    return redirect(url_for('login'))
 
@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password)
 
   
        cursor.execute('SELECT * FROM funcionarios WHERE username = %s', (username,))
      
        account = cursor.fetchone()
 
        if account:
            password_rs = account['password']
            print(password_rs)
        
            if check_password_hash(password_rs, password):
             
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
            
                return redirect(url_for('home'))
            else:
             
                flash('Usuario Incorrecto /password')
        else:
       
            flash('Incorrecto usuario/password')
 
    return render_template('login.html')
  
@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'tipo_documento' in request.form and 'documento' in request.form and 'nombre_1' in request.form and 'nombre_2' in request.form and 'apellido_1' in request.form and 'apellido_2' in request.form and 'fecha_nacimiento' in request.form and 'genero' in request.form and 'telefono' in request.form and 'estado_funcionario' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        
        tipo_documento = request.form['tipo_documento']
        documento = request.form['documento']
        nombre_1 = request.form['nombre_1']
        nombre_2 = request.form['nombre_2']
        apellido_1 = request.form['apellido_1']
        apellido_2 = request.form['apellido_2']
        fecha_nacimiento = request.form['fecha_nacimiento']
        genero = request.form['genero']
        telefono = request.form['telefono']
        estado_funcionario=request.form['estado_funcionario']
        username=request.form['username']
        password=request.form['password']
        email=request.form['email']
    
        _hashed_password = generate_password_hash(password)
 
       
        cursor.execute('SELECT * FROM funcionarios WHERE username = %s', (username,))
        account = cursor.fetchone()
        print(account)
    
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
       
            cursor.execute("INSERT INTO funcionarios (tipo_documento, documento, nombre_1, nombre_2, apellido_1, apellido_2, fecha_nacimiento, genero, telefono, estado_funcionario, username, password, email) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (tipo_documento, documento, nombre_1, nombre_2, apellido_1, apellido_2, fecha_nacimiento, genero, telefono, estado_funcionario, username, password, email))
            conn.commit()
            flash('¡Se ha registrado exitosamente!')
    elif request.method == 'POST':
      
        flash('Please fill out the form!')

    return render_template('register.html')
   
   
@app.route('/logout')
def logout():

   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)

   return redirect(url_for('login'))
  
@app.route('/profile')
def profile(): 
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
 
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM funcionarios WHERE id = %s', [session['id']])
        account = cursor.fetchone()
       
        return render_template('profile.html', account=account)
   
    return redirect(url_for('login'))
 
if __name__ == "__main__":
    app.run(debug=True)