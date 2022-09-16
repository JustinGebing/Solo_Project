from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.account import Account
from flask_bcrypt import Bcrypt
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Games:
    db = 'navdex_schema'

    def __init__(self, data):
        self.id = data['id']
        self.game = data['game']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM games;"
        results = connectToMySQL(cls.db).query_db(query)
        games = []
        for game in results:
            print(games)
            games.append( Games(game) )
        return games
        # for row in results:
        #     game = cls(row)
        #     account_data = {
        #         'id' : row['accounts.id'],
        #         'first_name' : row['first_name'],
        #         'last_name' : row['last_name'],
        #         'email' : row['email'],
        #         'password' : row['password'],
        #         'created_at': row['accounts.created_at'],
        #         'updated_at' : row['accounts.updated_at']
        #     }
        #     account = Account(account_data)
        #     game.account = account
        #     games.append(game)
        # return results

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM games WHERE games.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) < 1:
            return False
        print(results[0])

        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO games (game) Values (%(game)s);'
        save = connectToMySQL(cls.db).query_db(query, data)
        print(save)
        return save
        

    @classmethod
    def update(cls, data):
        query = 'UPDATE games SET game=%(game)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM games WHERE id = %(id)s'
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_games(game):
            valid = True

            if len(game['game']) < 2:
                valid = False
                flash("Trainer, I don't recognize this game.", 'error')

            return valid