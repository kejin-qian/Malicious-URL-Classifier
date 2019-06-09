from app import db


class URL(db.Model):
    """
    Create a data model for the database to be set up for capturing user-input url
    """
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), unique=False, nullable=False)
    pred = db.Column(db.Integer, unique=False, nullable=False)


    def __repr__(self):
        return '<URL address %r>' % self.url

