from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(status="ok", service="pedidos")

@app.route("/pedidos")
def listar_pedidos():
    pedidos = [
        {"id": 1, "produto": "Teclado", "status": "criado"},
        {"id": 2, "produto": "Mouse", "status": "pago"},
        {"id": 3, "produto": "Monitor", "status": "em separação"}
    ]
    return jsonify(pedidos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
