from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Account

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/balance', methods=['GET', 'POST'])
def balance():
    if request.method == 'POST':
        name = request.form['name']
        account = Account.query.filter_by(name=name).first()
        if account:
            return render_template('balance.html', balance=account.balance)
        else:
            flash('Account not found', 'error')
    return render_template('balance.html')

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        account = Account.query.filter_by(name=name).first()
        if account:
            account.balance += amount
            db.session.commit()
            flash('Deposit successful', 'success')
        else:
            flash('Account not found', 'error')
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        account = Account.query.filter_by(name=name).first()
        if account:
            if account.balance >= amount:
                account.balance -= amount
                db.session.commit()
                flash('Withdrawal successful', 'success')
            else:
                flash('Insufficient funds', 'error')
        else:
            flash('Account not found', 'error')
    return render_template('withdraw.html')

if __name__ == '__main__':
    app.run(debug=True)
