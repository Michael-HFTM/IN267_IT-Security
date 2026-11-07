import os
import sqlite3
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
DATABASE_PATH = 'xss.db'

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialisiert die Datenbank mit Standardwerten."""
    if os.path.exists(DATABASE_PATH):
        try:
            os.remove(DATABASE_PATH)
        except PermissionError:
            pass

    conn = get_db()
    cursor = conn.cursor()

    # Level 1: Reviews
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            rating INTEGER,
            content TEXT,
            created_at TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO reviews (author, rating, content, created_at)
        VALUES ('Dr. Alice Smith', 5, 'Hervorragender Lötkolben! Schnelle Aufheizzeit und präzise Temperatur.', datetime('now'))
    ''')

 # Level 2 & 3: Support-Tickets (Phishing-Szenario)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            created_at TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO tickets (message, created_at)
        VALUES (
            'Guten Tag, gilt der Rabattcode aus diesem Link auch für Firmenkunden? http://localhost:5002/product?ref=SommerSpecial2026',
            datetime('now')
        )
    ''')

    # Server Request Logs für den /logs Endpunkt
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS request_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            method TEXT,
            path TEXT,
            full_url TEXT,
            user_agent TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Request-Logging Hook: Protokolliert jeden Aufruf in der DB
@app.before_request
def log_incoming_request():
    # Statische Assets und den Log-Viewer selbst nicht rekursiv fluten
    if request.path.startswith('/static') or request.path == '/logs':
        return

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO request_logs (timestamp, method, path, full_url, user_agent)
               VALUES (datetime('now', 'localtime'), ?, ?, ?, ?)''',
            (
                request.method,
                request.path,
                request.full_path.rstrip('?'),
                request.headers.get('User-Agent', 'Unbekannt')
            )
        )
        conn.commit()
        conn.close()
    except Exception:
        pass

# --- ROUTEN ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/product', methods=['GET', 'POST'])
def product():
    conn = get_db()
    cursor = conn.cursor()

    # POST: Neues Review speichern (Level 1: Stored XSS)
    if request.method == 'POST':
        author = request.form.get('author', 'Kunde')
        rating = int(request.form.get('rating', 5))
        content = request.form.get('content', '')
        cursor.execute(
            'INSERT INTO reviews (author, rating, content, created_at) VALUES (?, ?, ?, datetime("now"))',
            (author, rating, content)
        )
        conn.commit()
        return redirect(url_for('product'))

    # GET: Reflected Parameter für Level 2 (z. B. ?ref=...)
    ref_param = request.args.get('ref', '')

    reviews = cursor.execute('SELECT * FROM reviews ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('product.html', reviews=reviews, ref_param=ref_param)

@app.route('/support', methods=['GET', 'POST'])
def support():
    if request.method == 'POST':
        message = request.form.get('message', '')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tickets (message, created_at) VALUES (?, datetime("now"))',
            (message,)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('tickets'))

    return render_template('support.html')

@app.route('/tickets')
def tickets():
    conn = get_db()
    cursor = conn.cursor()
    all_tickets = cursor.execute('SELECT * FROM tickets ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('tickets.html', tickets=all_tickets)

@app.route('/logs')
def logs():
    conn = get_db()
    cursor = conn.cursor()
    all_logs = cursor.execute('SELECT * FROM request_logs ORDER BY id DESC LIMIT 50').fetchall()
    conn.close()
    return render_template('logs.html', logs=all_logs)

@app.route('/reset', methods=['POST'])
def reset():
    init_db()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    print("XSS-Lab bereit auf http://localhost:5002")
    app.run(host='0.0.0.0', port=5000, debug=True)