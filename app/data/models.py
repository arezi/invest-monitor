



from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


from sqlalchemy.engine.cursor import CursorResult

def to_dict(rs, keys=None):
    #return [dict(it.items()) for it in rs] # doesn't work more :(
    if keys == None:
        keys = rs.keys()
    res = []
    for it in rs:
        res.append(dict(zip(keys, it)))
    return res

from sqlalchemy.inspection import inspect
class Serializer(object):
    def serialize(self):
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
        dto = super().serialize()
        dto['date'] = dump_date(self.date)
        return dto






class Planning(db.Model, Serializer):
    __tablename__ = "planning"
    
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    active = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=True)
    stop_gain = db.Column(db.Float, nullable=True)
    stop_loss = db.Column(db.Float, nullable=True)
    alert_gain = db.Column(db.Float, nullable=True)
    alert_loss = db.Column(db.Float, nullable=True)
    fair_value = db.Column(db.Float, nullable=True)
    notes = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        return "<Pln: {}>".format(self.ticker)

    def serialize(self):
        dto = super().serialize()
        dto['date'] = dump_date(self.date)
        return dto


