from flask import Flask
from flask import render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import CustomerForm, RentalForm
from calculator import calculate_price, calculate_late_charge

app = Flask(__name__)
app.config['SECRET_KEY'] = '229b845d2e364ca8a032e35c104f69b1'
app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///video.db'
# db.init_app(app)
db = SQLAlchemy(app)

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
    film_category = db.Column(db.String(20))
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

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        film_name = request.form['fname']
        film_category = request.form['fcategory']
        new_film = Film(name=film_name, category=film_category)

        try:
            db.session.add(new_film)
            db.session.commit()
            return redirect('/')

        except:
            return 'there was an issue adding the film'

    else:
        films = Film.query.all()
        return render_template('index.html', films=films)

@app.route('/delete/<int:id>')
def delete(id):
    film_to_delete = Film.query.get_or_404(id)

    try:
        db.session.delete(film_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was a problem deleting the film'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    film = Film.query.get_or_404(id)

    if request.method == 'POST':
        film.name = request.form['fname']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue updating the film'
    else:
        return render_template('update.html', film=film)

@app.route('/rent/<int:id>', methods=['GET', 'POST'])
def rent(id):
    film = Film.query.get_or_404(id)

    if request.method == 'POST':
        nfilm_name = film.name
        ncust_id = request.form['customerid']
        nstart_date = request.form['startdate']
        nend_date = request.form['enddate']

        new_rental = Rental(film_name=nfilm_name, cust_id=ncust_id, start_date=nstart_date, end_date=nend_date)

        try:
            db.session.add(new_rental)
            db.session.commit()
            return redirect('/rentals')
        except:
            return 'there was an issue adding the rental'
    else:
        return render_template('rent.html', film=film)

@app.route('/rentals', methods=['GET'])
def get_all_rentals():
    rentals = Rental.query.order_by(Rental.end_date).all()
    return render_template('rentals.html', rentals=rentals)

@app.route("/rentals/add/<int:id>", methods=['GET', 'POST'])
def add_rental(id):
    film = Film.query.get_or_404(id)
    form = RentalForm()
    form.film_name.data = film.name

    if request.method == 'POST':
        if form.validate_on_submit:
            cust_email=form.cust_email.data
            customer = Customer.query.filter_by(email=cust_email).first()
    
            if customer:
                if form.start_date.data > form.end_date.data:
                    flash('The due date must be a day after the start date! ')
                    return render_template('add-rental.html', form=form, film=film)
                else:
                    # y,m,d = form.start_date.data.split('-')
                    # startdate = datetime.datetime(int(y), int(m), int(d))
                    # y,m,d = form.end_date.data.split('-')
                    # enddate = datetime.datetime(int(y), int(m), int(d))

                    # if film.category == 'New release':
                    premium_price = 40
                    basic_price = 30
                    new_rental = Rental(film_id=film.id,
                                    film_name=film.name,
                                    film_category=film.category,
                                    cust_id=customer.id,
                                    cust_email=customer.email,
                                    start_date=form.start_date.data, 
                                    end_date=form.end_date.data)
                    days = (form.end_date.data - form.start_date.data).days

                    if film.category == 'new release':
                            price = days * premium_price
                            new_rental.price = price
                            try:
                                db.session.add(new_rental)
                                db.session.commit()
                                flash('The rental has been added!','success')
                                return redirect('/rentals')

                            except:
                                return 'There was an issue adding the rental'

                    elif film.category == 'regular film':
                            if days <= 3:
                                price = basic_price
                                new_rental.price = price
                                try:
                                    db.session.add(new_rental)
                                    db.session.commit()
                                    flash('The rental has been added!','success')
                                    return redirect('/rentals')

                                except:
                                    return 'There was an issue adding the rental'
                            else:
                                price = basic_price + (days - 3) * basic_price
                                new_rental.price = price
                                try:
                                    db.session.add(new_rental)
                                    db.session.commit()
                                    flash('The rental has been added!','success')
                                    return redirect('/rentals')

                                except:
                                    return 'There was an issue adding the rental'

                    else:

                        price = calculate_price(days, 'old film')
                        new_rental.price = price
                        try:
                            db.session.add(new_rental)
                            db.session.commit()
                            flash(f'The rental for {form.film_name.data} has been added!','success')
                            return redirect('/rentals')

                        except:
                            return 'There was an issue adding the rental'
                        # if days <= 5:
                        #         price = basic_price
                        #         new_rental.price = price
                        #         try:
                        #             db.session.add(new_rental)
                        #             db.session.commit()
                        #             flash(f'The rental for {form.film_name.data} has been added!','success')
                        #             return redirect('/rentals')

                        #         except:
                        #             return 'There was an issue adding the rental'
                        # else:
                        #     price = basic_price + (days - 5) * basic_price
                        #     new_rental.price = price
                            
                        #     try:
                        #         db.session.add(new_rental)
                        #         db.session.commit()
                        #         flash(f'The rental for {form.film_name.data} has been added!','success')
                        #         return redirect('/rentals')

                        #     except:
                        #         return 'There was an issue adding the rental'
                    
            else:
                flash('customer does not exist')
                return render_template('add-rental.html', form=form, film=film)
                
        #     else:
        #         return render_template('add-rental.html', form=form)
        # else:
        #     return render_template('add-rental.html', form=form)
    # else:
        # flash('Customer does not exist! ')
    return render_template('add-rental.html', form=form, film=film)

@app.route('/customers', methods=['POST','GET'])
def customer():
    if request.method == 'POST':
        cust_email = request.form['email']
        cust_firstname = request.form['firstname']
        cust_lastname = request.form['lastname']
        new_customer = Customer(email=cust_email, first_name=cust_firstname, last_name=cust_lastname)

        try:
            db.session.add(new_customer)
            db.session.commit()
            return redirect('/customers')

        except:
            return 'there was an issue adding the customer'

    else:
        customers = Customer.query.all()
        return render_template('customers.html', customers=customers)

@app.route("/customers/add", methods=['GET', 'POST'])
def add_customer():
    form = CustomerForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_customer = Customer(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data)
            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('The customer has been added!','success')
                return redirect('/customers')

            except:
                return 'there was an issue adding the customer'
        else:
            return render_template('add-customer.html', form=form)
    else:
        return render_template('add-customer.html', form=form)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)