from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.trainer import Trainers
from flask_app.models.account import Account
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)



# @app.route('/dashboard')
# def result():
#     account_data = {
#         'id': session['id']
#     }
#     trainers = Trainers.get_all()
#     account = Account.get_one(account_data)
#     return render_template('dashboard.html', account=account, trainers=trainers)

@app.route('/process/trainer')
def process_trainer():
    return render_template('hiddeninfo.html')

@app.route('/new/trainers', methods=['POST'])
def new_trainers():
    if Trainers.validate_trainers(request.form):
        Trainers.save(request.form)
        return redirect('/hiddeninfo')

    return redirect('/process/trainer')

@app.route('/trainer/<int:id>/trainer')
def show_trainer(id):
    trainer_data = {
        'id' : id
    }
    trainer = Trainers.get_one(trainer_data)
    return render_template('view_trainer.html', trainer=trainer)

@app.route('/edit/<int:id>/trainer')
def edit_trainer(id):
    trainer_data = {
        'id' : id
    }
    trainer = Trainers.get_one(trainer_data)
    return render_template('edit_hiddenTrainerInfo.html', trainer=trainer)

@app.route('/update/<int:id>/trainer', methods=['POST'])
def update_trainer(id):
    if Trainers.validate_trainers(request.form):
        Trainers.update(request.form)
        return redirect('/hiddeninfo')
    return redirect(f'/edit/{id}/trainer')

@app.route('/delete/<int:id>/trainer', methods=['post'])
def delete_trainer(id):
    Trainers.delete(
        {'id': id}
    )
    return redirect('/hiddeninfo')