from flask import Flask, jsonify, request
import requests
import logging
import json
import time

app = Flask(__name__)

SERVICOS = {
    "pedidos": "http://pedidos:5000/pedidos",
    "pagamentos": "http://pagamentos:5000/pagamentos",
    "estoque": "http://estoque:5000/estoque"
}

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "level": record.levelname,
            "service": "gateway",
            "message": record.getMessage()
        }
        if hasattr(record, "extra"):
            log.update(record.extra)
        return json.dumps(log)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())

logger = logging.getLogger("gateway")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

logging.getLogger("werkzeug").setLevel(logging.WARNING)


@app.route("/health")
def health():
    logger.info(
        "health check",
        extra={"extra": {"route": "/health"}}
    )
    return jsonify(status="ok", service="gateway")


def proxy(service_name):
    start_time = time.time()
    url = SERVICOS[service_name]

    logger.info(
        "request received",
        extra={"extra": {
            "route": request.path,
            "method": request.method,
            "target_service": service_name
        }}
    )

    try:
        response = requests.get(url, timeout=3)
        duration_ms = int((time.time() - start_time) * 1000)

        logger.info(
            "request forwarded",
            extra={"extra": {
                "route": request.path,
                "target_service": service_name,
                "status_code": response.status_code,
                "duration_ms": duration_ms
            }}
        )

        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        duration_ms = int((time.time() - start_time) * 1000)

        logger.error(
            "service unavailable",
            extra={"extra": {
                "route": request.path,
                "target_service": service_name,
                "error": str(e),
                "duration_ms": duration_ms
            }}
        )

        return jsonify(error="Service unavailable"), 502


@app.route("/pedidos")
def pedidos():
    return proxy("pedidos")


@app.route("/pagamentos")
def pagamentos():
    return proxy("pagamentos")


@app.route("/estoque")
def estoque():
    return proxy("estoque")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
