from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return f'<Account {self.name}>'
