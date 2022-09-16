from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.account import Account
from flask_app.models.scene import Scenes
from flask_bcrypt import Bcrypt
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class SceneNotes:
    db = 'navdex_schema'

    def __init__(self, data):
        self.id = data['id']
        self.game = data['game']
        self.scene = data['scene']
        self.encounter = data['encounter']
        self.routeNotes = data['routeNotes']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.account_id = data['account_id']
        self.account = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM scenenotes JOIN accounts ON scenenotes.account_id=accounts.id;"
        results = connectToMySQL(cls.db).query_db(query)
        scenenotes = []
        for row in results:
            note = cls(row)
            account_data = {
                'id' : row['accounts.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at': row['accounts.created_at'],
                'updated_at' : row['accounts.updated_at']
            }
            account = Scenes(account_data)
            note.account = account
            scenenotes.append(note)
        return scenenotes

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM scenenotes JOIN accounts ON scenenotes.account_id=accounts.id WHERE scenenotes.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) < 1:
            return False

        row = results[0]
        show = cls(row)
        account_data = {
                'id' : row['accounts.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at': row['accounts.created_at'],
                'updated_at' : row['accounts.updated_at']
            }
        account = Account(account_data)
        show.account = account

        return show

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO scenenotes (game, scene, encounter, routeNotes, account_id) Values (%(game)s, %(scene)s, %(encounter)s, %(routeNotes)s, %(account_id)s);'
        save = connectToMySQL(cls.db).query_db(query, data)
        print(save)
        return save
        

    @classmethod
    def update(cls, data):
        query = 'UPDATE scenenotes SET game=%(game)s, scene=%(scene)s, encounter=%(encounter)s, routeNotes=%(routeNotes)s, WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM scenenotes WHERE id = %(id)s'
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_scenenotes(scenenote):
            valid = True

            if len(scenenote['routeNotes']) < 1:
                valid = False
                flash('Trainer, be more descriptive!', 'error')

            return valid