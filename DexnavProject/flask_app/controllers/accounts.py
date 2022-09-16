from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.account import Account
from flask_app.models.scene import Scenes
from flask_app.models.game import Games
from flask_app.models.wildmon import WildMons
from flask_app.models.trainer import Trainers
from flask_bcrypt import Bcrypt
from flask import Flask
bcrypt=Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=["POST"])
def process():
    if not Account.validate_account(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        'first_name': request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password': pw_hash,
        }
    
    account = Account.save(data)
    session['id'] = account
    flash(f'{request.form["email"]}, you have registered!')
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete(id):
    Account.delete(
        {'id': id}
    )
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email' : request.form['email'],
        }

    account = Account.get_one_email(data)
    if account:
        if not bcrypt.check_password_hash(account.password, request.form['password']):
            flash('Email or Password is incorect!')
            return redirect('/')
    
        session['id'] = account.id
        flash(f'{account.first_name}, you have successfully logged in!')
        return redirect('/dashboard')

    flash('Email not recognized')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/view')
def view_hiddeninfo():
    account_data = {
        'id': session['id']
    }
    account = Account.get_one(account_data)
    All_scenes = Scenes.get_all()
    All_games = Games.get_all()
    All_trainers = Trainers.get_all()
    All_Wildmons = WildMons.get_all()

    return render_template('hiddeninfo.html', scenes=All_scenes, games=All_games, trainers=All_trainers, wildmons=All_Wildmons, account=account)

@app.route('/add')
def add_scene():
    account_data = {
        'id': session['id']
    }
    All_scenes = Scenes.get_all()
    All_games = Games.get_all()
    return render_template('new_game.html', scenes=All_scenes, games=All_games)

@app.route('/hiddeninfo')
def add_hidden():
    account_data = {
        'id': session['id']
    }
    account = Account.get_one(account_data)
    All_scenes = Scenes.get_all()
    All_games = Games.get_all()
    All_trainers = Trainers.get_all()
    All_Wildmons = WildMons.get_all()

    return render_template('hiddeninfo.html', scenes=All_scenes, games=All_games, trainers=All_trainers, wildmons=All_Wildmons, account=account)

@app.route('/continue')
def view_continue():
    account_data = {
        'id': session['id']
    }
    All_scenes = Scenes.get_all()
    All_games = Games.get_all()
    return render_template('continue.html', scenes=All_scenes, games=All_games)

