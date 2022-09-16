from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.scene import Scenes
from flask_app.models.account import Account
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)



# @app.route('/dashboard')
# def result():
#     account_data = {
#         'id': session['id']
#     }
#     scenes = Scenes.get_all()
#     account = Account.get_one(account_data)
#     return render_template('dashboard.html', account=account, scenes=scenes)

@app.route('/process/scene')
def process_scene():
    return render_template('hiddeninfo.html')

@app.route('/new/scene', strict_slashes=False, methods=['POST'])
def new_scene():
    if Scenes.validate_scenes(request.form):
        # print(request.form['account_id'])
        Scenes.save(request.form)
        return redirect('/hiddeninfo')

    return redirect('/process/scene')

@app.route('/scene/<int:id>/scene')

def show_scene(id):
    scene_data = {
        'id' : id
    }
    scene = Scenes.get_one(scene_data)
    return render_template('view_scene.html', scene=scene)

@app.route('/edit/<int:id>/scene')
def edit_scene(id):
    scene_data = {
        'id' : id
    }
    scene = Scenes.get_one(scene_data)
    return render_template('edit_hiddenSceneinfo.html', scene=scene)

@app.route('/update/<int:id>/scene', methods=['POST'])
def update_scene(id):
    if Scenes.validate_scenes(request.form):
        Scenes.update(request.form)
        return redirect('/hiddeninfo')
    return redirect(f'/edit/{id}/scene')

@app.route('/delete/<int:id>/scene', methods=['post'])
def delete_scene(id):
    Scenes.delete(
        {'id': id}
    )
    return redirect('/hiddeninfo')