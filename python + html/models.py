from database import db

class ContasBancarias(db.Model):
    __tablename__ = "contasbancarias"
    id_conta = db.Column(db.Integer, primary_key = True)
    numero_conta = db.Column(db.String(20))
    tipo_conta = db.Column(db.String(20))
    saldo = db.Column(db.Decimal(10, 2))

    def __init__(self, numero_conta, tipo_conta, saldo):
        self.numero_conta = numero_conta
        self.tipo_conta = tipo_conta
        self.saldo = saldo

    def __repr__(self):
        return "<Usuario {}>".format(self.numero_conta)