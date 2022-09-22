import os
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlalchemy.sql import func
from datetime import date

from transaction import Transaction

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


conn = sqlite3.connect('prod_mpesa_db.db', check_same_thread=False,  timeout=15, isolation_level=None)
#, timeout=15, isolation_level=None
conn.execute('pragma journal_mode=wal')

amount_to_milliters = 10
milliters_to_seconds = 67
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS transactions (
        created_at text,
        guid text,
        amount text,
        milliliters text,
        timestamp text,
        status text,
        receipt text
)""")



def insert_transaction(transaction):
    with conn:
        c.execute("INSERT INTO transactions VALUES (:created_at, :guid, :amount, :milliliters, :timestamp, :status, :receipt)", {'created_at': transaction.created_at, 'guid': transaction.guid, 'amount': transaction.amount, 'milliliters': transaction.milliliters, 'timestamp': transaction.timestamp,'status': transaction.status, 'receipt': transaction.receipt })
def find_all():
    #with conn:
        c.execute("SELECT * FROM transactions")
        return c.fetchall()
def find_by_guid(guid):
    #with conn:
        c.execute("SELECT * FROM transactions WHERE guid=:guid", {'guid': guid})
        return c.fetchone()


@app.route('/api/v1/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"


@app.route("/query_transaction/<string:transaction_guid>",  methods=['GET', 'POST'])
def transaction(transaction_guid):
    print(transaction_guid)
    print("added")
    transaction = find_by_guid(transaction_guid)
    return jsonify(response = transaction, code = '200')


@app.route('/create_transaction', methods=['POST'])
def createTransaction():

    new_invoice = Transaction("20220226153456", "bba5156f-1ab5-4a29-89a8-5267cae105b5", "50", "50", "20220226153456", "0", "QLG45GW091")
    print(new_invoice.created_at)
    insert_transaction(new_invoice)

@app.route('/request_qr', methods=['POST'])
def requestQR():
    amount = request.json['amount']
    amountInt = int(amount)
    milliters = amountInt * amount_to_milliters
    seconds = amount_to_milliters * milliters
    guid = request.json['guid']
    print("qr request : " + amount + "  " + guid)
    ## Create transaction
    new_invoice = Transaction("20220226153456", guid, amount, milliters, "20220226153456", "2", "QLG45GW091")
    print(new_invoice.created_at)
    insert_transaction(new_invoice)
    qr_code = "iVBORw0KGgoAAAANSUhEUgAAASwAAAEsCAIAAAD2HxkiAAAHtElEQVR42u3d23rqIBAGUN//pbNv91c1cpwMsP7L1lgSZ uUAaF+XiDyal0MgAqEIhCICoQiEIgKhCIQiAqEIhCICoQiEu+zbf2l7wfvLyl/Z/Cc62/Btk8Ktag/Ot7/1LeWbQLgbwo+ dWtLlVfVxj7AZWEON9hf34wjPoQjhXIRDLsi11TmkspMgPMHhQQjfu7MZYRWnSQhrr6u1lZ0H4fYOIazg8QjCIW3odDX8a bxqryHcCuGf7oxB2AljIMJ5AzPDEQ7cEQjTISy/Rr1v1fyQ2Yywsw09Ffw4wnMcHjRF0YOwZ5NRCCc9Q0II4QMICyfxBiL 8eAq4//kMhPOmKCCEsLQLyxG2jTHW/qptcKJhjHT2FAWEEFYj/DnIEfOr/utq84QhhBA+g/DPxTAS4f1DaW0J9i9hq1pzA yGEUxAWTl1UzSMPnPGbNJcNIYTPI7wq5w/XQjhw8s08IYQTEV6/JtMmIfx2M9wwstI8ZrMKQitmjkbY8+GjUQhHteH+5NL wGNmzhjbmfhvCZRBeZRMA8xAOuV5N/YhQHoTX7oEwFOFVP8s36qF3yIBqPMLrgPhkfcsH4Xs2H/jYVnvL3TyO+gjC65j4j hEIFQBEIRgVAEQhGBUARCEYFQB EIRgVAEQhl0cD99bUnP15zMeM3PP73uP1qBkMBXMMIeVw1N1cUQLiNwFML715S/4YxXCoSpBRbWa+c94fuvSmjVnkc4hHA 9foXFWnsZvEHY9sO222k9DuEaApvL/f6dm8FACOEpIzGjEJa8ZzPC8ntgAiFcCWHzo9fPt+1HWDvWYlQGwsUQ9ox/9MAeh dA8IYQ73532XwaHI/zGzJUQQgi/XiSHPBOWt8QzIYSbI6wVGIzQ6CiEEFb8Mz0IIZRlEM54pUAI4e/b11FDOBBCuA/CtlK etHa0fMjUGCmEEPoUBYSSFeE14vOEPa8UCCGse+dyVATOzj9sNbb7uEGwmwAAAABJRU5ErkJggg=="
    payload = {'qr_code': qr_code, 'seconds': seconds}
    
    return jsonify(response = payload, code = '200')


@app.route('/callback', methods=['POST'])
def mpesaCallback():
    amount = request.json['amount']
    guid = request.json['guid']
    print("qr request : " + amount + "  " + guid)
    ## Create transaction
    new_invoice = Transaction("20220226153456", guid, amount, milliters, "20220226153456", "2", "QLG45GW091")
    print(new_invoice.created_at)
    insert_transaction(new_invoice)
    qr_code = "iVBORw0KGgoAAAANSUhEUgAAASwAAAEsCAIAAAD2HxkiAAAHtElEQVR42u3d23rqIBAGUN//pbNv91c1cpwMsP7L1lgSZ uUAaF+XiDyal0MgAqEIhCICoQiEIgKhCIQiAqEIhCICoQiEu+zbf2l7wfvLyl/Z/Cc62/Btk8Ktag/Ot7/1LeWbQLgbwo+ dWtLlVfVxj7AZWEON9hf34wjPoQjhXIRDLsi11TmkspMgPMHhQQjfu7MZYRWnSQhrr6u1lZ0H4fYOIazg8QjCIW3odDX8a bxqryHcCuGf7oxB2AljIMJ5AzPDEQ7cEQjTISy/Rr1v1fyQ2Yywsw09Ffw4wnMcHjRF0YOwZ5NRCCc9Q0II4QMICyfxBiL 8eAq4//kMhPOmKCCEsLQLyxG2jTHW/qptcKJhjHT2FAWEEFYj/DnIEfOr/utq84QhhBA+g/DPxTAS4f1DaW0J9i9hq1pzA yGEUxAWTl1UzSMPnPGbNJcNIYTPI7wq5w/XQjhw8s08IYQTEV6/JtMmIfx2M9wwstI8ZrMKQitmjkbY8+GjUQhHteH+5NL wGNmzhjbmfhvCZRBeZRMA8xAOuV5N/YhQHoTX7oEwFOFVP8s36qF3yIBqPMLrgPhkfcsH4Xs2H/jYVnvL3TyO+gjC65j4j hEIFQBEIRgVAEQhGBUARCEYFQB EIRgVAEQhl0cD99bUnP15zMeM3PP73uP1qBkMBXMMIeVw1N1cUQLiNwFML715S/4YxXCoSpBRbWa+c94fuvSmjVnkc4hHA 9foXFWnsZvEHY9sO222k9DuEaApvL/f6dm8FACOEpIzGjEJa8ZzPC8ntgAiFcCWHzo9fPt+1HWDvWYlQGwsUQ9ox/9MAeh dA8IYQ73532XwaHI/zGzJUQQgi/XiSHPBOWt8QzIYSbI6wVGIzQ6CiEEFb8Mz0IIZRlEM54pUAI4e/b11FDOBBCuA/CtlK etHa0fMjUGCmEEPoUBYSSFeE14vOEPa8UCCGse+dyVATOzj9sNbb7uEGwmwAAAABJRU5ErkJggg=="
    payload = {'qr_code': qr_code, 'seconds': seconds}
    
    return jsonify(response = payload, code = '200')



@app.route('/get_all_transaction', methods=['POST'])
def getAllTransaction():
    transactions = find_all()
    
    return jsonify(response = transactions, code = '201')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8070)

