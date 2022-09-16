from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.scenenote import SceneNotes
from flask_app.models.account import Account
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)



# @app.route('/dashboard')
# def result():
#     account_data = {
#         'id': session['id']
#     }
#     notes = SceneNotes.get_all()
#     account = Account.get_one(account_data)
#     return render_template('dashboard.html', account=account, notes=notes)

@app.route('/process/notes')
def process_notes():
    return render_template('scenes.html')

@app.route('/new/notes', methods=['POST'])
def new_notes():
    if SceneNotes.validate_scenenotes(request.form):
        print(request.form['account_id'])
        SceneNotes.save(request.form)
        return redirect('/process/notes')

    return redirect('/process/notes')

@app.route('/notes/<int:id>/notes')
def show_note(id):
    note_data = {
        'id' : id
    }
    note = SceneNotes.get_one(note_data)
    return render_template('view_note.html', note=note)

@app.route('/edit/<int:id>/note')
def edit_notes(id):
    note_data = {
        'id' : id
    }
    note = SceneNotes.get_one(note_data)
    return render_template('edit_note.html', note=note)

@app.route('/update/<int:id>/note', methods=['POST'])
def update_note(id):
    if SceneNotes.validate_scenenotes(request.form):
        SceneNotes.update(request.form)
        return redirect('/dashboard')
    return redirect(f'/edit/{id}/note')

@app.route('/delete/<int:id>/note', methods=['post'])
def delete_note(id):
    SceneNotes.delete(
        {'id': id}
    )
    return redirect('/dashboard')

