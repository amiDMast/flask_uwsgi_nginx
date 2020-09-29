import random
import time
import logging
import pathlib

from flask import Flask, request, jsonify, make_response

import config

app = Flask("react_test_task_back")

logger = logging.getLogger("react_test_task_back")
formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
handler = logging.FileHandler(pathlib.Path(config.LOG_TO_DIR) / "flask_app.log")
handler.setFormatter(formatter)
handler.setLevel(config.LOG_LEVEL)
logger.addHandler(handler)
logger.setLevel(config.LOG_LEVEL)

INVOICE_PAY_METHODS = [
    {"name": "Card UAH", "id": 6},
    {"name": "Payeer", "id": 2},
    {"name": "YandexMoney Personal", "id": 3},
    {"name": "Bitcoin", "id": 4},
    {"name": "Capitalist RUB", "id": 5},
    {"name": "LiqPay UAH", "id": 7},
    {"name": "WM test", "id": 9},
    {"name": "Test 2", "id": 10},
]

WITHDRAW_PAY_METHODS = [
    {"name": "Card UAH", "id": 6},
    {"name": "YandexMoney Personal", "id": 3},
    {"name": "Bitcoin", "id": 4},
    {"name": "Приват24 UAH", "id": 8},
    {"name": "BitcoinCash", "id": 20},
    {"name": "Dash", "id": 21},
]


def error(message, status_code=400, **extra_fields):
    logger.error(message)

    return make_response(jsonify(message=message, **extra_fields), status_code)


@app.route("/payMethods", methods=["GET"])
def pay_methods():
    logger.info("received request to fetch pay methods")

    return jsonify(invoice=INVOICE_PAY_METHODS, withdraw=WITHDRAW_PAY_METHODS,)


def find_payway(base, pm_id):
    if base == "invoice":
        pms = INVOICE_PAY_METHODS
    elif base == "withdraw":
        pms = WITHDRAW_PAY_METHODS
    else:
        return

    for pm in pms:
        if pm["id"] == pm_id:
            return pm


@app.route("/payMethods/calculate", methods=["GET"])
def calculate():
    logger.info(
        "received request to calculate with data: {}".format(dict(request.args))
    )

    amount = request.args.get("amount")
    base = request.args.get("base")
    invoice_pay_method = request.args.get("invoicePayMethod")
    withdraw_pay_method = request.args.get("withdrawPayMethod")

    if (
        amount is None
        or base is None
        or invoice_pay_method is None
        or withdraw_pay_method is None
    ):
        return error("Invalid query string parameters")

    try:
        amount = float(amount)
    except ValueError:
        return error("'amount' must be a number")

    if amount <= 0:
        return error("'amount' must be a positive number")

    if base not in ("invoice", "withdraw"):
        return error("'base' must be 'invoice' or 'withdraw'")

    if (
        not invoice_pay_method.isdigit()
        or find_payway("invoice", int(invoice_pay_method)) is None
    ):
        return error("Invalid invoice pay method")

    if (
        not withdraw_pay_method.isdigit()
        or find_payway("withdraw", int(withdraw_pay_method)) is None
    ):
        return error("Invalid withdraw pay method")

    time.sleep(random.uniform(0, config.CALCULATE_WAIT_TIME))

    amount = round(amount * random.uniform(0.7, 1.3), 2)

    logger.info("calculated amount: {}".format(amount))

    return jsonify(amount=amount)


@app.route("/bids", methods=["POST"])
def create():
    if not request.is_json:
        return error("Expect Content-Type: application/json")

    if not isinstance(request.json, dict):
        return error("Invalid json structure")

    logger.info(
        "received request to create bid with data: {}".format(dict(request.args))
    )

    amount = request.json.get("amount")
    base = request.json.get("base")
    invoice_pay_method = request.json.get("invoicePayMethod")
    withdraw_pay_method = request.json.get("withdrawPayMethod")

    if (
        amount is None
        or base is None
        or invoice_pay_method is None
        or withdraw_pay_method is None
    ):
        return error("Invalid body parameters")

    try:
        amount = float(amount)
    except ValueError:
        return error("'amount' must be a number")

    if amount <= 0:
        return error("'amount' must be a positive number")

    if base not in ("invoice", "withdraw"):
        return error("'base' must be 'invoice' or 'withdraw'")

    if (
        not isinstance(invoice_pay_method, int)
        or find_payway("invoice", invoice_pay_method) is None
    ):
        return error("Invalid invoice pay method")

    if (
        not isinstance(withdraw_pay_method, int)
        or find_payway("withdraw", int(withdraw_pay_method)) is None
    ):
        return error("Invalid withdraw pay method")

    time.sleep(random.uniform(0, config.BID_CREATION_WAIT_TIME))

    logger.info(
        "created bid with params: {}".format(
            dict(
                amount=amount,
                base=base,
                invoice_pay_method=invoice_pay_method,
                withdraw_pay_method=withdraw_pay_method,
            )
        )
    )

    return jsonify(message="Success")


if __name__ == "__main__":
    app.run(port=5555, threaded=True)

