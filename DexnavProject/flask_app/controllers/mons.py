from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.mon import Mons
from flask_app.models.account import Account
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)



# @app.route('/dashboard')
# def result():
#     account_data = {
#         'id': session['id']
#     }
#     mons = Mons.get_all()
#     account = Account.get_one(account_data)
#     return render_template('dashboard.html', account=account, mons=mons)

@app.route('/process/mon')
def process_mon():
    return render_template('add_mons.html')

@app.route('/new/mons', methods=['POST'])
def new_mons():
    if Mons.validate_mons(request.form):
        print(request.form['account_id'])
        Mons.save(request.form)
        return redirect('/dashboard')

    return redirect('/process/mon')

@app.route('/mon/<int:id>/mon')
def show_mon(id):
    mon_data = {
        'id' : id
    }
    mon = Mons.get_one(mon_data)
    return render_template('view_mon.html', mon=mon)

@app.route('/edit/<int:id>/mon')
def edit_mon(id):
    mon_data = {
        'id' : id
    }
    mon = Mons.get_one(mon_data)
    return render_template('edit_mon.html', mon=mon)

@app.route('/update/<int:id>/mon', methods=['POST'])
def update_mon(id):
    if Mons.validate_mons(request.form):
        Mons.update(request.form)
        return redirect('/dashboard')
    return redirect(f'/edit/{id}/mon')

@app.route('/delete/<int:id>/mon', methods=['post'])
def delete_mon(id):
    Mons.delete(
        {'id': id}
    )
    return redirect('/dashboard')