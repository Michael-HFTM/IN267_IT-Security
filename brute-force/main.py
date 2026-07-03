from flask import Flask, request, render_template_string

app = Flask(__name__)

# Der Ziel-Account mit einem Passwort aus den klassischen Top-Listen
USER_DATABASE = {
    'admin': 'shadow1' 
}

HTML_LOGIN = '''
<!doctype html>
<title>Admin Login Portal</title>
<div style="max-width: 400px; margin: 50px auto; font-family: sans-serif; line-height: 1.5;">
    <h2>Unternehmens-Admin-Login</h2>
    <p style="background: #f4f4f4; padding: 10px; border-left: 5px solid #007BFF;">
        <strong>Mission für Studierende:</strong> Finden Sie das Passwort des Benutzers "admin" heraus. Nutzen Sie dafür ein automatisiertes Skript.
    </p>
    <form method="POST">
      Benutzername: <input type="text" name="username" value="admin" readonly style="background: #eee;"><br><br>
      Passwort: <input type="password" name="password" autofocus><br><br>
      <input type="submit" value="Einloggen" style="padding: 5px 15px;">
    </form>
    {% if message %}
        <p style="color: red; font-weight: bold;">{{ message }}</p>
    {% endif %}
</div>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if USER_DATABASE.get(username) == password:
            return "<h1>FLAG{brut3_f0rc3_succ3ssful_992} - Zugriff gewährt!</h1>"
        else:
            message = "Falsches Passwort!"
            
    return render_template_string(HTML_LOGIN, message=message)

if __name__ == '__main__':
    # host='0.0.0.0' sorgt dafür, dass Flask Verbindungen von außerhalb des Containers annimmt
    app.run(host='0.0.0.0', port=5000, debug=True)