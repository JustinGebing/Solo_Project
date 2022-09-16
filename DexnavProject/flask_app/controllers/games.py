from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.game import Games
from flask_app.models.account import Account
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)



@app.route('/dashboard')
def result():
    account_data = {
        'id': session['id']
    }
    account = Account.get_one(account_data)
    return render_template('dashboard.html', account=account )

@app.route('/process/game')
def process_game():
    return render_template('hiddeninfo.html')

@app.route('/new/games', strict_slashes=False, methods=['POST'])
def new_game():
    if Games.validate_games(request.form):
        Games.save(request.form)
        return redirect('/hiddeninfo')

    return redirect('/process/game')

@app.route('/game/<int:id>/game')

def show_game(id):
    game_data = {
        'id' : id
    }
    game = Games.get_one(game_data)
    return render_template('view_game.html', game=game)

@app.route('/edit/<int:id>/game')

def edit_game(id):
    game_data = {
        'id' : id
    }
    game = Games.get_one(game_data)
    return render_template('edit_hiddenGameInfo.html', game=game)

@app.route('/update/<int:id>/game', methods=['POST'])
def update_game(id):
    if Games.validate_games(request.form):
        Games.update(request.form)
        return redirect('/hiddeninfo')

    return redirect(f'/edit/{id}/game')

@app.route('/delete/<int:id>/game', methods=['post'])
def delete_game(id):
    Games.delete(
        {'id': id}
    )
    return redirect('/hiddeninfo')