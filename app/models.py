from app import db


class Cliente(db.Model):
    __tablename__ = 'Cliente'

    # Colunas
    id_cliente = db.Column(db.String(32), primary_key=True)
    nome = db.Column(db.String(255))
    email = db.Column(db.String(255))
    ddd = db.Column(db.String(2))
    telefone = db.Column(db.String(9))
    observacao = db.Column(db.Text)

    def __repr__(self):
        return '<Cliente {}>'.format(self.nome)

    def to_dict(self):
        data = {
            'id_cliente': self.id_cliente,
            'nome': self.nome,
            'email': self.email,
            'ddd': self.ddd,
            'telefone': self.telefone,
            'observacao': self.observacao,
        }

        return data

    def from_dict(self, data):
        for field in ['nome', 'email', 'ddd', 'telefone', 'observacao']:
            if field in data:
                setattr(self, field, data[field])


class Agendamento(db.Model):
    __tablename__ = 'Agendamento'

    # Colunas
    id_agendamento = db.Column(db.Integer, primary_key=True)
    horario_inicio = db.Column(db.DateTime)
    horario_fim = db.Column(db.DateTime)
    id_cliente = db.Column(db.String(32), db.ForeignKey('Cliente.id_cliente'))
    observacao = db.Column(db.Text)

    #Relacionamento
    cliente = db.relationship('Cliente', backref='Agendamento')

    def __repr__(self):
        return '<Agendamento {}>'.format(self.id_agendamento)

    def to_dict(self):
        data = {
            'id_agendamento': self.id_agendamento,
            'id_cliente': self.id_cliente,
            'cliente': self.cliente.to_dict(),
            'horario_inicio': self.horario_inicio,
            'horario_fim': self.horario_fim,
            'observacao': self.observacao,
        }

        return data

    def from_dict(self, data):
        for field in ['id_cliente', 'horario_inicio', 'horario_fim', 'observacao']:
            if field in data:
                setattr(self, field, data[field])
