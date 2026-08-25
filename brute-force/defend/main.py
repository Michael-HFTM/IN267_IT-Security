import hashlib
import time
from flask import Flask, request, render_template

app = Flask(__name__)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Gehashte Passwörter
USER_DATABASE = {
    'admin1': '044f07d3e9f586bffda43c444322142ff313fc6f044c5b9ae74db00ab360f706',
    'admin2': 'a1d8529ac580b2e643526d7fda61bd8e0aa759d64092ad7886129c8eef3cc898'
}

failed_attempts = {}  # username -> count of failed attempts
locked_until = {}     # username -> locked until (Unix-Timestamp)


def lockout_seconds(attempts: int) -> int:
    # Lock account after 3rd failed attempt: 3->5s, 4->20s, 5->45s, 6->80s ...
    if attempts < 3:
        return 0
    return 5 * (attempts - 2) ** 2


@app.route('/', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # is the account locked?
        unlock_time = locked_until.get(username, 0)
        if unlock_time > time.time():
            remaining = int(unlock_time - time.time()) + 1
            message = f"Account gesperrt. Bitte in {remaining} Sekunden erneut versuchen."
            return render_template('login.html', message=message), 429

        if USER_DATABASE.get(username) == hash_password(password):
            # Success: reset counter and lock
            failed_attempts.pop(username, None)
            locked_until.pop(username, None)
            return f"<h1>Herzlichen Glückwunsch! Zugriff für {username} erfolgreich gewährt.</h1>"
        else:
            # Failed: count attempts -> lock account
            failed_attempts[username] = failed_attempts.get(username, 0) + 1
            count = failed_attempts[username]
            if count >= 3:
                locked_until[username] = time.time() + lockout_seconds(count)
            message = "Ungültige Anmeldedaten. Bitte versuchen Sie es erneut."
            return render_template('login.html', message=message), 401

    return render_template('login.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
