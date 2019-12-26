from flask import render_template, url_for, request, redirect, flash
from videorentalstore import app, db
from videorentalstore.models import Film, Rental, Customer, Return
from videorentalstore.calculator import calculate_price, calculate_late_charge, calculate_bonus_point
from videorentalstore.forms import CustomerForm, RentalForm, ReturnForm
from datetime import datetime, date
import traceback

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        film_name = request.form['fname']
        film_category = request.form['fcategory']
        new_film = Film(name=film_name, category=film_category)

        try:
            # flash('adding a new film')
            db.session.add(new_film)
            db.session.commit()
            flash(f'  The film {film_name} has been added!', 'success')
            return redirect('/')

        except Exception as e:
            traceback.print_exc()
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
        film.category = request.form['fcategory']
        try:
            db.session.commit()
            flash(f'  The film {film.name} has been updated!', 'success')
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
                    flash('  The due date must be a day after the start date! ')
                    return render_template('add-rental.html', form=form, film=film)
                else:
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
                                flash(f'  The rental for {form.film_name.data} has been added!','success')
                                return redirect('/rentals')

                            except:
                                return 'There was an issue adding the rental'

                    elif film.category == 'regular film':
                        price = calculate_price(days, 'regular film')
                        new_rental.price = price
                        try:
                            db.session.add(new_rental)
                            db.session.commit()
                            flash(f'  The rental for {form.film_name.data} has been added!','success')
                            return redirect('/rentals')

                        except:
                            return 'There was an issue adding the rental'

                    else:
                        price = calculate_price(days, 'old film')
                        new_rental.price = price
                        try:
                            db.session.add(new_rental)
                            db.session.commit()
                            flash(f'  The rental for {form.film_name.data} has been added!','success')
                            return redirect('/rentals')

                        except:
                            return 'There was an issue adding the rental'
                    
            else:
                flash('customer does not exist')
                return render_template('add-rental.html', form=form, film=film)
        
    return render_template('add-rental.html', form=form, film=film)

@app.route('/rentals/return/<int:id>', methods=['POST', 'GET'])
def return_film(id):
    rental = Rental.query.get_or_404(id)
    form = ReturnForm()
    form.film_name.data = rental.film_name
    form.cust_email.data = rental.cust_email
    form.start_date.data = rental.start_date
    form.due_date.data = rental.end_date
    form.return_date.data = date.today()

    if request.method == 'POST':
        if form.validate_on_submit:
            days = rental.end_date.date() - rental.start_date.date()
            overdue_days = (date.today() - rental.end_date.date()).days
            new_return = Return(film_id=rental.film_id,
                                    film_name=rental.film_name,
                                    film_category=rental.film_category,
                                    cust_id=rental.cust_id,
                                    cust_email=rental.cust_email,
                                    start_date=rental.start_date, 
                                    return_date=date.today())
            if overdue_days < 0:
                days = (date.today() - rental.start_date.date()).days
                total_price = calculate_price(days, rental.film_category)
                new_return.overdue_days = 0
                new_return.total_price = total_price
                new_return.late_charge = 0
                try:
                    db.session.add(new_return)
                    db.session.commit()
                    flash(f'  The return for {form.film_name.data} has been added!','success')
                    return redirect('/returns')

                except:
                    return 'There was an issue adding the return'
            else:
                days = (date.today() - rental.start_date.date()).days
                late_charge = calculate_late_charge(overdue_days, rental.film_category)
                new_return.overdue_days = overdue_days
                new_return.total_price = rental.price + late_charge
                new_return.late_charge = late_charge
                try:
                    db.session.add(new_return)
                    db.session.commit()
                    flash(f'  The return for {form.film_name.data} has been added!','success')
                    # flash('Updating bonus points for the customer')
                    customer = Customer.query.get_or_404(rental.cust_id)
                    bpt = calculate_bonus_point(rental.film_category)
                    customer.bonus_points += bpt
                    db.session.commit()
                    flash(f'  The bonus point for {customer.first_name} {customer.last_name} has been added!','success')
                    return redirect('/returns')

                except:
                    return 'There was an issue adding the return'

        return redirect('/returns')

    return render_template('return-rental.html', form=form, rental=rental)    

@app.route('/returns', methods=['GET'])
def get_all_returns():
    returns = Return.query.order_by(Return.return_date).all()
    return render_template('returns.html', returns=returns)  

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
                flash(f'  The customer {form.first_name.data} {form.last_name.data} has been added!','success')
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