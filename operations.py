# from app import db
# from flask import flash

# def insert_data(new_object, flash_var):
#     try:
#         db.session.add(new_object)
#         db.session.commit()
#         flash(f'The rental for {flash_var} has been added!','success')
#         return redirect('/rentals')

#     except:
#         return 'There was an issue adding the rental'