from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
from oauthlib.oauth2 import WebApplicationClient
import requests

app = Flask(__name__)
app.secret_key = 'IZAZTJGIVWFSGNJJSTRFALUUCHNKRFFZ'  

# Credenziali OAuth2 (generale da Google Cloud Platform)
app.config['CLIENT_ID'] = '756315647919-v7tl6mke44ejufmb7m7oloh0pm3r8ont.apps.googleusercontent.com' 
app.config['CLIENT_SECRET'] = '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'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'marina.lumento@gmail.com' 
app.config['MAIL_PASSWORD'] = 'akhv lzyi qzal ziiy'  # Sostituisci con la tua password specifica

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    client = WebApplicationClient(app.config['CLIENT_ID'])
    redirect_uri = url_for('authorize', _external=True)
    authorization_url, state = client.prepare_request_uri(
        'https://accounts.google.com/o/oauth2/auth',
        redirect_uri=redirect_uri,
        scope=['https://mail.google.com/'],
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/authorize')
def authorize():
    client = WebApplicationClient(app.config['CLIENT_ID'])
    token = client.parse_request_uri(request.url)
    if token is None:
        return render_template('error.html', message='Errore durante l\'autenticazione OAuth2.')

    credentials = client.get_access_token(
        'https://www.googleapis.com/oauth2/v4/token',
        state=session['state'],
        token=token,
    )
    session['access_token'] = credentials['access_token']
    return redirect(url_for('home'))

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    # Invia l'email
    msg = Message(
        'Nuovo messaggio dal sito web',
        sender='marina.lumento@gmail.com',
        recipients=['marina.lumento@gmail.com']
    )
    msg.body = f'Nome: {name}\nEmail: {email}\nTelefono: {phone}\nMessaggio: {message}'
    mail.send(msg)

    return render_template('confirmation.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
