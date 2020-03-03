from settings import db

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)

