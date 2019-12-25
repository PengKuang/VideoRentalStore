class Film(db.Model):
    __tablename__ = "film"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(20))
    available = db.Column(db.Integer, default=1)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    rentals = db.relationship('Rental', backref="film", lazy=True)

    def __repr__(self):
        return '<Film %r>' % self.name

class Rental(db.Model):
    __tablename__ = "rental"

    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    film_name = db.Column(db.String(100))
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    cust_email = db.Column(db.String(120))
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Integer, default=30)

    def __repr__(self):
        return '<Rental %r>' % self.id

class Customer(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    bonus_points = db.Column(db.Integer, nullable=False, default=0)
    rentals = db.relationship('Rental', backref='customer', lazy=True)

    def __repr__(self):
        return '<Customer %r>' % self.id