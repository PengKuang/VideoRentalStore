from flask import Flask
from flask import render_template, url_for, request, redirect
# from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from flask_validator import ValidateInteger, ValidateString, ValidateEmail

app = Flask(__name__)
app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///video.db'
db = SQLAlchemy(app)
# Bootstrap(app)

class Film(db.Model):
    __tablename__ = "film"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(20))
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.content

class Rental(db.Model):
    __tablename__ = "rental"

    id = db.Column(db.Integer, primary_key=True)
    # film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    cust_id = db.Column(db.Integer)
    film_name = db.Column(db.String(200))
    start_date = db.Column(db.String(200))
    end_date = db.Column(db.String(200))

    def __repr__(self):
        return '<Rental %r>' % self.id

class Customer(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    bonus_points = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Customer %r>' % self.id

    # @classmethod
    # def __delcare_last_(cls):
    #     ValidateEmail(Customer.email, true, true, "The e-mail is not valid. Please check it")    

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Film(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return 'there was an issue adding the task'

    else:
        tasks = Film.query.order_by(Film.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Film.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was a problem deleting the task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Film.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue updating the task'
    else:
        return render_template('update.html', task=task)

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
        tasks = Customer.query.all()
        return render_template('customers.html', tasks=tasks)

@app.route('/rent/<int:id>', methods=['GET', 'POST'])
def rent(id):
    film = Film.query.get_or_404(id)

    if request.method == 'POST':
        nfilm_name = film.content
        ncust_id = request.form['customerid']
        nstart_date = request.form['startdate']
        nend_date = request.form['enddate']

        new_rental = Rental(film_name=nfilm_name, cust_id=ncust_id, start_date=nstart_date, end_date=nend_date)

        try:
            db.session.add(new_rental)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue adding the rental'
    else:
        return render_template('rent.html', task=film)

@app.route('/rentals', methods=['GET'])
def get_all_rentals():
    rentals = Rental.query.order_by(Rental.end_date).all()
    return render_template('rentals.html', tasks=rentals)


@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)