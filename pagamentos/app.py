from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(status="ok", service="pagamentos")

@app.route("/pagamentos")
def pagamentos():
    resposta = {
        "gateway": "mock",
        "status": "aprovado",
        "mensagem": "Pagamento processado com sucesso"
    }
    return jsonify(resposta)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
