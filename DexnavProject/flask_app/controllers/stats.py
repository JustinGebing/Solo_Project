from os import stat
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.stat import Stats
from flask_app.models.account import Account
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)



# @app.route('/dashboard')
# def result():
#     account_data = {
#         'id': session['id']
#     }
#     stats = Stats.get_all()
#     account = Account.get_one(account_data)
#     return render_template('dashboard.html', account=account, stats=stats)

@app.route('/process/stat')
def process_stat():
    return render_template('add_stats.html')

@app.route('/new/stats', methods=['POST'])
def new_stats():
    if Stats.validate_stats(request.form):
        print(request.form['account_id'])
        Stats.save(request.form)
        return redirect('/dashboard')

    return redirect('/process/stat')

@app.route('/stat/<int:id>/stat')
def show_stat(id):
    stat_data = {
        'id' : id
    }
    stat = Stats.get_one(stat_data)
    return render_template('view_stats.html', stat=stat)

@app.route('/edit/<int:id>/stats')
def edit_stats(id):
    stats_data = {
        'id' : id
    }
    stat = Stats.get_one(stats_data)
    return render_template('edit_stats.html', stat=stat)

@app.route('/update/<int:id>/stat', methods=['POST'])
def update_stat(id):
    if Stats.validate_stats(request.form):
        Stats.update(request.form)
        return redirect('/dashboard')
    return redirect(f'/edit/{id}/stat')

@app.route('/delete/<int:id>/stat', methods=['post'])
def delete_stat(id):
    Stats.delete(
        {'id': id}
    )
    return redirect('/dashboard')