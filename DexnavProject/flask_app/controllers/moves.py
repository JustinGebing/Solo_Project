from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.move import Moves
from flask_app.models.account import Account
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)



# @app.route('/dashboard')
# def result():
#     account_data = {
#         'id': session['id']
#     }
#     moves = Moves.get_all()
#     account = Account.get_one(account_data)
#     return render_template('dashboard.html', account=account, moves=moves)

@app.route('/process/move')
def process_move():
    return render_template('add_moves.html')

@app.route('/new/move', methods=['POST'])
def new_moves():
    if Moves.validate_moves(request.form):
        print(request.form['account_id'])
        Moves.save(request.form)
        return redirect('/dashboard')

    return redirect('/process/move')

@app.route('/move/<int:id>/move')
def show_move(id):
    move_data = {
        'id' : id
    }
    move = Moves.get_one(move_data)
    return render_template('view_move.html', move=move)

@app.route('/edit/<int:id>/move')
def edit_move(id):
    move_data = {
        'id' : id
    }
    move = Moves.get_one(move_data)
    return render_template('edit_move.html', move=move)

@app.route('/update/<int:id>/move', methods=['POST'])
def update_move(id):
    if Moves.validate_moves(request.form):
        Moves.update(request.form)
        return redirect('/dashboard')
    return redirect(f'/edit/{id}/move')

@app.route('/delete/<int:id>/move', methods=['post'])
def delete_move(id):
    Moves.delete(
        {'id': id}
    )
    return redirect('/dashboard')