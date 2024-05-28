from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from flask import send_from_directory


app = Flask(__name__)

# Serve i file statici dalla cartella 'static'
app.config['STATIC_FOLDER'] = 'static' 
app.config['UPLOAD_FOLDER'] = 'uploads'


# Configurazione Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Sostituisci con il tuo server SMTP
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_password'

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chi_sono')
def chi_sono():
    return render_template('chi_sono.html')

@app.route('/consulenze')
def consulenze():
    return render_template('consulenze.html')

@app.route('/articoli')
def articoli():
    return render_template('articoli.html')

@app.route('/contatti')
def contatti():
    return render_template('contatti.html')

@app.route('/recensioni')
def recensioni():
    return render_template('recensioni.html')

@app.route('/domande')
def domande():
    return render_template('domande.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    # Invia l'email
    msg = Message(
        'Nuovo messaggio dal sito web',
        sender='your_email@example.com',
        recipients=['your_email@example.com']
    )
    msg.body = f'Nome: {name}\nEmail: {email}\nTelefono: {phone}\nMessaggio: {message}'
    mail.send(msg)

    # Mostra un messaggio di conferma all'utente
    return render_template('confirmation.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    return render_template('index.html')

# Serve i file statici dalla cartella 'static'
app.config['STATIC_FOLDER'] = 'static' 

@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

