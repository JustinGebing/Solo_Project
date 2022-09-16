from flask_app import app
from flask_app.controllers import accounts, scenes, games, mons, moves, stats, scenenotes, trainers, wildMons


if __name__=="__main__":
    app.run(debug=True)