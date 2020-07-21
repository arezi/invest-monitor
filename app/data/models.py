



from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()





from sqlalchemy.inspection import inspect
class Serializer(object):
    def serialize_attrs(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}



def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")

def dump_date(value):
    if value is None:
        return None
    return value.strftime("%Y-%m-%d")






class Operation(db.Model, Serializer):
    __tablename__ = "operation"
    
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    buy = db.Column(db.Integer, nullable=False)
    sell = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return "<Op: {}>".format(self.ticker)

    def serialize(self):
        return {
            'id' : self.id,
            'ticker' : self.ticker,
            'price' : self.price,
            'buy' : self.buy,
            'sell' : self.sell,
            'date': dump_date(self.date),
        }

