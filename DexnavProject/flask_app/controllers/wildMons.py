from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.wildmon import WildMons
from flask_app.models.account import Account
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)



# @app.route('/dashboard')
# def result():
#     account_data = {
#         'id': session['id']
#     }
#     wildmons = WildMons.get_all()
#     account = Account.get_one(account_data)
#     return render_template('dashboard.html', account=account, wildmons=wildmons)

@app.route('/process/wildmon')
def process_wildmon():
    return render_template('hiddeninfo.html')

@app.route('/new/wildmons', methods=['POST'])
def new_wildmons():
    if WildMons.validate_wildmon(request.form):
        # print(request.form['account_id'])
        WildMons.save(request.form)
        return redirect('/hiddeninfo')

    return redirect('/process/wildmon')

@app.route('/wildmon/<int:id>/wildmon')
def show_wildmon(id):
    wildmon_data = {
        'id' : id
    }
    wildmon = WildMons.get_one(wildmon_data)
    return render_template('view_wildmon.html', wildmon=wildmon)

@app.route('/edit/<int:id>/wildmon')
def edit_wildmon(id):
    wildmon_data = {
        'id' : id
    }
    wildmon = WildMons.get_one(wildmon_data)
    return render_template('edit_hiddenWildmonInfo.html', wildmon=wildmon)

@app.route('/update/<int:id>/wildmon', methods=['POST'])
def update_wildmon(id):
    if WildMons.validate_wildmon(request.form):
        WildMons.update(request.form)
        return redirect('/hiddeninfo')
    return redirect(f'/edit/{id}/wildmon')

@app.route('/delete/<int:id>/wildmon', methods=['post'])
def delete_wildmon(id):
    WildMons.delete(
        {'id': id}
    )
    return redirect('/hiddeninfo')