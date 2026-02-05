from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(status="ok", service="estoque")

@app.route("/estoque")
def estoque():
    itens = [
        {"produto": "Teclado", "quantidade": 12},
        {"produto": "Mouse", "quantidade": 8},
        {"produto": "Monitor", "quantidade": 5}
    ]
    return jsonify(itens)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
