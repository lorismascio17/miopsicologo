from flask import Flask, render_template, request, redirect, url_for, session
from oauthlib.oauth2 import WebApplicationClient
import requests

app = Flask(__name__)
app.secret_key = 'IZAZTJGIVWFSGNJJSTRFALUUCHNKRFFZ'  

# Credenziali OAuth2 (generale da Google Cloud Platform)
app.config['CLIENT_ID'] = '756315647919-v7tl6mke44ejufmb7m7oloh0pm3r8ont.apps.googleusercontent.com' 
app.config['CLIENT_SECRET'] = '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'

# ... (altre configurazioni se necessario) ... 

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

# ... (altre rotte se necessario) ...

if __name__ == '__main__':
    app.run(debug=True)