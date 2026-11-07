import os
import sqlite3
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, jsonify

app = Flask(__name__)
DATABASE_PATH = 'xss.db'

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialisiert die Datenbank mit Tabellen und Beispieldaten."""
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        
    conn = get_db()
    cursor = conn.cursor()

    # --- LEVEL 1: Support Tickets ---
    cursor.execute('''
        CREATE TABLE tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            title TEXT,
            message TEXT,
            created_at TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO tickets (author, title, message, created_at)
        VALUES ('Bob Jones', 'Drucker offline', 'Der Abteilungsdrucker im 2. OG reagiert nicht.', datetime('now'))
    ''')

    # --- LEVEL 2: Shop Reviews ---
    cursor.execute('''
        CREATE TABLE reviews (
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

    # --- ANGREIFER-POSTFACH (Catcher) ---
    cursor.execute('''
        CREATE TABLE mailbox (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            received_at TEXT,
            username TEXT,
            password TEXT,
            raw_data TEXT
        )
    ''')

    conn.commit()
    conn.close()

# --- NAVIGATION ---
@app.route('/')
def index():
    return render_template('index.html')

# --- LEVEL 1: Support-Ticket-System (Stored XSS PoC) ---
@app.route('/level1', methods=['GET', 'POST'])
def level1():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        author = request.form.get('author', 'Anonym')
        title = request.form.get('title', '')
        message = request.form.get('message', '')
        
        cursor.execute(
            'INSERT INTO tickets (author, title, message, created_at) VALUES (?, ?, ?, datetime("now"))',
            (author, title, message)
        )
        conn.commit()
        return redirect(url_for('level1'))

    tickets = cursor.execute('SELECT * FROM tickets ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('level1.html', tickets=tickets)

@app.route('/level1/reset', methods=['POST'])
def level1_reset():
    init_db()
    return redirect(url_for('level1'))

# --- LEVEL 2: Webshop Review & Phishing ---
@app.route('/level2', methods=['GET', 'POST'])
def level2():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        author = request.form.get('author', 'Kunde')
        rating = request.form.get('rating', 5)
        content = request.form.get('content', '')

        cursor.execute(
            'INSERT INTO reviews (author, rating, content, created_at) VALUES (?, ?, ?, datetime("now"))',
            (author, rating, content)
        )
        conn.commit()
        return redirect(url_for('level2'))

    reviews = cursor.execute('SELECT * FROM reviews ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('level2.html', reviews=reviews)

@app.route('/level2/reset', methods=['POST'])
def level2_reset():
    init_db()
    return redirect(url_for('level2'))

# --- API CATCHER (Empfängt erbeutete Login-Daten) ---
@app.route('/api/collect', methods=['GET', 'POST'])
def api_collect():
    username = request.values.get('username', '')
    password = request.values.get('password', '')
    raw_data = str(request.values.to_dict()) if request.values else request.get_data(as_text=True)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO mailbox (received_at, username, password, raw_data) VALUES (datetime("now"), ?, ?, ?)',
        (username, password, raw_data)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Daten erfolgreich abgefangen!"
    }), 200

# --- POSTFACH DES ANGREIFERS ---
@app.route('/mailbox')
def mailbox():
    conn = get_db()
    cursor = conn.cursor()
    entries = cursor.execute('SELECT * FROM mailbox ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('mailbox.html', entries=entries)

if __name__ == '__main__':
    init_db()
    print("XSS-Lab initialisiert auf Port 5002.")
    app.run(host='0.0.0.0', port=5000, debug=True)