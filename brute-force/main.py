import hashlib
from flask import Flask, request, render_template

app = Flask(__name__)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Gehashte Passwörter
USER_DATABASE = {
    'admin1': '044f07d3e9f586bffda43c444322142ff313fc6f044c5b9ae74db00ab360f706',
    'admin2': 'a1d8529ac580b2e643526d7fda61bd8e0aa759d64092ad7886129c8eef3cc898'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if USER_DATABASE.get(username) == hash_password(password):
            return f"<h1>Herzlichen Glückwunsch! Zugriff für {username} erfolgreich gewährt.</h1>"
        else:
            message = "Ungültige Anmeldedaten. Bitte versuchen Sie es erneut."
            return render_template('login.html', message=message), 401
            
    return render_template('login.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)