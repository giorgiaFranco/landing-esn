from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2
from datetime import datetime

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id SERIAL PRIMARY KEY,
            email TEXT,
            nome TEXT,
            consenso TEXT,
            password_inserita BOOLEAN,
            created_at TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def home():
    init_db()
    return render_template("esnPage.html")


@app.route("/submit", methods=["POST"])
def submit():

    email = request.form.get("email")
    nome = request.form.get("nome")
    consenso = request.form.get("consenso")
    password = request.form.get("password")

    password_inserita = True if password else False

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO submissions
        (email, nome, consenso, password_inserita, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        email,
        nome,
        consenso,
        password_inserita,
        datetime.now()
    ))

    conn.commit()
    cur.close()
    conn.close()

    print("\n=== DATI RICEVUTI NELLA SIMULAZIONE ===")
    print("Email:", email)
    print("Nome:", nome)
    print("Consenso:", consenso)
    print("Password inserita:", password_inserita)

    return redirect(url_for("success"))


@app.route("/success")
def success():
    return """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <title>Conferma</title>
    </head>
    <body style="background:black;color:white;text-align:center;font-family:Arial;margin-top:120px;">
        <img src="https://d3k81ch9hvuctc.cloudfront.net/company/RXHQa6/images/e95da67b-21b0-49e3-a51d-ab0fe78d05b5.png" width="130">
        <h1>Ci siamo! ✅</h1>
        <p><strong>Puoi ritirare la tua goodie bag.</strong></p>
        <p>Il tuo codice sconto del 20% per il tuo primo ordine ti verrà inviato via email a breve.</p>
    </body>
    </html>
    """
@app.route("/admin")
def admin():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, email, nome, consenso, password_inserita, created_at
        FROM submissions
        ORDER BY created_at DESC;
    """)

    records = cur.fetchall()

    cur.close()
    conn.close()

    html = """
    <html>
    <head>
        <title>Admin - Simulazione</title>
        <style>
            body { font-family: Arial; background: #111; color: white; padding: 30px; }
            table { border-collapse: collapse; width: 100%; background: #222; }
            th, td { border: 1px solid #555; padding: 10px; text-align: left; }
            th { background: #333; }
        </style>
    </head>
    <body>
        <h1>Risultati simulazione</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>Email</th>
                <th>Nome</th>
                <th>Consenso</th>
                <th>Password inserita</th>
                <th>Data</th>
            </tr>
    """

    for row in records:
        html += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{row[2]}</td>
                <td>{row[3]}</td>
                <td>{'SI' if row[4] else 'NO'}</td>
                <td>{row[5]}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
